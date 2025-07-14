# Development Notes

## 2025-07-06
- Switched prototype to use Pygame for quick iteration.
- Implemented basic `Player` class with gravity, movement, and jumping.
- Added ground platform to the `Game` loop and drawing logic.
- Updated README project title and description.
- Added simple test verifying player falls under gravity.

## 2025-07-07
- Generated placeholder character sprites and a sound effect.
- Updated `Player` to load an image if provided.
- Player in the game now uses the Gawr Gura sprite.
- Documented assets in the README and ignored `SavedGames` folder.

## 2025-07-08
- Implemented projectile system and firing with Z key.
- Player tracks facing direction and cooldown for shooting.
- Added tests for projectile movement.
- Restored full placeholder asset list in README.

## 2025-07-09
- Added `GravityZone` sprite and integrated a low-gravity area in the stage.
- Player now adjusts gravity based on zone collisions.
- Created unit test for gravity zones and updated existing tests to initialize pygame.

## 2025-07-10
- Implemented health and mana system for the `Player`.
- Drawing routine now displays health and mana bars on screen.
- Projectiles consume mana when fired and fail if insufficient.
- Added tests covering damage, mana usage, and status bar drawing.

## 2025-07-11
- Added melee attack sprite and blocking mechanic to `Player`.
- Game loop now handles melee attacks with the **X** key.
- Updated README to document controls.

## 2025-07-12
- Implemented parry ability activated with the **C** key.
- Replaced splash prompt with a menu system to start a new game.
- Added navigation for game type, player count, character, and map selection.
- Updated tests to cover parry logic.

## 2025-07-13
- Introduced map and chapter selection screens with placeholder images.
- Added a unique trident special attack for Gura, triggered by **V**.
- Created tests covering the new special attack.

## 2025-07-14
- Added `NetworkManager` with simple UDP sockets for upcoming multiplayer.
- Documented networking prototype in README and exported manager in package.
- Added unit test verifying send/receive between client and host.

## 2025-07-15
- Implemented broadcast-based server discovery mirroring Hive-style detection.
- Added menu step to choose online or offline multiplayer.
- Updated tests for discovery and menu options.

## 2025-07-16
- Completed settings menu with dynamic volume display and a new key-binding
  editor.
- Added states for editing controls and saving changes on exit.
- Updated README accordingly.

## 2025-07-17
- Added placeholder icons for characters, maps and chapters so menus look nicer.
- Character selection now displays AI count and a "Press J to join" prompt for
  local multiplayer.
- Added ability to add AI players from the character menu.
## 2025-07-18
- Added controller binding menu and saving of bindings
- Projectiles now aim toward the mouse and Gura's special attack explodes
- Added simple powerup spawns, level timer, and life system

## 2025-07-19
- Fixed crash when `settings.json` contains invalid JSON
- Volume adjustments no longer raise errors if the mixer fails to initialize

## 2025-07-20
- `save_settings` now recreates the save directory if it was deleted.
- Cleaned up a comment about the low-gravity zone.
- Network tests close sockets to avoid resource warnings.

## 2025-07-21
- Added `WatsonPlayer` with a time-dash special attack.
- Game now creates the player when a level starts so character selection matters.

## 2025-07-22
- Extended goals list with short- and long-term sections.
- AI players selected in the menu now spawn as enemies that pursue the player.

## 2025-07-23
- Added projectile and melee collision detection so enemies take damage when hit.
- Updated goals and development plan to mention combat collisions.

## 2025-07-24
- Enemies now deal contact damage to the player.
- Updated goals and development plan accordingly.

## 2025-07-25
- Added a "Growing Up" storyline for single-player with twenty chapter icons.
- Updated menus to list all chapters and load placeholder images.

## 2025-07-26
- Introduced `InaPlayer` with a tentacle grapple special attack.
- Character list now includes Ninomae Ina'nis and chapter menu supports her image.
- Collision logic pulls enemies toward the player when grapple projectile hits.

## 2025-07-27
- Refactored `Player` into `PlayerCharacter` and updated character subclasses.
- Added difficulty selector (Easy/Normal/Hard) to character menu.
- Researched Smash Bros AI which scales reaction time and randomness by level; plan to mimic this behavior.

