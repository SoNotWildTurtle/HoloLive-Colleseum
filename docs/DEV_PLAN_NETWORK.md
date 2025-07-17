# Networking Plan

The prototype uses a simple UDP based system for minimal latency. Discovery works
through broadcast packets so clients can locate hosts on the local network. To
expand beyond a single LAN, the `node_registry` module keeps a list of known
servers in `SavedGames/nodes.json`. Each host registers itself and sends an
`announce` packet to other nodes. When a node receives an announcement it adds
the sender to its registry. This creates a lightweight mesh of user-hosted nodes
without central coordination.
Clients ping all known nodes at startup and pick the one with the lowest
round-trip latency to use for online sessions. In addition to discovery,
nodes maintain a list of registered game hosts. When a player starts a match
they send a `register` packet to nearby nodes. Other clients can issue `find`
requests to any node and receive the list of currently available games. This
DNS-like approach lets user-hosted nodes route players to each other without a
central server. It also helps clients choose the closest peer when multiple
hosts are available.
Router nodes also share their game lists with each other using `games_update`
packets so the mesh stays synchronized even as matches come and go. They
likewise synchronize active clients by broadcasting `clients_update` packets
whenever a player joins or leaves a node. This will make it easier to scale the
prototype toward a larger MMO-style environment where servers need to know which
players are online.
State updates exchanged during gameplay carry a sequence number and only include
fields that changed since the previous update. The `StateSync` helper computes
these diffs so messages remain tiny and reduce network overhead.

Each packet now includes an HMAC signature when a shared secret is configured.
Nodes verify the signature before processing data so malicious or malformed
packets are discarded. This lightweight authentication helps secure the mesh
without adding heavy encryption.
To further reduce bandwidth usage, packets are compressed using a holographic
lithography technique. Messages are converted to a pointcloud with four anchor
points marking `(0,0,1)`, `(0,0,0)`, `(1,1,1)` and `(1,1,0)` in cyan, white,
black and red. Anchors now store a virtual size, luminosity and black/white
level so the pointcloud can be reconstructed at multiple detail layers. The
data is split into two base64 strings and recombined on receipt. The encoded bytes
 include a SHA256 digest so the receiver can verify integrity before decoding.
 If an `encrypt_key` is supplied, the pointcloud bytes are XOR encrypted so
 data in transit remains private even over unsecured networks.
Important control packets can also be sent in **reliable** mode. When enabled
the sender stores a copy and will resend it until an `ack` message confirms the
receiver got it. Each reliable packet includes an integer *importance* value so
critical packets are retried more aggressively. Higher importance reduces the
wait between resends and increases the total number of attempts. This ensures
registration and blockchain updates are delivered even if a packet is dropped.
Nodes periodically prune entries from `nodes.json` if they no longer respond to
a ping so discovery remains accurate over time.
Players can toggle hosting from the **Node Settings** menu. Starting a node
spawns a `NetworkManager` in host mode, registers the address, broadcasts an
`announce` packet and begins sharing new blockchain blocks. Choosing "Stop Node"
closes the socket and the game falls back to client-only behavior.

Game results are stored in a lightweight blockchain. When an online match
finishes the winner "mines" a block containing the participant IDs and optional
bet amount. The block is written to `chain.json` and shared with other nodes via
the announce system. Player balances in `balances.json` track wagers and can be
synchronized in the same way.
Remote chains can be verified and merged so all nodes eventually share the
longest valid history.

Nodes also broadcast ``records_update`` packets containing their best survival
time and high score. Peers merge these records so leaderboards stay consistent
across the mesh.
Clients can volunteer to act as relay nodes by enabling the *Latency Helper*
setting. Router nodes maintain a list of these relays and share them with peers.
Packets may be forwarded through a relay when it offers a faster path between
two players, keeping latency low even across distant networks.

Future work will experiment with rollback netcode and more efficient state
synchronization once the gameplay loop stabilizes.
