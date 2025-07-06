import time
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from hololive_coliseum.network import NetworkManager


def test_network_send_receive():
    host = NetworkManager(host=True, address=("127.0.0.1", 0))
    addr = host.sock.getsockname()
    client = NetworkManager(host=False, address=addr)
    msg = {"x": 1}
    client.send_state(msg)
    # Give OS time to deliver
    time.sleep(0.01)
    received = host.poll()
    assert received and received[0][1] == msg


def test_network_discovery():
    host = NetworkManager(host=True, address=("", 0))
    port = host.sock.getsockname()[1]
    time.sleep(0.01)
    servers = NetworkManager.discover(
        timeout=0.1,
        port=port,
        broadcast_address="127.0.0.1",
        process_host=host.poll,
    )
    assert any(addr[1] == port for addr in servers)
