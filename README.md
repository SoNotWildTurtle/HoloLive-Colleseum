# Hololive Coliseum
Prototype platform fighter featuring Hololive Vtubers.
All playable characters extend a common `PlayerCharacter` class providing
movement, combat actions and resource tracking.
The repository goals are detailed in [docs/GOALS.md](docs/GOALS.md).
Story mode chapters are outlined in [docs/DEV_PLAN_STORY.md](docs/DEV_PLAN_STORY.md).
Networking details live in [docs/DEV_PLAN_NETWORK.md](docs/DEV_PLAN_NETWORK.md).


## Asset Placeholders
The repository references simple placeholder images and a sound effect so the game runs without additional downloads. The PNG and WAV files are not included.

Directories
- `SavedGames/`
- `Images/`
- `sounds/`
The `SavedGames` folder stores settings in `settings.json`. Selecting "Wipe Saves" from the settings menu clears this directory.
If the folder is missing, it will be recreated automatically the next time settings are saved.

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
a cyan splash screen leading to a simple menu system. Combat features melee attacks with **X**, projectile shooting with **Z**, blocking with **Shift**, and a parry on **C**. A low-gravity zone reduces jump speed. Spike traps now inflict damage on contact and icy patches lower friction. Enemies attempt to jump over these hazards.
Movement now uses acceleration and friction for smoother platforming.
Menu navigation now includes character, map, and chapter selection screens with
placeholder icons generated at runtime. During offline multiplayer character
selection a **"Press J to join"** prompt allows additional local players to join,
 and an **Add AI Player** option lets you fill extra slots with simple bots in
 either solo or multiplayer. A **Difficulty** entry cycles between Easy,
 Normal and Hard to tune AI behavior. Selected AI players now spawn as enemies that
  chase the human player. Enemy AI adjusts reaction time and attack frequency
  depending on difficulty, using projectiles and melee swings when near. Projectiles and melee attacks damage enemies on
 contact, and enemies hurt the player when touching them. Press **V** to use Gura's special trident attack,
Watson's time-dash, Ina's tentacle grapple, Fubuki's freezing shard, or other character abilities during gameplay. Projectiles can be aimed with the mouse and the special attack
fires an exploding shot. Powerups periodically spawn to restore health or mana
and a simple life counter and level timer are displayed. A revamped **Settings**
menu features key and controller binding editors, volume adjustments,
window-size toggling, and a save-wipe option so preferences persist across
sessions. A new **Node Settings** entry lets advanced users start hosting a
blockchain node or stop hosting at any time.

### Story Mode
The single-player campaign follows Gura's growth from rookie idol to battle-tested hero.
Twenty chapter icons appear in the chapter select menu, each representing a new location and challenge.
Selecting an icon loads its corresponding map using the placeholder images listed above.
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
 system so packets remain small. The menus include an online versus offline
 multiplayer option to choose whether to connect to discovered nodes or play
 locally.
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
friends lists.

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
| `hololive_coliseum/game.py` | Invoked by `main.py` or `python -m hololive_coliseum`. | Coordinates menus, gameplay and settings management. |
| `hololive_coliseum/player.py` | Used by `game.py` to create players and enemies. | Imports `physics`, `projectile`, `melee_attack`. |
| `hololive_coliseum/projectile.py` | Instantiated from `player.py` or `game.py`. | None (pure sprite logic). |
| `hololive_coliseum/melee_attack.py` | Spawned from `player.py`. | None. |
| `hololive_coliseum/hazards.py` | Loaded by `game.py` to place spike traps and ice zones. | None. |
| `hololive_coliseum/gravity_zone.py` | Used in `game.py` to create low‑gravity areas. | None. |
| `hololive_coliseum/powerup.py` | Spawned by `game.py` during matches. | None. |
| `hololive_coliseum/network.py` | Created by `game.py` when online play is chosen. | Uses UDP sockets for discovery and state. |
| `hololive_coliseum/state_sync.py` | Helper for delta-compressed state updates with sequence numbers. | None. |
| `hololive_coliseum/node_registry.py` | Shared helper for tracking known server nodes. | Read/writes `SavedGames/nodes.json`. |
| `hololive_coliseum/save_manager.py` | Called by `game.py` and tests to persist settings. | Reads/writes JSON in `SavedGames`. |

The tests import the modules above to verify behaviour. Development documents in
`docs/` describe goals and planning for future work.
