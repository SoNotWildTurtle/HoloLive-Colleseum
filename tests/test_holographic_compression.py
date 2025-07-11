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
