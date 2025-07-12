# Hololive Coliseum
Prototype platform fighter featuring Hololive Vtubers.
All playable characters extend a common `PlayerCharacter` class providing
movement, combat actions and resource tracking. The roster currently includes
twenty selectable characters displayed in a grid on the character select screen.
The repository goals are detailed in [docs/GOALS.md](docs/GOALS.md).
Story mode chapters are outlined in [docs/DEV_PLAN_STORY.md](docs/DEV_PLAN_STORY.md).
Networking details live in [docs/DEV_PLAN_NETWORK.md](docs/DEV_PLAN_NETWORK.md).

# Hololive Coliseum
Prototype platform fighter featuring Hololive Vtubers.
All playable characters extend a common `PlayerCharacter` class providing
movement, combat actions and resource tracking. The roster currently includes
twenty selectable characters displayed in a grid on the character select screen.
The repository goals are detailed in [docs/GOALS.md](docs/GOALS.md).
Story mode chapters are outlined in [docs/DEV_PLAN_STORY.md](docs/DEV_PLAN_STORY.md).
Networking details live in [docs/DEV_PLAN_NETWORK.md](docs/DEV_PLAN_NETWORK.md).

# HoloLive Coliseum
Prototype platform fighter featuring Hololive Vtubers.



## Asset Placeholders
The repository references simple placeholder images and a sound effect so the game runs without additional downloads. The PNG and WAV files are not included.

## Asset Placeholders
The repository references simple placeholder images and a sound effect so the game runs without additional downloads. The PNG and WAV files are not included.

Directories
- `SavedGames/`
- `Images/`
- `sounds/`
The `SavedGames` folder stores settings in `settings.json`. Selecting "Wipe Saves" from the settings menu clears this directory.
If the folder is missing, it will be recreated automatically the next time settings are saved.
The file also tracks your best survival time and high score so far.

The `SavedGames` folder stores settings in `settings.json`. Selecting "Wipe Saves" from the settings menu clears this directory.
If the folder is missing, it will be recreated automatically the next time settings are saved.

The `SavedGames` folder stores settings in `settings.json`. Selecting "Wipe
saves" from the settings menu clears this directory.


Images (PNGs)
```
./Images/Watson_Amelia_right.png
./Images/Watson_Amelia_left.png
./Images/Gawr_Gura_right.png
./Images/Gawr_Gura_left.png
./Images/Ninomae_Inanis_right.png
./Images/Ninomae_Inanis_left.png
./Images/Takanashi_Kiara_right.png
./Images/Takanashi_Kiara_left.png
./Images/Mori_Calliope_right.png
./Images/Mori_Calliope_left.png
./Images/Ceres_Fauna_right.png
./Images/Ceres_Fauna_left.png
./Images/Ouro_Kronii_right.png
./Images/Ouro_Kronii_left.png
./Images/IRyS_right.png
./Images/IRyS_left.png
./Images/Nanashi_Mumei_right.png
./Images/Nanashi_Mumei_left.png
./Images/Hakos_Baelz_right.png
./Images/Hakos_Baelz_left.png
./Images/Shirakami_Fubuki_right.png
./Images/Shirakami_Fubuki_left.png
./Images/Sakura_Miko_right.png
./Images/Sakura_Miko_left.png
./Images/Minato_Aqua_right.png
./Images/Minato_Aqua_left.png
./Images/Usada_Pekora_right.png
./Images/Usada_Pekora_left.png
./Images/Houshou_Marine_right.png
./Images/Houshou_Marine_left.png
./Images/Hoshimachi_Suisei_right.png
./Images/Hoshimachi_Suisei_left.png
./Images/Nakiri_Ayame_right.png
./Images/Nakiri_Ayame_left.png
./Images/Shirogane_Noel_right.png
./Images/Shirogane_Noel_left.png
./Images/Shiranui_Flare_right.png
./Images/Shiranui_Flare_left.png
./Images/Oozora_Subaru_right.png
./Images/Oozora_Subaru_left.png
./Images/character_right.png
./Images/character_left.png
./Images/enemy_right.png
./Images/enemy_left.png
./Images/boss_right.png
./Images/boss_left.png
./Images/map_default.png
./Images/chapter1.png

./Images/chapter2.png
./Images/chapter3.png
./Images/chapter4.png
./Images/chapter5.png
./Images/chapter6.png
./Images/chapter7.png
./Images/chapter8.png
./Images/chapter9.png
./Images/chapter10.png
./Images/chapter11.png
./Images/chapter12.png
./Images/chapter13.png
./Images/chapter14.png
./Images/chapter15.png
./Images/chapter16.png
./Images/chapter17.png
./Images/chapter18.png
./Images/chapter19.png
./Images/chapter20.png

```

Audio Tracks
(no audio files included)

## Running the Prototype

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Launch the game:
   ```bash
   python -m hololive_coliseum
   ```

