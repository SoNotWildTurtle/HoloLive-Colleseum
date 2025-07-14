# Hololive Coliseum
Prototype platform fighter featuring Hololive VTubers.
All playable characters extend a common `PlayerCharacter` class providing movement,
combat actions and resource tracking. The roster currently includes twenty-one
selectable characters displayed in a grid on the character select screen.
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
The file also tracks your best survival time and high score so far.

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
./Images/Tokino_Sora_right.png
./Images/Tokino_Sora_left.png
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
 a cyan splash screen leading to a simple menu system. Combat features melee attacks with **X**, projectile shooting with **Z**, blocking with **Shift**, a parry on **C**, and quick dodges with **Left Ctrl**. A low-gravity zone reduces gravity so jumps carry the player higher while a high-gravity zone increases gravity to limit movement. Spike traps now inflict damage on contact, icy patches lower friction and lava pits deal damage over time. Enemies attempt to jump over these hazards.
Movement now uses acceleration and friction for smoother platforming.
Characters can also perform a double jump before landing for extra mobility.
Menu navigation now includes character, map, and chapter selection screens with
grid layouts and **Back** buttons for easy navigation. The map selector displays
tiles in the same 5×4 grid used for characters. During offline multiplayer character
selection a **"Press J to join"** prompt allows additional local players to join,
 and an **Add AI Player** option lets you fill extra slots with simple bots in
 either solo or multiplayer. A **Difficulty** entry cycles between Easy,
Normal and Hard to tune AI behavior. Selected AI players now spawn as enemies that
  chase the human player. Enemy AI adjusts reaction time and attack frequency
 depending on difficulty, using projectiles and melee swings when near. They will also dodge incoming shots on higher levels. Projectiles and melee attacks damage enemies on contact, and enemies hurt the player when touching them. Press **V** to use Gura's special trident attack,
Watson's time-dash, Ina's tentacle grapple, Kiara's fiery dive, Calliope's returning scythe, Fauna's healing field, Fubuki's freezing shard, Miko's piercing beam, Mumei's slowing flock, Kronii's extended parry, IRyS's crystal shield, Baelz's chaos effect, Aqua's water blast, Pekora's explosive carrot, Marine's anchor boomerang, Suisei's piercing star, Ayame's swift dash, Noel's ground slam, Flare's flame burst, Subaru's stunning blast, Sora's uplifting melody, or other character abilities during gameplay. Projectiles can be aimed with the mouse and the special attack
fires an exploding shot. A status effect manager tracks temporary effects such as freezing or slowing enemies when these abilities land. A skill manager coordinates ability cooldowns so each character registers its unique special once. An **AIManager** directs enemy behavior while an **NPCManager** organizes enemy and ally groups. An **AllyManager** keeps friendly NPCs active. Powerups periodically spawn to restore health or mana, and an **InventoryManager** stores collected items, while a **QuestManager** tracks objectives and an **AchievementManager** records milestones. A simple life counter, level timer and enemy score are displayed. A revamped **Settings**
menu features key and controller binding editors managed by a **KeybindManager**, volume adjustments,
 window-size toggling, an option to toggle an FPS counter, and a save-wipe option
 so preferences persist across sessions. You can also reset your best time and
 score. A new **Node Settings** entry lets advanced users start hosting a