## 2025-07-28
- Implemented three AI tiers that vary reaction delay and aggression.
- Enemies now shoot and use melee attacks, marking their projectiles so
  collisions damage the player.
- Updated collision handling for these enemy attacks and added tests.

## 2025-07-29
- Added SpikeTrap and IceZone hazards with player and enemy interactions.
- Extended Enemy AI to jump over hazards when possible.
- Created placeholder subclasses for each Hololive member with unique specials.
- Updated development plan and goals accordingly and added new tests.

## 2025-07-30
- Added `FubukiPlayer` with an ice shard that slows enemies.
- Updated menus and image lists to include Shirakami Fubuki.
- Documented the new ability in the development plan and goals.

## 2025-07-31
- Added volume cycling when selecting the option in the settings menu.
- Documented project structure and file paths in README and notes.

## 2025-08-01
- Introduced a `node_registry` module storing known server addresses.
- NetworkManager now registers hosts and handles `announce` messages to build a
  mesh of user-hosted nodes.
- Added a networking plan document and updated development plans and README.

## 2025-08-02
- Added **Node Settings** menu with options to start or stop hosting a
  blockchain node.
- Starting a node creates a `NetworkManager` in host mode and broadcasts an
  `announce` message so other nodes discover it.
- Stopping closes the socket to disable hosting and return to client mode.

## 2025-08-03
- Added ping response handling in `NetworkManager` and a helper to measure
  latency to other nodes.
- Clients now choose the best host by pinging all known nodes at startup.
 - Documented the new behavior in the networking plan and goals.

## 2025-08-04
- Nodes now act as DNS-style routers. Game hosts send a `register` packet so
  routers store their address. Clients send `find` to receive the list of
  available matches. Added helpers in `NetworkManager` and updated plans and
  goals accordingly.

## 2025-08-05
- Router nodes broadcast `games_update` packets when their host list changes.
  This keeps every node's list of joinable matches synchronized.

## 2025-08-06
- Router nodes now track active clients. When a player registers with a node
  it adds their address and broadcasts `clients_update` packets so other nodes
  learn about new peers.

## 2025-08-07
- Introduced `StateSync` helper and integrated it with `NetworkManager` so state
  packets only contain changed fields. Each update includes a sequence number to
  detect lost packets and reduce latency.

## File Overview

This section lists each source file and explains how the modules depend on one
another.  Paths are relative to the repository root.

| File | Description |
| ---- | ----------- |
| `main.py` | Small launcher that calls `hololive_coliseum.game.main`. |
| `hololive_coliseum/__init__.py` | Package initializer re-exporting all game classes for easy imports. |
| `hololive_coliseum/game.py` | Main loop, menu system and overall coordinator. Uses most other modules. |
| `hololive_coliseum/player.py` | Base character logic and subclasses for each VTuber plus the `Enemy` AI. |
| `hololive_coliseum/projectile.py` | Projectile sprites including exploding and grapple variants. |
| `hololive_coliseum/melee_attack.py` | Short-lived melee hitbox sprite. |
| `hololive_coliseum/gravity_zone.py` | Sprite representing low-gravity areas. |
| `hololive_coliseum/hazards.py` | Contains `SpikeTrap` and `IceZone` terrain hazards. |
| `hololive_coliseum/powerup.py` | Simple pickup items that heal or restore mana. |
| `hololive_coliseum/physics.py` | Utility functions for acceleration, friction and gravity. |
| `hololive_coliseum/network.py` | UDP networking helper used for online multiplayer. |
| `hololive_coliseum/node_registry.py` | Stores and updates known network node addresses. |
| `hololive_coliseum/save_manager.py` | Reads/writes `SavedGames/settings.json`. |
| `tests/` | Unit tests verifying gameplay mechanics and utilities. |
| `docs/` | Development plans and this notes file. |
| `Images/` | Placeholder art referenced by the menus. |
| `sounds/` | Placeholder directory kept empty with `.gitkeep`. |

- Added blockchain module to record multiplayer wins and wagers.

## 2025-08-08
- Removed stray merge conflict comments left from earlier revisions.
- Updated `.gitignore` to exclude temporary `test_nodes` directories created by
  the test suite.
## 2025-08-09
 - Clarified zero-vector projectile behavior and extended corresponding test.
