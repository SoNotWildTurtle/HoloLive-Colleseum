# Project Goals and Architecture Overview

This document collects the current goals and explains how each part of the
prototype works.  It complements `DEV_PLAN.md` and the other development notes.

## High Level Goals

- Build a platform fighter inspired by Super Smash Brothers with Hololive
  VTubers.
- Support both single player and multiplayer, locally and online.
- Provide controller and keyboard/mouse input with configurable bindings.
- Include special abilities, projectiles, melee attacks, blocking and parry
  mechanics.
- Prototype powerups, gravity zones and basic AI opponents.

## Development Plan

The detailed plan lives in `docs/DEV_PLAN.md`.  In short, we are iterating on a
Pygame prototype first.  Features are added in small steps:

1. Core player movement with acceleration and friction.
2. Combat options: shooting, melee, blocking, parry and unique specials.
3. Menus for splash screen, game type selection, character selection and maps.
4. Settings menu with key/controller bindings, volume and save management.
5. Local multiplayer and a lightweight UDP networking layer for online play,
   using a `node_registry` so hosts can discover each other across the internet.
6. Additional characters and maps with unique mechanics.

## Module Overview

### `hololive_coliseum.game.Game`
Handles the main Pygame loop. It coordinates player input, spawns
projectiles and melee attacks, updates gravity zones and powerups and saves
settings on exit. Menu drawing helpers now live in `menus.py` which is mixed
into the `Game` class.

Key methods:
- `run()` — main loop switching between menu states and gameplay.
- Menu navigation updates internal state to choose characters, maps and
  multiplayer options.

### `hololive_coliseum.player.PlayerCharacter`
Base sprite for all characters and enemies.  Features include:
- Acceleration and friction based movement using `physics` helpers.
- Jumping, blocking, parry and gravity adjustment.
- Ability to double jump before landing.
- Health, mana and life tracking with a `draw_status` helper.
- `shoot`, `melee_attack` and `special_attack` create offensive sprites.

`GuraPlayer` extends this class to add the trident special attack.  `Enemy`
subclasses `PlayerCharacter` and contains a tiny AI routine.

### `hololive_coliseum.projectile`
Defines `Projectile` and `ExplodingProjectile`.  Projectiles move each frame and
are removed when leaving the screen or when their timer expires.

### `hololive_coliseum.melee_attack`
Small hitbox sprite used for close range attacks.  It self-destructs after a few
frames.

### `hololive_coliseum.gravity_zone`
Provides the `GravityZone` sprite that modifies gravity for any `Player` inside
its rectangle.  The `Game` loop checks for collisions with these zones and sets
the player's gravity multiplier accordingly.

### `hololive_coliseum.powerup`
Simple powerups that restore health or mana when the player collides with them.
They are spawned periodically by the `Game` loop.

### `hololive_coliseum.hazards`
Defines `SpikeTrap` and `IceZone` terrain hazards. `Game` adds these to maps and
enemy AI will attempt to avoid them.

### `hololive_coliseum.physics`
Contains helper functions for gravity, acceleration and friction.  These are used
by the `Player` class to keep movement consistent.

### `hololive_coliseum.network`
A lightweight UDP manager with discovery so clients can locate local hosts.
Hosts call `poll()` to process incoming data.  Clients call `discover()` to find
servers.  Both sides use `send_state()` for game data.

### `hololive_coliseum.node_registry`
Reads and writes `nodes.json` in the save directory, keeping a list of known
servers. Hosts add themselves to the registry and share their address via
`announce` packets so a mesh of nodes can be built.

### `hololive_coliseum.menus`
Provides ``MenuMixin`` with helpers to draw splash and option menus. ``Game``
inherits from this mixin so the rendering code is kept separate from gameplay.

### `hololive_coliseum.save_manager`
Loads and saves configuration files in the `SavedGames` directory.  `Game` uses
it to store window size, volume and input bindings.  The settings menu can also
invoke `wipe_saves()` to clear this folder.

### `hololive_coliseum.accounts`
Manages user accounts stored in ``accounts.json``. Functions allow registering
public keys and access levels so messages on the blockchain can be encrypted for
each user. Accounts can also be deleted.

## File Dependencies

- `game.py` imports almost all other modules and drives the simulation.
- `player.py` relies on `physics.py` for movement logic and spawns projectiles,
  melee attacks and special projectiles from other modules.
- `network.py` is optional but used when online multiplayer is selected.
- `save_manager.py` is required by `game.py` to persist settings.
- Tests under `tests/` import these modules to verify key features.

