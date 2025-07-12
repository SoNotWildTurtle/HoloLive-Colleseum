# Hololive Coliseum Development Plan

## Project Overview
Hololive Coliseum is a platform fighting game inspired by Super Smash Brothers, featuring popular Hololive Vtubers as playable characters. The game will support single-player and multiplayer modes with both keyboard/mouse and console controller input.

Additional networking concepts are described in `DEV_PLAN_NETWORK.md`.

## Goals
- Create a functional prototype with placeholder sprites and minimal features.
- Implement unique skills for each Vtuber character.
- Develop multiple maps with special gravity zones affecting physics and projectiles.
- Support local and online multiplayer modes.
- Provide basic AI opponents for single-player mode.

## Key Features
1. **Playable Characters**
   - Unique movesets and special attacks for each Hololive member.
   - Animations for walking, jumping, attacking, and using special skills.

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
   - Implement unique abilities for each Vtuber.
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
 - Expand maps and experiment with more gravity zones. *(High-gravity zone implemented)*
- Introduce spike traps and ice zones and teach AI to avoid them.
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
  compact pointclouds split into two base64 strings. Verify pointcloud data with
  a SHA256 digest and optionally XOR encrypt it using an `encrypt_key`.
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
- Sync these records across nodes so every client sees the latest leaderboard.

