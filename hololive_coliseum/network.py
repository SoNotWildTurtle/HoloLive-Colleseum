import json
import socket
import time
from typing import Any, List, Tuple


class NetworkManager:
    """Simple UDP networking manager for multiplayer.

    Hosts respond to broadcast discovery packets so clients can
    automatically find available games on the local network.
    """

    def __init__(self, host: bool = False, address: Tuple[str, int] = ("", 50007)) -> None:
        self.host = host
        self.address = address
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setblocking(False)
        if host:
            self.sock.bind(address)
            self.clients: set[Tuple[str, int]] = set()
        else:
            self.sock.bind(("", 0))

        # allow broadcast for discovery
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
    def send_state(self, data: dict[str, Any]) -> None:
        payload = json.dumps(data).encode("utf-8")
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
            if self.host:
                if data.get("type") == "discover":
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
