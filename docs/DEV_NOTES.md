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