The current prototype includes a basic player with gravity, health and mana bars,
a cyan splash screen leading to a simple menu system. Combat features melee attacks with **X**, projectile shooting with **Z**, blocking with **Shift**, a parry on **C**, and quick dodges with **Left Ctrl**. A low-gravity zone reduces gravity so jumps carry the player higher while a high-gravity zone increases gravity to limit movement. Spike traps now inflict damage on contact and icy patches lower friction. Enemies attempt to jump over these hazards.

Movement now uses acceleration and friction for smoother platforming.
Menu navigation now includes character, map, and chapter selection screens with
grid layouts and **Back** buttons for easy navigation. The map selector displays
tiles in the same 5×4 grid used for characters. During offline multiplayer character
selection a **"Press J to join"** prompt allows additional local players to join,
 and an **Add AI Player** option lets you fill extra slots with simple bots in
either solo or multiplayer. A **Difficulty** entry cycles between Easy,
Normal and Hard to tune AI behavior. Selected AI players now spawn as enemies that
chase the human player. Enemy AI adjusts reaction time and attack frequency
depending on difficulty, using projectiles and melee swings when near. They will also dodge incoming shots on higher levels. Projectiles and melee attacks damage enemies on contact, and enemies hurt the player when touching them. Press **V** to use Gura's special trident attack,
Watson's time-dash, Ina's tentacle grapple, Kiara's fiery dive, Calliope's returning scythe, Fauna's healing field, Fubuki's freezing shard, Miko's piercing beam, Mumei's slowing flock, Kronii's extended parry, IRyS's crystal shield, Baelz's chaos effect, or other character abilities during gameplay. Projectiles can be aimed with the mouse and the special attack
fires an exploding shot. Powerups periodically spawn to restore health or mana
and a simple life counter, level timer and enemy score are displayed. A revamped **Settings**
menu features key and controller binding editors, volume adjustments,
 window-size toggling, and a save-wipe option so preferences persist across
sessions. A new **Node Settings** entry lets advanced users start hosting a
blockchain node or stop hosting at any time. An **Accounts** submenu allows
registering or deleting the current player account. Press **Esc** during
gameplay to open a pause menu with options to resume or return to the main
menu. Menus are outlined with a teal border for a cleaner look. The main menu
also features **How to Play** and **Credits** options describing the controls
and acknowledging contributors. Selecting
multiplayer now leads
to a lobby screen listing every joined human and AI player before the map menu
appears.
Losing all lives transitions to a **Game Over** screen that shows your time
survived, total score, and the best run and high score. After a short pause the screen reveals
**Play Again** and **Main Menu** buttons. Play Again jumps back to the character
selection so you can quickly start another run.
Defeating all enemies or surviving the level timer displays a **Victory** screen
with the same summary, including your best time and high score, and a brief delay before the options appear.

A new **Records** entry on the main menu shows your best survival time and high
score so far. Use it to track progress across multiple runs.
and a simple life counter and level timer are displayed. A revamped **Settings**
menu features key and controller binding editors, volume adjustments,
 window-size toggling, and a save-wipe option so preferences persist across
 sessions. A new **Node Settings** entry lets advanced users start hosting a
 blockchain node or stop hosting at any time. An **Accounts** submenu allows
 registering or deleting the current player account. Selecting multiplayer now leads
 to a lobby screen listing every joined human and AI player before the map menu
 appears.

### Story Mode
The single-player campaign follows Gura's growth from rookie idol to battle-tested hero.
Twenty chapter icons appear in the chapter select menu, each representing a new location and challenge.
Selecting an icon loads its corresponding map using the placeholder images listed above.
a cyan splash screen leading to a simple menu system. Combat features melee attacks
with **X**, projectile shooting with **Z**, blocking with **Shift**, and a parry on
**C**. A low-gravity zone reduces jump speed.
Menu navigation now includes character, map, and chapter selection screens with
simple previews. Multiplayer can be played offline or online, chosen from a new
multiplayer mode menu. Press **V** to use Gura's special trident attack during
gameplay. A new **Settings** menu allows adjusting key bindings, window size,
and volume, as well as wiping saved data.

Additional characters, maps, and features will be introduced over time.

### Networking Prototype
The package now contains a `NetworkManager` module that uses UDP sockets for
lightweight communication. Hosts answer broadcast discovery packets so clients
can automatically locate games on the local network. A separate
`node_registry` module stores known server addresses in `SavedGames/nodes.json`
alongside a small set of built-in nodes. When a host starts it registers its
address in this file and can broadcast an `announce` packet to share its
location with other nodes. Clients maintain their own registry and add entries
whenever they receive an `announce` message. When connecting online the game
 pings all known nodes and chooses the one with the lowest latency. Nodes also
 act as lightweight routers: hosts register their match with nearby nodes and
 clients query those routers to receive a list of available games. Router nodes
 exchange `games_update` packets so each peer keeps the same set of available
 matches and additionally share `clients_update` packets so each node knows
 which users are currently online. State updates include a sequence number and
 only transmit fields that changed using the lightweight `StateSync` delta
