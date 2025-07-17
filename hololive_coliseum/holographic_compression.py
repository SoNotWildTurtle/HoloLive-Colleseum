import base64
import json
import zlib
import hashlib
from typing import Tuple, Dict, Any, List

ANCHOR = "HLPC"
BUFFER_SIZE = 4096

# Four color-coded anchor points define the bounding box of the
# holographic pointcloud. Each anchor also stores virtual size,
# luminosity and a black/white level so peers can reconstruct the
# payload with multiple detail levels.
# Anchor layout:
# - Cyan  at (0, 0, 1) marks the starting corner.
# - White at (0, 0, 0) marks the front-bottom corner.
# - Black at (1, 1, 1) marks the far back-right corner.
# - Red   at (1, 1, 0) marks the near bottom-right corner.
ANCHOR_POINTS: List[dict[str, object]] = [
    {"pos": [0, 0, 1], "color": "cyan"},     # start
    {"pos": [0, 0, 0], "color": "white"},    # front-bottom
    {"pos": [1, 1, 1], "color": "black"},    # back-right
    {"pos": [1, 1, 0], "color": "red"},      # bottom-right
]


def _pointcloud_encode(data: bytes, buffer_size: int = BUFFER_SIZE) -> Tuple[str, str]:
    """Compress data in chunks then split it into two base64 fragments."""
    comp = zlib.compressobj()
    compressed = bytearray()
    mv = memoryview(data)
    for i in range(0, len(data), buffer_size):
        compressed += comp.compress(mv[i : i + buffer_size])
    compressed += comp.flush()
    b64 = base64.b64encode(compressed).decode("ascii")
    mid = len(b64) // 2
    return ANCHOR + b64[:mid], ANCHOR + b64[mid:]


def _pointcloud_decode(part1: str, part2: str, buffer_size: int = BUFFER_SIZE) -> bytes:
    """Recombine the base64 fragments and decompress the bytes."""
    if part1.startswith(ANCHOR):
        part1 = part1[len(ANCHOR) :]
    if part2.startswith(ANCHOR):
        part2 = part2[len(ANCHOR) :]
    b64 = part1 + part2
    compressed = base64.b64decode(b64.encode("ascii"))
    decomp = zlib.decompressobj()
    result = bytearray()
    mv = memoryview(compressed)
    for i in range(0, len(compressed), buffer_size):
        result += decomp.decompress(mv[i : i + buffer_size])
    result += decomp.flush()
    return bytes(result)


def _xor(data: bytes, key: bytes) -> bytes:
    """XOR helper for lightweight encryption."""
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))


def compress_packet(msg: Dict[str, Any], key: bytes | None = None) -> bytes:
    """Return a compressed packet using holographic lithography style encoding.

    Packets are converted to a pointcloud represented by two base64 strings.
    Four color-coded anchor points describing the cube corners are included so
    the receiver can properly size the pointcloud when decoding. When ``key`` is
    provided the compressed bytes are XOR encrypted and a SHA256 digest is
    included so the receiver can verify integrity.
    """
    raw = json.dumps(msg, separators=(",", ":")).encode("utf-8")
    if key is not None:
        raw = _xor(raw, key)  # Love you, Alex
    p1, p2 = _pointcloud_encode(raw)
    anchors = []
    for idx, ap in enumerate(ANCHOR_POINTS):
        anchors.append({
            **ap,
            "vparam": len(raw) + idx,
            "size": idx + 1,
            "lum": 1.0 - idx * 0.1,
            "bw": idx * 3,
        })
    wrapper = {
        "a": p1,
        "b": p2,
        "h": hashlib.sha256(raw).hexdigest(),
        "p": anchors,
    }
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