blockchain node or stop hosting at any time. An **Accounts** submenu allows
registering or deleting the current player account. Press **Esc** during
gameplay to open a pause menu with options to resume or return to the main
menu. Press **Enter** to open an in-game chat box and coordinate with other
players. Menus are outlined with a teal border for a cleaner look. The main menu
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
score so far. When online, nodes broadcast these numbers so every player sees
the latest records across the mesh.

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
system so packets remain small. When a shared secret is configured, packets
also include an HMAC signature so nodes can discard tampered data. The menus
include an online versus offline
multiplayer option to choose whether to connect to discovered nodes or play
locally.
Packets are compressed using a holographic lithography method. Each message is
converted to a pointcloud and split into two base64 strings for transmission,
then reconstructed on receipt to keep bandwidth low. The encoded pointcloud
contains four color-coded anchor points -- black at `(0,0,0)`, red at `(1,0,0)`,
white at `(1,1,1)` and cyan at `(1,0,1)` -- so the receiver can determine the
pointcloud bounds before decoding. The encoded pointcloud
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
Advanced users can also enable a **Latency Helper** option in Node Settings.
When active, the client announces itself as a relay so other players can route
traffic through the lowest‑latency path. Router nodes share their available
relays and clients may send packets via these helpers if it shortens the route.
Whenever a new best time or high score is achieved, the node broadcasts a
``records_update`` packet so peers can merge the latest numbers into their own
settings.

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
| `hololive_coliseum/hazards.py` | Loaded by `game.py` to place spike traps, ice zones and lava pits. | None. |
| `hololive_coliseum/gravity_zone.py` | Used in `game.py` to create low‑gravity areas. | None. |
| `hololive_coliseum/powerup.py` | Spawned by `game.py` during matches. | None. |
| `hololive_coliseum/skill_manager.py` | Used by `player.py` to manage ability cooldowns. | None. |
| `hololive_coliseum/health_manager.py` | Provides health tracking helpers used by `player.py`. | None. |
| `hololive_coliseum/mana_manager.py` | Provides mana tracking helpers used by `player.py`. | None. |
| `hololive_coliseum/stats_manager.py` | Returns STR, DEX and other stats with temporary modifiers. | None. |
| `hololive_coliseum/experience_manager.py` | Tracks XP and levels up when thresholds are reached. | None. |
| `hololive_coliseum/equipment_manager.py` | Stores equipped items for each player. | None. |
| `hololive_coliseum/inventory_manager.py` | Tracks collected items. | None. |
| `hololive_coliseum/quest_manager.py` | Manages active quests and progress. | None. |
| `hololive_coliseum/achievement_manager.py` | Records unlocked achievements. | None. |
| `hololive_coliseum/keybind_manager.py` | Holds configurable key mappings. | None. |
| `hololive_coliseum/ai_manager.py` | Coordinates enemy decision making. | Used by `game.py` during play. |
| `hololive_coliseum/npc_manager.py` | Holds enemy and ally sprite groups. | Used by `game.py` to organize NPCs. |
| `hololive_coliseum/ally_manager.py` | Updates friendly NPCs that assist the player. | Called from `game.py` each frame. |
| `hololive_coliseum/menu_manager.py` | Tracks menu selection and navigation. | Used by `game.py` when handling menus. |
| `hololive_coliseum/game_state_manager.py` | Stores the current and previous game state. | Updated by `game.py` whenever the state changes. |
| `hololive_coliseum/network.py` | Created by `game.py` when online play is chosen. | Uses UDP sockets for discovery, state and record sharing. |
| `hololive_coliseum/state_sync.py` | Helper for delta-compressed state updates with sequence numbers. | None. |
| `hololive_coliseum/holographic_compression.py` | Encodes packets into pointcloud base64 pairs with optional XOR encryption and digest verification. | None. |
| `hololive_coliseum/node_registry.py` | Shared helper for tracking known server nodes. | Read/writes `SavedGames/nodes.json`. |
| `hololive_coliseum/save_manager.py` | Called by `game.py` and tests to persist settings. | Reads/writes JSON in `SavedGames` and merges record updates from peers. |
| `hololive_coliseum/accounts.py` | Used by the blockchain and tests. | Stores public keys and access levels and can delete accounts. |
| `hololive_coliseum/combat_manager.py` | Manages turn order and engagement logic. | None. |
| `hololive_coliseum/damage_manager.py` | Computes final damage after reductions. | None. |
| `hololive_coliseum/threat_manager.py` | Tracks threat values for AI targeting. | None. |
| `hololive_coliseum/loot_manager.py` | Generates loot from drop tables. | None. |
| `hololive_coliseum/buff_manager.py` | Applies buffs and debuffs using the status effect system. | None. |
| `hololive_coliseum/appearance_manager.py` | Stores selected skins per entity. | None. |
| `hololive_coliseum/animation_manager.py` | Tracks animation states and frames. | None. |
| `hololive_coliseum/name_manager.py` | Handles naming and renames for characters. | None. |
| `hololive_coliseum/session_manager.py` | Maintains login sessions to prevent duplicates. | None. |
| `hololive_coliseum/sync_manager.py` | Computes time offsets between clients. | None. |
| `hololive_coliseum/instance_manager.py` | Creates and destroys gameplay instances. | None. |
| `hololive_coliseum/patch_manager.py` | Records the current patch version. | None. |
| `hololive_coliseum/auth_manager.py` | Validates logins and issues tokens. | None. |
| `hololive_coliseum/cheat_detection_manager.py` | Flags suspicious behavior. | None. |
| `hololive_coliseum/ban_manager.py` | Maintains banned account list. | None. |
| `hololive_coliseum/data_protection_manager.py` | Provides simple XOR encryption. | None. |
| `hololive_coliseum/logging_manager.py` | Collects log events. | None. |
| `hololive_coliseum/ui_manager.py` | Tracks active UI elements. | None. |
| `hololive_coliseum/notification_manager.py` | Queues in-game notifications. | None. |
| `hololive_coliseum/input_manager.py` | Stores key and controller mappings. | None. |
| `hololive_coliseum/accessibility_manager.py` | Toggles colorblind modes and fonts. | None. |
| `hololive_coliseum/chat_manager.py` | Manages text chat messages and chat box state. | Used by `game.py` during matches. |
| `hololive_coliseum/voice_chat_manager.py` | Tracks users in voice channels. | None. |
| `hololive_coliseum/emote_manager.py` | Provides available emotes. | None. |
| `hololive_coliseum/sound_manager.py` | Plays sound effects and music. | None. |
| `hololive_coliseum/effect_manager.py` | Triggers particle effects. | None. |
| `hololive_coliseum/script_manager.py` | Loads and stores small scripts. | None. |
| `hololive_coliseum/localization_manager.py` | Provides basic text translation. | None. |
| `hololive_coliseum/resource_manager.py` | Caches loaded assets. | None. |
| `hololive_coliseum/cluster_manager.py` | Tracks nodes in a cluster. | None. |
| `hololive_coliseum/matchmaking_manager.py` | Groups players for matches. | None. |
| `hololive_coliseum/load_balancer_manager.py` | Chooses the least busy server. | None. |
| `hololive_coliseum/migration_manager.py` | Handles player transfers between servers. | None. |
| `hololive_coliseum/billing_manager.py` | Records purchases and subscriptions. | None. |
| `hololive_coliseum/ad_manager.py` | Manages in-game ads. | None. |
| `hololive_coliseum/api_manager.py` | Stores third-party API endpoints. | None. |
| `hololive_coliseum/support_manager.py` | Tracks support tickets. | None. |
| `hololive_coliseum/crafting_manager.py` | Handles crafting recipes. | None. |
| `hololive_coliseum/profession_manager.py` | Tracks profession XP and levels. | None. |
| `hololive_coliseum/trade_manager.py` | Manages item trades between players. | None. |
| `hololive_coliseum/economy_manager.py` | Stores global item prices. | None. |
| `hololive_coliseum/currency_manager.py` | Tracks player currency balances. | None. |
| `hololive_coliseum/title_manager.py` | Unlocks and sets active titles. | None. |
| `hololive_coliseum/reputation_manager.py` | Stores faction reputation. | None. |
| `hololive_coliseum/friend_manager.py` | Maintains the friends list. | None. |
| `hololive_coliseum/guild_manager.py` | Handles guild membership and ranks. | None. |
| `hololive_coliseum/mail_manager.py` | Sends and retrieves player mail. | None. |
| `hololive_coliseum/map_manager.py` | Stores available maps and the current one. | None. |
| `hololive_coliseum/environment_manager.py` | Tracks weather and other environment settings. | None. |
| `hololive_coliseum/spawn_manager.py` | Schedules NPC or item spawns. | None. |
| `hololive_coliseum/event_manager.py` | Records triggered world events. | None. |
| `hololive_coliseum/dungeon_manager.py` | Manages dungeon lockouts for players. | None. |
| `hololive_coliseum/housing_manager.py` | Stores player housing data. | None. |
| `hololive_coliseum/mount_manager.py` | Tracks mounts per player. | None. |
| `hololive_coliseum/pet_manager.py` | Maintains collectible pets. | None. |
| `hololive_coliseum/companion_manager.py` | Assigns companions to players. | None. |

The tests import the modules above to verify behavior. Development documents in
`docs/` describe goals and planning for future work.
