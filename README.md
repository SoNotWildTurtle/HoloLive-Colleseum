# Hololive Coliseum
Prototype platform fighter featuring Hololive Vtubers.
The repository goals are detailed in [docs/GOALS.md](docs/GOALS.md).
Story mode chapters are outlined in [docs/DEV_PLAN_STORY.md](docs/DEV_PLAN_STORY.md).


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
a cyan splash screen leading to a simple menu system. Combat features melee attacks with **X**, projectile shooting with **Z**, blocking with **Shift**, and a parry on **C**. A low-gravity zone reduces jump speed.
Movement now uses acceleration and friction for smoother platforming.
Menu navigation now includes character, map, and chapter selection screens with
placeholder icons generated at runtime. During offline multiplayer character
selection a **"Press J to join"** prompt allows additional local players to join,
 and an **Add AI Player** option lets you fill extra slots with simple bots in
 either solo or multiplayer. Selected AI players now spawn as enemies that
  chase the human player. Projectiles and melee attacks damage enemies on
   contact, and enemies hurt the player when touching them. Press **V** to use Gura's special trident attack,
Watson's time-dash, or Ina's tentacle grapple during gameplay. Projectiles can be aimed with the mouse and the special attack
fires an exploding shot. Powerups periodically spawn to restore health or mana
and a simple life counter and level timer are displayed. A revamped **Settings**
menu features key and controller binding editors, volume adjustments,
window-size toggling, and a save-wipe option so preferences persist across
sessions.

### Story Mode
The single-player campaign follows Gura's growth from rookie idol to battle-tested hero.
Twenty chapter icons appear in the chapter select menu, each representing a new location and challenge.
Selecting an icon loads its corresponding map using the placeholder images listed above.
Additional characters, maps, and features will be introduced over time.

### Networking Prototype
The package now contains a `NetworkManager` module that uses UDP sockets for
lightweight communication. Hosts answer broadcast discovery packets so clients
can automatically locate games on the local network. The menus include an
online versus offline multiplayer option to select whether to connect to other
discovered nodes or play locally.
