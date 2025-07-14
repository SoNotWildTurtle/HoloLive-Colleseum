# Hololive Coliseum Development Plan

## Project Overview
Hololive Coliseum is a platform fighting game inspired by Super Smash Brothers, featuring popular Hololive VTubers as playable characters. The game will support single-player and multiplayer modes with both keyboard/mouse and console controller input.

Additional networking concepts are described in `DEV_PLAN_NETWORK.md`.

## Goals
- Create a playable prototype with advanced features.
- Implement unique skills for each VTuber character.
- Develop multiple maps with special gravity zones affecting physics and projectiles.
- Support local and online multiplayer modes.
- Provide basic AI opponents for single-player mode.

## Key Features
1. **Playable Characters**
   - Unique movesets and special attacks for each Hololive member.
   - Animations for walking, jumping, attacking, and using special skills.
   - Double jump mechanic for increased mobility.

2. **Maps**
   - Different stages with interactive elements.
   - Gravity modifiers (+/- gravity zones) altering character jump height and projectile paths.

3. **Input Support**
   - Keyboard + mouse control scheme.
   - Console controller support (e.g., Xbox, PlayStation, generic USB controllers).

4. **Multiplayer**
   - Local multiplayer with up to four players.
   - Networked multiplayer using rollback netcode if feasible.

## Development Steps
1. **Engine Selection**
   - For the initial prototype, we use Pygame to quickly iterate on mechanics.

2. **Project Setup**
   - Initialize repository with engine project files.
   - Add placeholder assets from `README.md` asset list.

3. **Core Gameplay**
   - Character controller for movement and jumping.
   - Basic attacks and hit detection.
   - Gravity zone logic.
   - Health and mana resource system with UI bars.

4. **Character Abilities**
   - Implement unique abilities for each VTuber.
   - Balance and test.

5. **Multiplayer Implementation**
   - Add local multiplayer.
   - Integrate networked multiplayer.
   - Allow players to join on the character screen and add AI opponents.

6. **Polish and Content**
   - Improved animations and sound effects.
   - Additional stages and items.

## Milestones
1. Prototype with one character and one stage.
2. Demo with multiple characters and local multiplayer.
3. Online multiplayer beta.
4. Version 1.0 release with polished visuals and gameplay.

## Next Steps
- Continue refining player abilities and additional characters.
- Add Ouro Kronii with a time-freeze parry. *(Implemented)*
- Add IRyS with a crystal shield. *(Implemented)*
- Add Hakos Baelz with a chaos effect. *(Implemented)*
- Add Sakura Miko with a piercing beam special. *(Implemented)*
- Polish melee attack, blocking, and parry mechanics.
- Add a double jump so players can reach higher platforms. *(Implemented)*
 - Expand maps and experiment with more gravity zones. *(High-gravity zone implemented)*
 - Introduce spike traps, ice zones and lava pits and teach AI to avoid them.
- Refine existing local multiplayer features.
- Flesh out menu flow for starting a game, adding chapter selection for story mode and graphical previews for characters and maps.
- Add grid-based map selection menu with a Back option and lobby screen listing joined players.
- Populate story mode with twenty chapter icons representing Gura's growth.
- Prototype networking with a lightweight UDP manager. Extend it with broadcast
  discovery so clients can find local hosts automatically and add an online vs
  offline selection to the menus. Introduce a `node_registry` storing known
  server addresses so user-hosted nodes can discover each other similar to a
  Hive network. Add a latency check that pings all known nodes and selects the
  closest one automatically. Extend nodes so they track active hosts and answer
  `find` requests from clients, effectively acting as DNS routers for the game.
  Share connected clients across router nodes using `clients_update` packets so
  the mesh can discover active players in real time.
  Add a reliable packet mode that resends important messages until an
  acknowledgement is received. Reliable packets should include an
  ``importance`` value to adjust retry rate. Provide ``refresh_nodes`` to remove
  unreachable peers and merge longer valid blockchains from other nodes.
  Introduce holographic lithography compression so packets are encoded as
  compact pointclouds split into two base64 strings. Include colored anchor
  points at `(0,0,0)`, `(1,0,0)`, `(1,0,1)` and `(1,1,1)` so the decoder knows
  the pointcloud bounds. Verify pointcloud data with a SHA256 digest and
  optionally XOR encrypt it using an `encrypt_key`.
- Harden save loading against corrupt files and ensure volume controls work even when the audio mixer is unavailable.
- Automatically recreate the `SavedGames` folder if it is deleted so settings save reliably.
- Spawn AI players during matches with simple pursuit logic.
- Add a difficulty selector in the character menu to scale AI behavior.
- Expand AI into Easy, Normal and Hard levels that vary reaction time and
  attack frequency.
