# Settings Menu Development Plan

The settings menu will allow players to customize their experience. Key areas:

- **Key Bindings**: Rebind actions such as jump, shoot, melee, and special attack.
- **Window Size**: Toggle between common resolutions or allow direct input.
- **Volume Control**: Adjust master volume for sounds and music.
- **Save Management**: Provide a button to wipe all files inside `SavedGames/`.
- **Account Management**: Register or delete the current user account.
- **Persistence**: Changes persist across sessions via `settings.json`.

Current prototype implements these features with a dedicated key-binding menu
and volume adjustments using the arrow keys.