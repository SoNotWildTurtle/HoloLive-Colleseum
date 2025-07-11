import json
import socket
import time
from typing import Any, List, Tuple, Dict
import hmac
import hashlib

from .holographic_compression import compress_packet, decompress_packet

from .state_sync import StateSync

from .node_registry import add_node, load_nodes
from .node_registry import prune_nodes


class NetworkManager:
    """Simple UDP networking manager for multiplayer.

    Hosts respond to broadcast discovery packets so clients can automatically
    find available games on the local network. Router nodes keep track of game
    hosts **and** individual clients so the mesh knows which players are online
    at any moment.
    """

    def __init__(
        self,
        host: bool = False,
        address: Tuple[str, int] = ("", 50007),
        secret: bytes | None = None,
        encrypt_key: bytes | None = None,
    ) -> None:
        self.host = host
        self.address = address
        self.secret = secret
        self.encrypt_key = encrypt_key
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
        self._reliable_seq = 0
        self._pending_acks: dict[
            Tuple[Tuple[str, int], int], tuple[bytes, float, int, int]
        ] = {}
        self.ack_timeout = 0.2

    def _sign(self, msg: dict[str, Any]) -> str:
        raw = json.dumps(msg, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hmac.new(self.secret or b"", raw, hashlib.sha256).hexdigest()

    def _encode(self, msg: dict[str, Any]) -> bytes:
        if self.secret is not None:
            msg = msg.copy()
            msg["sig"] = self._sign(msg)
        return compress_packet(msg, key=self.encrypt_key)

    def _decode(self, data: bytes) -> dict[str, Any] | None:
        msg = decompress_packet(data, key=self.encrypt_key)
        if msg is None:
            return None
        if self.secret is not None:
            sig = msg.pop("sig", None)
            if sig is None or not hmac.compare_digest(self._sign(msg), sig):
                return None
        return msg

    def broadcast_announce(self, nodes: List[Tuple[str, int]] | None = None) -> None:
        """Broadcast our presence to known nodes."""
        if nodes is None:
            nodes = load_nodes()
        msg = self._encode({"type": "announce"})
        for node in nodes:
            try:
                self.sock.sendto(msg, tuple(node))
            except OSError:
                pass

    def register_game(self, nodes: List[Tuple[str, int]] | None = None) -> None:
        """Register this host with router nodes so players can find the game."""
        if nodes is None:
            nodes = load_nodes()
        msg = self._encode({"type": "register"})
        for node in nodes:
            try:
                self.sock.sendto(msg, tuple(node))
            except OSError:
                pass

    def register_client(self, nodes: List[Tuple[str, int]] | None = None) -> None:
        """Register this client with router nodes for discovery."""
        if nodes is None:
            nodes = load_nodes()
        msg = self._encode({"type": "client_join"})
        for node in nodes:
            try:
                self.sock.sendto(msg, tuple(node))
            except OSError:
                pass

    def refresh_nodes(self) -> None:
        """Prune unreachable nodes from the registry."""
        prune_nodes(lambda n: NetworkManager.ping_node(n, timeout=self.ack_timeout))

    def broadcast_games(self, nodes: List[Tuple[str, int]] | None = None) -> None:
        """Share our current game list with other nodes."""
        if not self.host:
            return
        if nodes is None:
            nodes = load_nodes()
        payload = self._encode({"type": "games_update", "games": list(self.games)})
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
        payload = self._encode({"type": "clients_update", "clients": list(self.live_clients)})
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
        secret: bytes | None = None,
    ) -> List[Tuple[str, int]]:
        """Ask a router node for known game hosts."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(timeout)
        enc = NetworkManager(secret=secret)
        msg = enc._encode({"type": "find"})
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
            data = enc._decode(packet)
            if data is None:
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
        secret: bytes | None = None,
    ) -> List[Tuple[str, int]]:
        """Ask a router node for known live clients."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(timeout)
        enc = NetworkManager(secret=secret)
        msg = enc._encode({"type": "list_clients"})
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
            data = enc._decode(packet)
            if data is None:
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
        payload = self._encode(self._sync.encode(data))
        if self.host:
            for client in list(self.clients):
                try:
                    self.sock.sendto(payload, client)
                except OSError:
                    pass
        else:
            self.sock.sendto(payload, self.address)

    def send_reliable(
        self,
        data: dict[str, Any],
        addr: Tuple[str, int] | None = None,
        max_retries: int = 5,
        importance: int = 1,
    ) -> None:
        """Send a packet that will be resent until acknowledged.

        ``importance`` controls how quickly resends occur and how many
        attempts are made. Higher values mean more frequent retries.
        """
        self._reliable_seq += 1
        seq = self._reliable_seq
        packet = data.copy()
        packet["reliable"] = True
        packet["seq"] = seq
        payload = self._encode(packet)
        if addr is None:
            dests = list(self.clients) if self.host else [self.address]
        else:
            dests = [addr]
        now = time.monotonic()
        for dest in dests:
            try:
                self.sock.sendto(payload, dest)
                self._pending_acks[(dest, seq)] = (
                    payload,
                    now,
                    max_retries * importance,
                    importance,
                )
            except OSError:
                pass

    def process_reliable(self) -> None:
        """Resend any unacknowledged reliable packets."""
        now = time.monotonic()
        for key, (payload, sent, retries, importance) in list(
            self._pending_acks.items()
        ):
            if now - sent < self.ack_timeout / importance:
                continue
            addr, seq = key
            if retries <= 0:
                del self._pending_acks[key]
                continue
            try:
                self.sock.sendto(payload, addr)
                self._pending_acks[key] = (
                    payload,
                    now,
                    retries - 1,
                    importance,
                )
            except OSError:
                del self._pending_acks[key]

    def poll(self) -> List[Tuple[Tuple[str, int], dict[str, Any]]]:
        messages = []
        while True:
            try:
                packet, addr = self.sock.recvfrom(4096)
            except BlockingIOError:
                break
            data = self._decode(packet)
            if data is None:
                continue
            msg_type = data.get("type")
            if msg_type == "ack":
                self._pending_acks.pop((addr, data.get("seq")), None)
                continue
            if data.get("reliable") and "seq" in data:
                ack = self._encode({"type": "ack", "seq": data["seq"]})
                self.sock.sendto(ack, addr)
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
                resp = self._encode({"type": "games", "games": list(self.games)})
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
                resp = self._encode({"type": "clients", "clients": list(self.live_clients)})
                self.sock.sendto(resp, addr)
                continue
            if msg_type == "ping":
                # reply with a pong for latency checks
                resp = self._encode({"type": "pong"})
                self.sock.sendto(resp, addr)
                continue
            if self.host:
                if msg_type == "discover":
                    # respond to discovery with address for client to connect
                    resp = self._encode({"type": "host"})
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
        secret: bytes | None = None,
    ) -> List[Tuple[str, int]]:
        """Broadcast a discovery packet and return responding server addresses."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.bind(("", 0))
        sock.settimeout(timeout)
        enc = NetworkManager(secret=secret)
        msg = enc._encode({"type": "discover"})
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
            data = enc._decode(packet)
            if data is None:
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
        secret: bytes | None = None,
    ) -> float | None:
        """Return round-trip latency to addr in seconds or None if unreachable."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(timeout)
        enc = NetworkManager(secret=secret)
        msg = enc._encode({"type": "ping"})
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
            data = enc._decode(packet)
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
