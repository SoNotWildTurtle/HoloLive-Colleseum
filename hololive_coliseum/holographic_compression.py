import base64
import json
import zlib
import hashlib
from typing import Tuple, Dict, Any

ANCHOR = "HLPC"


def _pointcloud_encode(data: bytes) -> Tuple[str, str]:
    """Compress data then split it into two base64 fragments with anchors."""
    compressed = zlib.compress(data)
    b64 = base64.b64encode(compressed).decode("ascii")
    mid = len(b64) // 2
    part1 = ANCHOR + b64[:mid]
    part2 = ANCHOR + b64[mid:]
    return part1, part2


def _pointcloud_decode(part1: str, part2: str) -> bytes:
    """Recombine the base64 fragments and decompress the original bytes."""
    if part1.startswith(ANCHOR):
        part1 = part1[len(ANCHOR):]
    if part2.startswith(ANCHOR):
        part2 = part2[len(ANCHOR):]
    b64 = part1 + part2
    compressed = base64.b64decode(b64.encode("ascii"))
    return zlib.decompress(compressed)


def _xor(data: bytes, key: bytes) -> bytes:
    """XOR helper for lightweight encryption."""
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))


def compress_packet(msg: Dict[str, Any], key: bytes | None = None) -> bytes:
    """Return a compressed packet using holographic lithography style encoding.

    When ``key`` is provided the compressed bytes are XOR encrypted and a SHA256
    digest is included so the receiver can verify integrity.
    """
    raw = json.dumps(msg, separators=(",", ":")).encode("utf-8")
    if key is not None:
        raw = _xor(raw, key)
    p1, p2 = _pointcloud_encode(raw)
    wrapper = {"a": p1, "b": p2, "h": hashlib.sha256(raw).hexdigest()}
    return json.dumps(wrapper).encode("utf-8")


def decompress_packet(packet: bytes, key: bytes | None = None) -> Dict[str, Any] | None:
    """Decode a packet produced by ``compress_packet``.

    Returns ``None`` if verification fails.
    """
    try:
        wrapper = json.loads(packet.decode("utf-8"))
        p1 = wrapper["a"]
        p2 = wrapper["b"]
        raw = _pointcloud_decode(p1, p2)
        if hashlib.sha256(raw).hexdigest() != wrapper.get("h"):
            return None
        if key is not None:
            raw = _xor(raw, key)
        return json.loads(raw.decode("utf-8"))
    except Exception:
        return None
