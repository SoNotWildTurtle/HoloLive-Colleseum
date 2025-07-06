# HoloLive Coliseum
Prototype platform fighter featuring Hololive Vtubers.


## Asset Placeholders
The repository references simple placeholder images and a sound effect so the game runs without additional downloads. The PNG and WAV files are not included.

Directories
- `SavedGames/`
- `Images/`
- `sounds/`
The `SavedGames` folder stores settings in `settings.json`. Selecting "Wipe
saves" from the settings menu clears this directory.

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
a cyan splash screen leading to a simple menu system. Combat features melee attacks
with **X**, projectile shooting with **Z**, blocking with **Shift**, and a parry on
**C**. A low-gravity zone reduces jump speed.
Menu navigation now includes character, map, and chapter selection screens with
simple previews. Multiplayer can be played offline or online, chosen from a new
multiplayer mode menu. Press **V** to use Gura's special trident attack during
gameplay. A new **Settings** menu allows adjusting key bindings, window size,
and volume, as well as wiping saved data.
Additional characters, maps, and features will be introduced over time.

### Networking Prototype
The package now contains a `NetworkManager` module that uses UDP sockets for
lightweight communication. Hosts answer broadcast discovery packets so clients
can automatically locate games on the local network. The menus include an
online versus offline multiplayer option to select whether to connect to other
discovered nodes or play locally.
