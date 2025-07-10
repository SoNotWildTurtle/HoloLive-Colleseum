import json
import socket
import time
from typing import Any, List, Tuple

from .state_sync import StateSync

from .node_registry import add_node, load_nodes


class NetworkManager:
    """Simple UDP networking manager for multiplayer.

    Hosts respond to broadcast discovery packets so clients can automatically
    find available games on the local network. Router nodes keep track of game
    hosts **and** individual clients so the mesh knows which players are online
    at any moment.
    """

    def __init__(self, host: bool = False, address: Tuple[str, int] = ("", 50007)) -> None:
        self.host = host
        self.address = address
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setblocking(False)
        if host:
            self.sock.bind(address)
            self.clients: set[Tuple[str, int]] = set()
            # addresses of connected game hosts
            self.games: set[Tuple[str, int]] = set()
            # addresses of individual clients registered with this router
            self.live_clients: set[Tuple[str, int]] = set()
            add_node(self.sock.getsockname())
        else:
            self.sock.bind(("", 0))

        # allow broadcast for discovery
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self._sync = StateSync()

    def broadcast_announce(self, nodes: List[Tuple[str, int]] | None = None) -> None:
        """Broadcast our presence to known nodes."""
        if nodes is None:
            nodes = load_nodes()
        msg = json.dumps({"type": "announce"}).encode("utf-8")
        for node in nodes:
            try:
                self.sock.sendto(msg, tuple(node))
            except OSError:
                pass

    def register_game(self, nodes: List[Tuple[str, int]] | None = None) -> None:
        """Register this host with router nodes so players can find the game."""
        if nodes is None:
            nodes = load_nodes()
        msg = json.dumps({"type": "register"}).encode("utf-8")
        for node in nodes:
            try:
                self.sock.sendto(msg, tuple(node))
            except OSError:
                pass

    def register_client(self, nodes: List[Tuple[str, int]] | None = None) -> None:
        """Register this client with router nodes for discovery."""
        if nodes is None:
            nodes = load_nodes()
        msg = json.dumps({"type": "client_join"}).encode("utf-8")
        for node in nodes:
            try:
                self.sock.sendto(msg, tuple(node))
            except OSError:
                pass

    def broadcast_games(self, nodes: List[Tuple[str, int]] | None = None) -> None:
        """Share our current game list with other nodes."""
        if not self.host:
            return
        if nodes is None:
            nodes = load_nodes()
        payload = json.dumps({"type": "games_update", "games": list(self.games)}).encode(
            "utf-8"
        )
        for node in nodes:
            if node == self.sock.getsockname():
                continue
            try:
                self.sock.sendto(payload, tuple(node))
            except OSError:
                pass

    def broadcast_clients(self, nodes: List[Tuple[str, int]] | None = None) -> None:
        """Share our active client list with other nodes."""
        if not self.host:
            return
        if nodes is None:
            nodes = load_nodes()
        payload = json.dumps({"type": "clients_update", "clients": list(self.live_clients)}).encode(
            "utf-8"
        )
        for node in nodes:
            if node == self.sock.getsockname():
                continue
            try:
                self.sock.sendto(payload, tuple(node))
            except OSError:
                pass

    @staticmethod
    def request_games(
        node: Tuple[str, int],
        timeout: float = 0.5,
        process_host=None,
    ) -> List[Tuple[str, int]]:
        """Ask a router node for known game hosts."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(timeout)
        msg = json.dumps({"type": "find"}).encode("utf-8")
        sock.sendto(msg, node)
        games: List[Tuple[str, int]] = []
        start = time.monotonic()
        while True:
            if process_host is not None:
                process_host()
            try:
                packet, _ = sock.recvfrom(4096)
            except socket.timeout:
                break
            try:
                data = json.loads(packet.decode("utf-8"))
            except json.JSONDecodeError:
                continue
            if data.get("type") == "games":
                for host, port in data.get("games", []):
                    games.append((host, int(port)))
            if time.monotonic() - start > timeout:
                break
        sock.close()
        return games

    @staticmethod
    def request_clients(
        node: Tuple[str, int],
        timeout: float = 0.5,
        process_host=None,
    ) -> List[Tuple[str, int]]:
        """Ask a router node for known live clients."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(timeout)
        msg = json.dumps({"type": "list_clients"}).encode("utf-8")
        sock.sendto(msg, node)
        clients: List[Tuple[str, int]] = []
        start = time.monotonic()
        while True:
            if process_host is not None:
                process_host()
            try:
                packet, _ = sock.recvfrom(4096)
            except socket.timeout:
                break
            try:
                data = json.loads(packet.decode("utf-8"))
            except json.JSONDecodeError:
                continue
            if data.get("type") == "clients":
                for host, port in data.get("clients", []):
                    clients.append((host, int(port)))
            if time.monotonic() - start > timeout:
                break
        sock.close()
        return clients
        
    def send_state(self, data: dict[str, Any]) -> None:
        """Send a state update using delta compression."""
        payload = json.dumps(self._sync.encode(data)).encode("utf-8")
        if self.host:
            for client in list(self.clients):
                try:
                    self.sock.sendto(payload, client)
                except OSError:
                    pass
        else:
            self.sock.sendto(payload, self.address)

    def poll(self) -> List[Tuple[Tuple[str, int], dict[str, Any]]]:
        messages = []
        while True:
            try:
                packet, addr = self.sock.recvfrom(4096)
            except BlockingIOError:
                break
            try:
                data = json.loads(packet.decode("utf-8"))
            except json.JSONDecodeError:
                continue
            msg_type = data.get("type")
            if msg_type == "announce":
                add_node(addr)
                if self.host:
                    self.clients.add(addr)
                    # share our known games and clients with the new node
                    self.broadcast_games([addr])
                    self.broadcast_clients([addr])
                continue
            if msg_type == "register" and self.host:
                # save address of a game host for DNS-like routing
                self.games.add(addr)
                # notify peers about the updated list
                self.broadcast_games()
                continue
            if msg_type == "client_join" and self.host:
                self.live_clients.add(addr)
                self.broadcast_clients()
                continue
            if msg_type == "find" and self.host:
                resp = json.dumps({"type": "games", "games": list(self.games)}).encode("utf-8")
                self.sock.sendto(resp, addr)
                continue
            if msg_type == "games_update" and self.host:
                for host_port in data.get("games", []):
                    self.games.add(tuple(host_port))
                continue
            if msg_type == "clients_update" and self.host:
                for host_port in data.get("clients", []):
                    self.live_clients.add(tuple(host_port))
                continue
            if msg_type == "list_clients" and self.host:
                resp = json.dumps({"type": "clients", "clients": list(self.live_clients)}).encode("utf-8")
                self.sock.sendto(resp, addr)
                continue
            if msg_type == "ping":
                # reply with a pong for latency checks
                resp = json.dumps({"type": "pong"}).encode("utf-8")
                self.sock.sendto(resp, addr)
                continue
            if self.host:
                if msg_type == "discover":
                    # respond to discovery with address for client to connect
                    resp = json.dumps({"type": "host"}).encode("utf-8")
                    self.sock.sendto(resp, addr)
                    continue
                self.clients.add(addr)
            messages.append((addr, data))
        return messages

    @staticmethod
    def discover(
        timeout: float = 0.5,
        port: int = 50007,
        broadcast_address: str = "255.255.255.255",
        process_host=None,
    ) -> List[Tuple[str, int]]:
        """Broadcast a discovery packet and return responding server addresses."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.bind(("", 0))
        sock.settimeout(timeout)
        msg = json.dumps({"type": "discover"}).encode("utf-8")
        sock.sendto(msg, (broadcast_address, port))
        hosts: List[Tuple[str, int]] = []
        start = time.monotonic()
        while True:
            if process_host is not None:
                process_host()
            try:
                packet, addr = sock.recvfrom(4096)
            except socket.timeout:
                break
            try:
                data = json.loads(packet.decode("utf-8"))
            except json.JSONDecodeError:
                continue
            if data.get("type") == "host":
                hosts.append(addr)
            if time.monotonic() - start > timeout:
                break
        sock.close()
        return hosts

    @staticmethod
    def ping_node(
        addr: Tuple[str, int],
        timeout: float = 0.2,
        process_host=None,
    ) -> float | None:
        """Return round-trip latency to addr in seconds or None if unreachable."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(timeout)
        msg = json.dumps({"type": "ping"}).encode("utf-8")
        start = time.monotonic()
        try:
            sock.sendto(msg, addr)
            while True:
                if process_host is not None:
                    process_host()
                packet, _ = sock.recvfrom(4096)
                break
        except (socket.timeout, OSError):
            sock.close()
            return None
        sock.close()
        try:
            data = json.loads(packet.decode("utf-8"))
        except json.JSONDecodeError:
            return None
        if data.get("type") != "pong":
            return None
        return time.monotonic() - start

    @staticmethod
    def select_best_node(
        nodes: List[Tuple[str, int]],
        ping_func=None,
        timeout: float = 0.2,
    ) -> Tuple[str, int] | None:
        """Return the node with the lowest latency from a list of addresses."""
        if ping_func is None:
            ping_func = lambda n: NetworkManager.ping_node(n, timeout)
        best = None
        best_latency = float("inf")
        for node in nodes:
            latency = ping_func(node)
            if latency is not None and latency < best_latency:
                best = node
                best_latency = latency
        return best
