# Networking Plan

The prototype uses a simple UDP based system for minimal latency. Discovery works
through broadcast packets so clients can locate hosts on the local network. To
expand beyond a single LAN, the `node_registry` module keeps a list of known
servers in `SavedGames/nodes.json`. Each host registers itself and sends an
`announce` packet to other nodes. When a node receives an announcement it adds
the sender to its registry. This creates a lightweight mesh of user hosted nodes
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
Players can toggle hosting from the **Node Settings** menu. Starting a node
spawns a `NetworkManager` in host mode, registers the address, broadcasts an
`announce` packet and begins sharing new blockchain blocks. Choosing "Stop Node"
closes the socket and the game falls back to client-only behavior.

Game results are stored in a lightweight blockchain. When an online match
finishes the winner "mines" a block containing the participant IDs and optional
bet amount. The block is written to `chain.json` and shared with other nodes via
the announce system. Player balances in `balances.json` track wagers and can be
synchronized in the same way.

Future work will experiment with rollback netcode and more efficient state
synchronization once the gameplay loop stabilizes.