## 2025-08-10
- Added HMAC signing to all network packets for basic security.
- Networking plan and goals updated with authentication details.
## 2025-08-11
- Implemented reliable packet mode in `NetworkManager` that resends important
  messages until an `ack` is received.
- Updated docs and goals with the new networking feature.

## 2025-08-12
- Reliable packets now have an integer importance level controlling resend rate
  and attempts.
- Added `refresh_nodes` and `prune_nodes` to drop unreachable peers.
- Blockchain module can verify and merge chains from other nodes.


## 2025-08-13
- Added holographic lithography compression for all network packets.
- NetworkManager now compresses outgoing messages and decompresses on receipt.

## 2025-08-14
- Added SHA256 verification and optional XOR encryption to the holographic
  compression module.
- NetworkManager passes an `encrypt_key` to transparently secure packets.

## 2025-08-15
- Introduced account registry storing public keys and access levels.
- Added encrypted messaging blocks to the blockchain. Messages use a mixed key
  so moderators can decrypt them if needed.

## 2025-08-16
- Split `blockchain.py` by moving account management into `accounts.py`.
- Extracted menu rendering helpers into `menus.py` so `game.py` is smaller.

## 2025-08-17
- Added `delete_account` helper to remove users from the account registry.
- Updated goals and development plan to mention account deletion.

## 2025-08-18
- Blockchain `add_game` now validates that all listed players exist in
  `accounts.json` before recording a block. Updated tests accordingly.

## 2025-08-19
- Added `get_balance` helper to query player currency totals.
- `wipe_saves` now removes directories for a clean slate.

## 2025-08-20
- Tweaked physics constants for smoother motion and introduced a dodge move bound to Left Ctrl.
- Enemy AI now checks nearby projectiles and may dodge them on harder difficulties.

## 2025-08-21
- Added Calliope's returning scythe and Kiara's explosive dive.
- Implemented boomerang and explosion projectiles to support these abilities.

## 2025-08-22
- Introduced `FreezingProjectile` and `FlockProjectile` subclasses for Fubuki and Mumei.
- Updated their special attacks to use these classes and added tests.

## 2025-08-23
- Added HealingZone sprite and updated Fauna's special to create a healing field.
- Updated docs and tests accordingly.

## 2025-08-24
- Implemented IRyS crystal shield that blocks enemy projectiles.
- Updated collision handling and documentation.
- Added unit test covering the shield ability.

## 2025-08-25
- Added PiercingProjectile and Sakura Miko's beam special that passes through enemies.
- Updated character plans, goals and documentation.

## 2025-08-26
- Introduced eight new placeholder characters to reach twenty total.
- Character select menu now displays a 5x4 grid of icons so each character has a dedicated box.
- Updated images list and character plans accordingly.

## 2025-08-27
- Added grid layout to the map selection screen and "Back" options on most menus.
- Implemented a simple lobby screen showing joined players before selecting a map.
- Updated tests and documentation.

## 2025-08-28
- Added Accounts submenu under Settings with Register/Delete options.
- `Game.execute_account_option` handles account actions and tests can invoke it.
- Documentation and goals updated to mark account management implemented.

## 2025-08-29
- Added a high-gravity zone to levels so jumps are shorter in that area.
- Updated development plan and goals to mention the new zone.
- Added tests ensuring both gravity zones load correctly.

## 2025-08-30
- Polished all menus with a teal border for better readability.
- Added a pause menu triggered with **Esc** containing Resume and Main Menu options.
- Documented the new feature and updated goals accordingly.

## 2025-08-31
- Added a Game Over screen that appears when the player loses all lives.
- The screen shows the time survived and returns to the main menu.

## 2025-09-01
- Game Over screen now also displays the best time across runs.
- Best time persists in settings and updates when a new record is reached.

## 2025-09-02
- Enemies are removed when their health reaches zero and the player gains a
  score point.
- The current score is shown during gameplay and on the Game Over screen.

## 2025-09-03
- Added victory condition when all enemies are defeated or the timer reaches the
  limit.
- A new Victory screen displays the final time, best time and score before
  returning to the main menu.

## 2025-09-04
- Game Over and Victory screens now wait three seconds before showing options.
- Added **Play Again** to return to character selection or **Main Menu** to quit
  the run.

