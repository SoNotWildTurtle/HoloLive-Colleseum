# HoloLive Coliseum Development Plan

## Project Overview
HoloLive Coliseum is a platform fighting game inspired by Super Smash Brothers, featuring popular Hololive Vtubers as playable characters. The game will support single-player and multiplayer modes with both keyboard/mouse and console controller input.

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
   - Evaluate game engines (Godot, Unity, Unreal). Prefer an open-source option (Godot) for easier collaboration.

2. **Project Setup**
   - Initialize repository with engine project files.
   - Add placeholder assets from `README.md` asset list.

3. **Core Gameplay**
   - Character controller for movement and jumping.
   - Basic attacks and hit detection.
   - Gravity zone logic.

4. **Character Abilities**
   - Implement unique abilities for each Vtuber.
   - Balance and test.

5. **Multiplayer Implementation**
   - Add local multiplayer.
   - Integrate networked multiplayer.

6. **Polish and Content**
   - Improved animations and sound effects.
   - Additional stages and items.

## Milestones
1. Prototype with one character and one stage.
2. Demo with multiple characters and local multiplayer.
3. Online multiplayer beta.
4. Version 1.0 release with polished visuals and gameplay.

## Next Steps
- Choose an engine and begin prototype development.
- Commit engine project files and placeholder assets to the repository.
- Start building the character controller and stage with gravity zones.