## Interplay

During gameplay, `Game` calls `player.handle_input()` which uses
`physics.accelerate` and `physics.apply_friction` to update velocity.  Each frame
`player.update()` applies gravity via `physics.apply_gravity` and checks for
parry timing.  When attacks occur, new `Projectile` or `MeleeAttack` sprites are
added to the `all_sprites` group.  `GravityZone` sprites alter the player's
gravity multiplier, and `PowerUp` sprites restore health or mana when collected.

Settings are loaded at startup and saved on exit through `save_manager`.  If
online mode is chosen, `NetworkManager` handles packet exchange for state
synchronization or discovery of other hosts.

## Short-Term Goals

- Flesh out each VTuber's unique abilities (see `DEV_PLAN_CHARACTERS.md`).
*Watson Amelia implemented.*
 *Ninomae Ina'nis implemented.*
 *Shirakami Fubuki implemented.*
 *Sakura Miko implemented.*
*Ceres Fauna implemented.*
*Nanashi Mumei implemented.*
*Ouro Kronii implemented.*
*IRyS implemented.*
   *Hakos Baelz implemented.*
   *Tokino Sora implemented.*
   *Minato Aqua implemented.*
   *Usada Pekora implemented.*
   *Houshou Marine implemented.*
   *Hoshimachi Suisei implemented.*
   *Nakiri Ayame implemented.*
   *Shirogane Noel implemented.*
   *Shiranui Flare implemented.*
   *Oozora Subaru implemented.*
  - Roster expanded to **21** playable characters with unique specials.
 - Expand map mechanics with gravity zones, spike traps, ice patches and lava pits. *(High-gravity zone added)*
- Improve enemy AI to navigate around hazards intelligently.
- Add AI-controlled opponents that use the shared `PlayerCharacter` base class.
- Provide a difficulty selector so AI behavior can scale from Easy to Hard.
- Implement three AI levels with different reaction times and aggression.
- Add a dodge action for players and let advanced AI attempt dodges when threatened.
- Support double jumps for greater mobility. *(Implemented)*
- Implement combat collisions so projectiles and melee attacks damage
  enemies, and enemies now harm the player on contact.
- Polish menus with clearer prompts and optional controller hints. *(Improved with teal borders)*
- Draw menus via a lookup table instead of long chains of conditionals.
- Add an in-game pause menu triggered with Esc.
- Display a Game Over screen when the player runs out of lives.
- Track the best survival time and show it on the Game Over screen.
- Track the highest score and show it on Game Over and Victory screens.
- Keep a running score of defeated enemies and display it during gameplay and on
  the Game Over screen.
- Show a Victory screen when the timer expires or all enemies are defeated.
- End screens should pause for a moment before showing **Play Again** and
  **Main Menu** buttons; Play Again returns to character selection.
- Provide **How to Play** instructions and a **Credits** screen in the main menu.
- Include a **Records** menu showing your best time and high score.
- Sync records across nodes so everyone sees the latest leaderboard.
- Add **Show FPS** and **Reset Records** options to the settings menu.
- Add grid-based map selection and a lobby screen listing joined players.
- Continue adding tests for new mechanics as they appear.
- Cover edge cases like zero-length projectile shots to prevent crashes.
- Design the "Growing Up" story mode with 20 chapter icons that load each level.
- Record multiplayer results in a lightweight blockchain so wins submit a block
  shared with other players. Include search tools and a simple currency for
  betting on matches.
- Allow players to start or stop acting as a blockchain node from the settings
  menu to help grow a decentralized network.
- Offer a **Latency Helper** toggle so willing players can act as relay nodes and
  route traffic for others when they have a faster connection.
- Provide account management features including deleting accounts when needed. *(Implemented)*
- Validate that all players recorded on the blockchain have registered accounts.
- Provide `get_balance` to read each player's currency amount from `balances.json`.
- Ping known nodes at startup and connect to the one with the lowest latency.
- Nodes act as game routers: hosts register with them and clients query for
  available matches so players can find each other across the mesh.
- Router nodes exchange game lists via `games_update` packets and also
  synchronize active clients with `clients_update` so the mesh knows who is
  online.
- State updates use the `StateSync` delta system with sequence numbers for
  efficient packet sizes and minimal latency.
- Packets include an HMAC signature when a shared secret is set so nodes can
  discard tampered data.