## 2025-09-05
- Main menu offers **How to Play** and **Credits** entries with simple screens.

## 2025-09-06
- Tracked a high score across runs and displayed it on Game Over and Victory screens.
- Settings now save `best_score` alongside the best time.

## 2025-09-07
- Added a **Records** screen on the main menu showing the best time and high score.
- Planned to sync these records across nodes via the blockchain in future updates.

## 2025-09-08
- Simplified level setup with a character mapping table.
- Menu rendering now looks up draw functions from a dictionary so the game loop
  has fewer conditionals.
- The Settings menu includes **Show FPS** and **Reset Records** options.

## 2025-09-09
- Records now sync across nodes. When one player achieves a new best time or
  score, their node broadcasts the update and peers merge it into their own
  settings.

## 2025-09-10
- Added a **Latency Helper** toggle in the Node Settings menu.
- NetworkManager can now forward packets through relay nodes so players with
  better connections can help reduce latency for others.

## 2025-09-11
- Added a new **LavaZone** hazard dealing damage over time.
- Updated level setup to include a lava pit and adjusted collision handling.

## 2025-09-12
- Implemented a double jump mechanic so players can jump twice before landing.

## 2025-09-13
- Added Tokino Sora to the roster with an area-of-effect melody special.

## 2025-09-14
- Introduced `SkillManager` to centralize ability cooldowns. Gura and other characters register their specials with the manager.

## 2025-09-15
- Added basic `HealthManager`, `ManaManager` and `EquipmentManager` classes to begin modularizing player stats.
- PlayerCharacter now uses these managers internally.

## 2025-09-16
- Implemented `AIManager` to coordinate enemy actions.
- Added `NPCManager` to keep enemy and ally groups organized.
- Added `AllyManager` for future friendly NPC support.

## 2025-09-17
- Added MenuManager and GameStateManager modules for organizing menus and state transitions. Game now uses `_set_state` to update them.

## 2025-09-18
- Introduced `InventoryManager` to track collected items.
- Added `KeybindManager` so input bindings are stored separately from the `Game` class.
## 2025-09-19
- Added StatsManager for base attributes and ExperienceManager for level progression.

## 2025-09-20
- Created additional management modules including CombatManager, DamageManager,
  ThreatManager and LootManager.
- Added BuffManager plus appearance, animation and name managers.
- Implemented simple session, sync, instance and patch managers for future
  services.
## 2025-09-21
- Added security and UI-related management modules including AuthManager, CheatDetectionManager, BanManager, DataProtectionManager and LoggingManager.
- Implemented UIManager, NotificationManager, InputManager and AccessibilityManager for front-end features.
- Created ChatManager, VoiceChatManager and EmoteManager for communication.
- Added SoundManager and EffectManager placeholders for audio/visual effects.
## 2025-09-22
- Introduced ScriptManager, LocalizationManager and ResourceManager for scripting, translation and asset caching.
- Added server management modules: ClusterManager, MatchmakingManager, LoadBalancerManager and MigrationManager.
- Implemented BillingManager, AdManager, APIManager and SupportManager for external service integration.

## 2025-09-23
- Added color-coded anchor metadata to holographic compression so packets
  include black `(0,0,0)`, red `(1,0,0)`, cyan `(1,0,1)` and white `(1,1,1)`
  points describing the pointcloud bounds.
## 2025-09-24
- Created CraftingManager, ProfessionManager, TradeManager and EconomyManager
  to handle crafting, professions, trading and pricing.
## 2025-09-25
- Added CurrencyManager, TitleManager, ReputationManager, FriendManager,
  GuildManager and MailManager to flesh out social systems.
## 2025-09-26
- Introduced MapManager, EnvironmentManager, SpawnManager, EventManager and DungeonManager for world logic.
- Added HousingManager along with MountManager, PetManager and CompanionManager for player assets.
## 2025-09-27
- Expanded `ChatManager` with open/close state and capped history to display an
  in-game chat box. Updated tests and documentation.
## 2025-09-28
- Integrated the `ChatManager` with `Game` so players can toggle a chat box with
  Enter during matches. Text input is captured and sent through the manager.
  Added a new test verifying chat messages send correctly.
