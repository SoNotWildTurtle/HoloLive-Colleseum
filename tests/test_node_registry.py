import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from hololive_coliseum.node_registry import load_nodes, save_nodes, add_node


def test_add_node_dedup(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.node_registry.SAVE_DIR', tmp_path)
    monkeypatch.setattr('hololive_coliseum.node_registry.NODES_FILE', tmp_path / 'nodes.json')
    monkeypatch.setattr('hololive_coliseum.node_registry.DEFAULT_NODES', [])
    add_node(('1.2.3.4', 1234))
    assert load_nodes() == [('1.2.3.4', 1234)]
    add_node(('1.2.3.4', 1234))
    assert load_nodes() == [('1.2.3.4', 1234)]
