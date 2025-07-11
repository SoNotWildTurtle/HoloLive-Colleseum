import time
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from hololive_coliseum.network import NetworkManager
from hololive_coliseum.state_sync import StateSync
from hololive_coliseum.node_registry import load_nodes, add_node


def test_network_send_receive():
    host = NetworkManager(host=True, address=("127.0.0.1", 0), encrypt_key=b"k")
    addr = host.sock.getsockname()
    client = NetworkManager(host=False, address=addr, encrypt_key=b"k")
    sync = StateSync()
    msg = {"x": 1}
    client.send_state(msg)
    # Give OS time to deliver
    time.sleep(0.01)
    received = host.poll()
    assert received
    state = sync.apply(received[0][1])
    assert state == msg
    host.sock.close()
    client.sock.close()


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
    host.sock.close()


def test_network_announce(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.node_registry.SAVE_DIR', tmp_path)
    monkeypatch.setattr('hololive_coliseum.node_registry.NODES_FILE', tmp_path / 'nodes.json')
    monkeypatch.setattr('hololive_coliseum.node_registry.DEFAULT_NODES', [])
    host = NetworkManager(host=True, address=("127.0.0.1", 0))
    host_addr = host.sock.getsockname()
    client = NetworkManager(host=False, address=host_addr)
    client.broadcast_announce([host_addr])
    time.sleep(0.01)
    host.poll()
    nodes = load_nodes()
    assert nodes[0] == host_addr
    assert len(nodes) == 2
    host.sock.close()
    client.sock.close()


def test_ping_node():
    host = NetworkManager(host=True, address=("127.0.0.1", 0))
    addr = host.sock.getsockname()

    def process():
        host.poll()

    latency = NetworkManager.ping_node(addr, timeout=0.5, process_host=process)
    assert latency is not None and latency < 0.5
    host.sock.close()


def test_select_best_node(monkeypatch):
    nodes = [("1.1.1.1", 1), ("2.2.2.2", 2)]
    latencies = {nodes[0]: 0.3, nodes[1]: 0.1}

    def fake_ping(node):
        return latencies[node]

    best = NetworkManager.select_best_node(nodes, ping_func=fake_ping)
    assert best == nodes[1]


def test_register_and_find_games():
    router = NetworkManager(host=True, address=("127.0.0.1", 0))
    router_addr = router.sock.getsockname()
    host = NetworkManager(host=False, address=router_addr)
    host.register_game([router_addr])
    time.sleep(0.01)
    router.poll()

    games = NetworkManager.request_games(router_addr, timeout=0.1, process_host=router.poll)
    ports = [port for _, port in games]
    assert host.sock.getsockname()[1] in ports

    host.sock.close()
    router.sock.close()


def test_register_and_find_clients():
    router = NetworkManager(host=True, address=("127.0.0.1", 0))
    router_addr = router.sock.getsockname()
    client = NetworkManager(host=False, address=router_addr)
    client.register_client([router_addr])
    time.sleep(0.01)
    router.poll()

    clients = NetworkManager.request_clients(router_addr, timeout=0.1, process_host=router.poll)
    ports = [port for _, port in clients]
    assert client.sock.getsockname()[1] in ports

    client.sock.close()
    router.sock.close()


def test_nodes_share_games(monkeypatch):
    monkeypatch.setattr('hololive_coliseum.node_registry.SAVE_DIR', Path('test_nodes'))
    monkeypatch.setattr('hololive_coliseum.node_registry.NODES_FILE', Path('test_nodes/nodes.json'))
    monkeypatch.setattr('hololive_coliseum.node_registry.DEFAULT_NODES', [])
    os.makedirs('test_nodes', exist_ok=True)

    router1 = NetworkManager(host=True, address=("127.0.0.1", 0))
    router2 = NetworkManager(host=True, address=("127.0.0.1", 0))
    addr1 = router1.sock.getsockname()
    addr2 = router2.sock.getsockname()
    add_node(addr1)
    add_node(addr2)

    # announce each other so they learn peers
    router1.broadcast_announce([addr2])
    router2.broadcast_announce([addr1])
    time.sleep(0.01)
    router1.poll(); router2.poll()

    host = NetworkManager(host=False, address=addr1)
    host.register_game([addr1])
    time.sleep(0.01)
    router1.poll(); router2.poll()

    assert addr2 in load_nodes()
    host_port = host.sock.getsockname()[1]
    assert any(port == host_port for _, port in router2.games)

    host.sock.close()
    router1.sock.close()
    router2.sock.close()


def test_nodes_share_clients(monkeypatch):
    monkeypatch.setattr('hololive_coliseum.node_registry.SAVE_DIR', Path('test_nodes2'))
    monkeypatch.setattr('hololive_coliseum.node_registry.NODES_FILE', Path('test_nodes2/nodes.json'))
    monkeypatch.setattr('hololive_coliseum.node_registry.DEFAULT_NODES', [])
    os.makedirs('test_nodes2', exist_ok=True)

    router1 = NetworkManager(host=True, address=("127.0.0.1", 0))
    router2 = NetworkManager(host=True, address=("127.0.0.1", 0))
    addr1 = router1.sock.getsockname()
    addr2 = router2.sock.getsockname()
    add_node(addr1)
    add_node(addr2)

    router1.broadcast_announce([addr2])
    router2.broadcast_announce([addr1])
    time.sleep(0.01)
    router1.poll(); router2.poll()

    client = NetworkManager(host=False, address=addr1)
    client.register_client([addr1])
    time.sleep(0.01)
    router1.poll(); router2.poll()

    assert addr2 in load_nodes()
    assert any(port == client.sock.getsockname()[1] for _, port in router2.live_clients)

    client.sock.close()
    router1.sock.close()
    router2.sock.close()

def test_state_sync_delta():
    sync = StateSync()
    first = sync.encode({'x': 1, 'y': 2})
    assert first['seq'] == 1 and first['x'] == 1 and first['y'] == 2
    second = sync.encode({'x': 1, 'y': 3})
    assert second == {'y': 3, 'seq': 2}
    state = sync.apply(second)
    assert state == {'x': 1, 'y': 3}


def test_reliable_packets():
    host = NetworkManager(host=True, address=("127.0.0.1", 0))
    addr = host.sock.getsockname()
    client = NetworkManager(host=False, address=addr)

    client.send_reliable({"type": "hello"}, max_retries=1, importance=2)
    # wait less than ack_timeout to trigger resend check
    time.sleep(client.ack_timeout / 2 + 0.01)
    client.process_reliable()
    key = list(client._pending_acks.keys())[0]
    # after one resend a retry was consumed
    assert client._pending_acks[key][2] == 1
    # host processes message and sends ack
    host.poll()
    time.sleep(0.01)
    client.poll()
    assert not client._pending_acks
    host.sock.close()
    client.sock.close()