- Compress network traffic using a holographic lithography approach that
  converts each packet into a compact pointcloud represented by two base64
  strings. Anchor points at `(0,0,0)` (black), `(1,0,0)` (red), `(1,0,1)` (cyan)
  and `(1,1,1)` (white) describe the bounds so peers can reconstruct packets.
- Verify the pointcloud bytes with a SHA256 digest and optionally XOR encrypt
  them while in transit.
- Important control packets support a **reliable** mode that resends them until
  acknowledged so critical data like game registration is not lost.
- Reliable packets accept an integer importance so crucial updates retry faster
  and more often.
- Nodes periodically drop unreachable peers from the registry to keep the mesh
  healthy.
- Blockchain data can be verified and longer valid chains replace stale copies.

## Long-Term Goals

- Improve network latency handling and implement rollback if possible.
- Add proper sprites and sound effects once the gameplay loop is solid.
- Introduce a full story mode with chapters and cutscenes.
- Package the game for multiple platforms with configurable installers.
- Handle corrupt save files gracefully and keep UI responsive even without audio support.
- Ensure the save directory is recreated automatically if missing.
- Support encrypted player messaging with public and admin keys so abusive
  chats can be audited while regular messages remain private.

- Centralize special ability cooldowns through a `SkillManager`.
- Add dedicated `HealthManager` and `ManaManager` classes for resource tracking.
- Introduce an `EquipmentManager` so players can equip items in various slots.
- Manage all enemies through an `AIManager` so decision logic stays organized.
- Provide an `NPCManager` for grouping enemies and potential allies.
- Add an `AllyManager` to update friendly NPC behavior.
- Track menu navigation with a `MenuManager` so option handling is reusable.
- Track the current game state in a `GameStateManager` for cleaner transitions.
- Manage player inventory with an `InventoryManager`.
- Track quests with a `QuestManager` so objectives can be completed.
- Record achievements with an `AchievementManager`.
- Store key mappings in a `KeybindManager` so rebinding works consistently.
- Provide a `StatsManager` for core attributes with modifiers.
- Implement an `ExperienceManager` for XP and leveling logic.
- Introduce a `CombatManager` for turn order.
- Add a `DamageManager` to handle reductions.
- Keep aggro tables in a `ThreatManager`.
- Generate item drops with a `LootManager`.
- Coordinate buffs through a `BuffManager`.
- Store character skins in an `AppearanceManager`.
- Track animations via an `AnimationManager`.
- Support renames with a `NameManager`.
- Manage login tokens using a `SessionManager`.
- Keep clocks synchronized through a `SyncManager`.
- Spin up separate sessions using an `InstanceManager`.
- Track game versions with a `PatchManager`.
- Enforce logins and bans with `AuthManager` and `BanManager`.
- Detect cheating through `CheatDetectionManager` and record events via `LoggingManager`.
- Secure data using `DataProtectionManager`.
- Organize UI with `UIManager` and show alerts via `NotificationManager`.
- Centralize controls with `InputManager` and accessibility settings with `AccessibilityManager`.
- Provide text and voice communication using `ChatManager` and `VoiceChatManager`.
- The chat manager is integrated with gameplay: pressing Enter toggles the chat box and messages are stored in a limited history.
- Manage audio and visual effects through `SoundManager` and `EffectManager`.
- Load and execute scripts with a `ScriptManager`.
- Provide translations through a `LocalizationManager`.
- Cache assets using a `ResourceManager`.
- Manage cross-server groups via a `ClusterManager` and `MatchmakingManager`.
- Balance server load with a `LoadBalancerManager` and support migrations through a `MigrationManager`.
- Track purchases using a `BillingManager` and display ads with an `AdManager`.
- Integrate third-party services through an `APIManager` and handle support tickets via `SupportManager`.
- Handle crafting via a `CraftingManager` and track professions through a `ProfessionManager`.
- Manage player trades with a `TradeManager` and global prices via an `EconomyManager`.
- Track gold and other money with a `CurrencyManager`.
- Unlock titles using a `TitleManager` and adjust faction standing via a `ReputationManager`.
- Maintain friends and guilds through `FriendManager` and `GuildManager`.
- Provide mailboxes through a `MailManager`.
- Organize world data with a `MapManager` and `EnvironmentManager`.
- Control spawns via a `SpawnManager` and log events through an `EventManager`.
- Handle dungeon lockouts using a `DungeonManager` and store housing via a `HousingManager`.
- Track mounts with a `MountManager`, pets with a `PetManager` and companions via a `CompanionManager`.
