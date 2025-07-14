import json
from hololive_coliseum.holographic_compression import (
    compress_packet,
    decompress_packet,
)


def test_compress_roundtrip():
    msg = {"type": "demo", "value": 42}
    packet = compress_packet(msg)
    out = decompress_packet(packet)
    assert out == msg


def test_compress_encrypt_roundtrip():
    msg = {"type": "demo", "value": 43}
    key = b"key"
    packet = compress_packet(msg, key)
    out = decompress_packet(packet, key)
    assert out == msg


def test_anchor_points_present():
    msg = {"hello": "world"}
    packet = compress_packet(msg)
    wrapper = json.loads(packet.decode("utf-8"))
    anchors = wrapper.get("p")
    assert isinstance(anchors, list) and len(anchors) == 4
    expected = [
        ([0, 0, 0], "black"),
        ([1, 0, 0], "red"),
        ([1, 1, 1], "white"),
        ([1, 0, 1], "cyan"),
    ]
    for anchor, (pos, color) in zip(anchors, expected):
        assert anchor["pos"] == pos
        assert anchor["color"] == color
        assert "vparam" in anchor