- Introduce a dodge move for players and teach higher level AI to dodge incoming projectiles.
- Detect collisions between attacks and enemies to apply damage during combat,
  and make enemies hurt the player on contact.
- Implement encrypted messaging on the blockchain. Register account keys and
  use a mixed admin key to audit messages if abuse occurs.
- Add helper to remove accounts from `accounts.json` via the settings menu. *(Implemented)*
- Validate players against the account registry before saving a block to the
  chain.
- Add `get_balance` helper returning the stored currency for a player.
- Add a pause menu accessible with Esc during gameplay. *(Implemented)*
- Show a Game Over screen with time survived when the player loses all lives.
- Record the best survival time and show it on the Game Over screen.
- Record the best score and show it on the Game Over and Victory screens.
- Track a score for defeated enemies and display it during play and on the Game
  Over screen.
- Show a Victory screen when every enemy is defeated or the timer expires.
- Delay the end screen buttons for a few seconds and include a **Play Again**
  option that returns to character selection.
- Add **How to Play** and **Credits** screens accessible from the main menu.
- Provide a **Records** screen showing the best survival time and high score.
- Sync these records across nodes so every client sees the latest leaderboard. *(Implemented)*
- Simplify menu drawing with a lookup table for splash and option screens.
- Add **Show FPS** toggle and **Reset Records** to the settings menu.
- Provide a **Latency Helper** option so nodes can relay packets for others and
  reduce their ping.

- Introduce a `SkillManager` so abilities register once and share cooldown logic.
- Add `HealthManager` and `ManaManager` classes so health and mana logic is modular.
- Create an `EquipmentManager` framework for future item slots.
- Refactor enemy updates into an `AIManager`.
- Track NPCs with a dedicated `NPCManager` and update friendly helpers through an `AllyManager`.
- Use a `MenuManager` to manage option navigation.
- Use a `GameStateManager` so state transitions are consistent.
- Add an `InventoryManager` so items collected during play can be tracked.
- Add a `QuestManager` to record tasks and progress.
- Add an `AchievementManager` so milestones persist between sessions.
- Centralize input bindings with a `KeybindManager` for easier customization.
- Introduce a `StatsManager` for STR/DEX/INT and temporary buffs.
- Add an `ExperienceManager` to handle XP gain and leveling.
- Implement a `CombatManager` to manage turn order and targeting.
- Add a `DamageManager` for calculations and reductions.
- Track aggro with a `ThreatManager` so AI focuses the biggest threat.
- Provide a `LootManager` for randomized drops.
- Wrap status effects with a `BuffManager` for stacking rules.
- Store skins and models in an `AppearanceManager`.
- Control animation state with an `AnimationManager`.
- Manage display names via a `NameManager`.
- Maintain login sessions using a `SessionManager`.
- Exchange time offsets through a `SyncManager`.
- Create and destroy gameplay instances with an `InstanceManager`.
- Record client versions in a simple `PatchManager`.
- Add `AuthManager` and `BanManager` for login and blacklist handling.
- Detect cheats via `CheatDetectionManager` and log them with `LoggingManager`.
- Encrypt packets with `DataProtectionManager`.
- Provide `UIManager`, `NotificationManager` and `InputManager` for front-end organization.
- Support chats and voice via `ChatManager` and `VoiceChatManager`.
- Integrate the `ChatManager` into the game loop with an Enter key toggle and message history so players can chat during matches.
- Play sounds and trigger effects through `SoundManager` and `EffectManager`.
- Add a `ScriptManager`/`ScriptingEngine` for map events and modding support.
- Introduce a `LocalizationManager` for multi-language text.
- Cache assets with a `ResourceManager` for quicker loading.
- Coordinate servers via a `ClusterManager` and match players with a `MatchmakingManager`.
- Use a `LoadBalancerManager` to pick the best server and a `MigrationManager` for world transfers.
- Implement a `BillingManager` for purchases, an `AdManager` for promotions and an `APIManager` for integrations.
- Provide a `SupportManager` so players can submit tickets.
- Introduce a `CraftingManager` and `ProfessionManager` for crafting and profession progression.
- Add a `TradeManager` so players can swap items and an `EconomyManager` for shared prices.
- Track currency through a `CurrencyManager`.
- Unlock titles via a `TitleManager` and track faction standing with a `ReputationManager`.
- Maintain friends lists through a `FriendManager` and guilds via a `GuildManager`.
- Provide per-user mailboxes with a `MailManager`.
- Organize maps with a `MapManager` and track weather via an `EnvironmentManager`.
- Spawn NPCs using a `SpawnManager` and log occurrences with an `EventManager`.
- Handle dungeons through a `DungeonManager` and player housing via a `HousingManager`.
- Manage mounts, pets and companions with dedicated managers.
