# Project Goals and Architecture Overview

This document collects the current goals and explains how each part of the
prototype works.  It complements `DEV_PLAN.md` and the other development notes.

## High Level Goals

- Build a platform fighter inspired by Super Smash Brothers with Hololive
  Vtubers.
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
5. Local multiplayer and a lightweight UDP networking layer for online play.
6. Additional characters and maps with unique mechanics.

## Module Overview

### `hololive_coliseum.game.Game`
Handles the main Pygame loop and all menus.  It coordinates player input,
spawns projectiles and melee attacks, updates gravity zones and powerups and
saves settings on exit.  The game depends on almost every other module.

Key methods:
- `run()` — main loop switching between menu states and gameplay.
- `_draw_*` helpers — render splash/menu screens.
- Menu navigation updates internal state to choose characters, maps and
  multiplayer options.

### `hololive_coliseum.player.Player`
Base sprite for all characters and enemies.  Features include:
- Acceleration and friction based movement using `physics` helpers.
- Jumping, blocking, parry and gravity adjustment.
- Health, mana and life tracking with a `draw_status` helper.
- `shoot`, `melee_attack` and `special_attack` create offensive sprites.

`GuraPlayer` extends this class to add the trident special attack.  `Enemy`
subclasses `Player` and contains a tiny AI routine.

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

### `hololive_coliseum.physics`
Contains helper functions for gravity, acceleration and friction.  These are used
by the `Player` class to keep movement consistent.

### `hololive_coliseum.network`
A lightweight UDP manager with discovery so clients can locate local hosts.
Hosts call `poll()` to process incoming data.  Clients call `discover()` to find
servers.  Both sides use `send_state()` for game data.

### `hololive_coliseum.save_manager`
Loads and saves configuration files in the `SavedGames` directory.  `Game` uses
it to store window size, volume and input bindings.  The settings menu can also
invoke `wipe_saves()` to clear this folder.

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

- Flesh out each Vtuber's unique abilities (see `DEV_PLAN_CHARACTERS.md`).
  *Watson Amelia implemented.*
- Expand map mechanics and integrate more gravity zones and hazards.
- Add AI-controlled opponents that use the same `Player` base class.
- Implement combat collisions so projectiles and melee attacks damage
  enemies, and enemies now harm the player on contact.
- Polish menus with clearer prompts and optional controller hints.
- Continue adding tests for new mechanics as they appear.

## Long-Term Goals

- Improve network latency handling and implement rollback if possible.
- Add proper sprites and sound effects once the gameplay loop is solid.
- Introduce a full story mode with chapters and cutscenes.
- Package the game for multiple platforms with configurable installers.
- Handle corrupt save files gracefully and keep UI responsive even without audio support.
- Ensure the save directory is recreated automatically if missing.