system so packets remain small. When a shared secret is configured, packets
also include an HMAC signature so nodes can discard tampered data. The menus
include an online versus offline
multiplayer option to choose whether to connect to discovered nodes or play
locally.
Packets are compressed using a holographic lithography method. Each message is
converted to a pointcloud and split into two base64 strings for transmission,
then reconstructed on receipt to keep bandwidth low. The encoded pointcloud
includes a SHA256 digest so corrupted data is ignored. Packets may also be
XOR-encrypted with a shared key for an additional layer of privacy.
Critical packets can be marked **reliable** so the sender will resend them
until an acknowledgement is received, ensuring important updates are not lost
even over an unreliable connection. Reliable packets now include an
``importance`` value that increases the resend rate and retry count for
critical messages.
Nodes periodically prune unreachable peers from the registry so discovery
remains accurate even as servers appear and disappear.
Starting a node from the **Node Settings** menu turns the game into a host that
shares blockchain updates and discovers peers to form an IP mesh. The same menu
offers a **Stop Node** option to revert to client-only mode.

### Game History Blockchain
Every completed online match is recorded in a lightweight blockchain stored in
`SavedGames/chain.json`. Each block contains the game ID, participating
usernames, winner and an optional wager amount. Winners "mine" a block when a
match ends and the block is shared with other nodes. Balances are tracked in
`balances.json` so players can bet currency on matches. Utility functions allow
searching the chain by game ID or user ID for features like leaderboards and
friends lists. A helper `get_balance(user_id)` returns the currency total for
any account. The blockchain can be verified for tampering and merged with
longer chains received from peers so all nodes share the same history. Game
records are only accepted if every player has a registered account so invalid
user IDs cannot be added.

Messages between players can also be stored in the chain. Each account
registers a public key and an access level (user, mod or admin). Accounts can
be removed later if needed. When a
message is sent, it is encrypted with a random key that is wrapped twice:
once with the recipient's public key and once with the admin key. This keeps
chats private while still allowing moderators to decrypt abusive messages using
the mixed key.

## Project Structure

This repository contains several directories and Python modules that make up the
prototype.  The key paths are listed below with a short description of how they
interact:

Directories
| Path | Purpose |
| ---- | ------- |
| `hololive_coliseum/` | Core game modules including the main loop, player classes and helpers. |
| `docs/` | Development notes, goals and design plans. |
| `tests/` | Pytest suite covering gameplay and systems. |
| `Images/` | Placeholder sprites loaded by the game menus. |
| `sounds/` | Placeholder location for sound effects (empty in repo). |
| `SavedGames/` | Created at runtime to store `settings.json`. |

Important files
| Path | Called From | Calls |
| ---- | ---------- | ----- |
| `main.py` | Entry point script executed directly. | `hololive_coliseum.game.main` |
| `hololive_coliseum/__init__.py` | Imported when using `hololive_coliseum` as a package. | Re-exports main classes from submodules. |
| `hololive_coliseum/game.py` | Invoked by `main.py` or `python -m hololive_coliseum`. | Coordinates gameplay, settings and networking. |
| `hololive_coliseum/menus.py` | Imported by `game.py`. | Renders splash and option menus. |
| `hololive_coliseum/player.py` | Used by `game.py` to create players and enemies. | Imports `physics`, `projectile`, `melee_attack`. |
| `hololive_coliseum/projectile.py` | Instantiated from `player.py` or `game.py`. | None (pure sprite logic). |
| `hololive_coliseum/melee_attack.py` | Spawned from `player.py`. | None. |
| `hololive_coliseum/hazards.py` | Loaded by `game.py` to place spike traps and ice zones. | None. |
| `hololive_coliseum/gravity_zone.py` | Used in `game.py` to create low‑gravity areas. | None. |
| `hololive_coliseum/powerup.py` | Spawned by `game.py` during matches. | None. |
| `hololive_coliseum/network.py` | Created by `game.py` when online play is chosen. | Uses UDP sockets for discovery and state. |
| `hololive_coliseum/state_sync.py` | Helper for delta-compressed state updates with sequence numbers. | None. |
| `hololive_coliseum/holographic_compression.py` | Encodes packets into pointcloud base64 pairs with optional XOR encryption and digest verification. | None. |
| `hololive_coliseum/node_registry.py` | Shared helper for tracking known server nodes. | Read/writes `SavedGames/nodes.json`. |
| `hololive_coliseum/save_manager.py` | Called by `game.py` and tests to persist settings. | Reads/writes JSON in `SavedGames`. |
| `hololive_coliseum/accounts.py` | Used by the blockchain and tests. | Stores public keys and access levels and can delete accounts. |

The tests import the modules above to verify behavior. Development documents in
`docs/` describe goals and planning for future work.

can automatically locate games on the local network. The menus include an
online versus offline multiplayer option to select whether to connect to other
discovered nodes or play locally.
