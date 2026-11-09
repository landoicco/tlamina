# 🎨 Credits

The art, sound effects, and music in Tlamina were made by other people. I don't own them. Every asset is released under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/), which doesn't require attribution, but their authors deserve the credit.

## 🖼️ Sprites

All sprites are packed into [`assets/atlas.png`](assets/atlas.png) by [`tools/build_atlas.py`](tools/README.md) and come unmodified from one pack:

| Pack | Author | License | Source |
|---|---|---|---|
| Space Shooter Redux | [Kenney](https://www.kenney.nl) | CC0 ([license](assets/kenney/space-shooter-redux/license.txt)) | [kenney.nl](https://kenney.nl/assets/space-shooter-redux), [OpenGameArt](https://opengameart.org/content/space-shooter-redux) |

The sprites in use are listed by their original names in [`tools/atlas.toml`](tools/atlas.toml).

The background tile, `assets/kenney/space-shooter-redux/darkPurple.png`, comes unmodified from the same pack's `Backgrounds/` folder.

## 🔊 Sound effects

| File | Used for | Pack | Author | License | Source |
|---|---|---|---|---|---|
| `assets/kenney/space-shooter-redux/sfx_laser1.ogg` | Lasers | Space Shooter Redux | [Kenney](https://www.kenney.nl) | CC0 ([license](assets/kenney/space-shooter-redux/license.txt)) | [OpenGameArt](https://opengameart.org/content/space-shooter-redux) |
| `assets/kenney/space-shooter-redux/sfx_laser2.ogg` | Charged arrow | Space Shooter Redux | [Kenney](https://www.kenney.nl) | CC0 ([license](assets/kenney/space-shooter-redux/license.txt)) | [OpenGameArt](https://opengameart.org/content/space-shooter-redux) |
| `assets/kenney/space-shooter-redux/sfx_twoTone.ogg` | Combo multiplier going up | Space Shooter Redux | [Kenney](https://www.kenney.nl) | CC0 ([license](assets/kenney/space-shooter-redux/license.txt)) | [OpenGameArt](https://opengameart.org/content/space-shooter-redux) |
| `assets/kenney/space-shooter-redux/sfx_zap.ogg` | Picking up a power-up | Space Shooter Redux | [Kenney](https://www.kenney.nl) | CC0 ([license](assets/kenney/space-shooter-redux/license.txt)) | [OpenGameArt](https://opengameart.org/content/space-shooter-redux) |
| `assets/kenney/space-shooter-redux/sfx_shieldUp.ogg` | Picking up the shield | Space Shooter Redux | [Kenney](https://www.kenney.nl) | CC0 ([license](assets/kenney/space-shooter-redux/license.txt)) | [OpenGameArt](https://opengameart.org/content/space-shooter-redux) |
| `assets/kenney/space-shooter-redux/sfx_shieldDown.ogg` | The shield breaking | Space Shooter Redux | [Kenney](https://www.kenney.nl) | CC0 ([license](assets/kenney/space-shooter-redux/license.txt)) | [OpenGameArt](https://opengameart.org/content/space-shooter-redux) |
| `assets/kenney/space-shooter-redux/sfx_lose.ogg` | Game over | Space Shooter Redux | [Kenney](https://www.kenney.nl) | CC0 ([license](assets/kenney/space-shooter-redux/license.txt)) | [OpenGameArt](https://opengameart.org/content/space-shooter-redux) |
| `assets/kenney/sci-fi-sounds/explosionCrunch_000.ogg` | Enemy destroyed | Sci-Fi Sounds | [Kenney](https://www.kenney.nl) | CC0 ([license](assets/kenney/sci-fi-sounds/license.txt)) | [kenney.nl](https://kenney.nl/assets/sci-fi-sounds), [OpenGameArt](https://opengameart.org/content/sci-fi-sounds) |
| `assets/kenney/sci-fi-sounds/explosionCrunch_001.ogg` | Player hit | Sci-Fi Sounds | [Kenney](https://www.kenney.nl) | CC0 ([license](assets/kenney/sci-fi-sounds/license.txt)) | [kenney.nl](https://kenney.nl/assets/sci-fi-sounds), [OpenGameArt](https://opengameart.org/content/sci-fi-sounds) |

## 🎵 Music

| File | Title | Author | License | Source |
|---|---|---|---|---|
| `assets/music/spacecrusher.ogg` | Spacecrusher | [yd](https://opengameart.org/users/yd) | CC0 | [OpenGameArt](https://opengameart.org/content/spacecrusher) |

## 📺 CRT effect

The screen border and scanlines are drawn in code by [`tlamina/visuals/crt.py`](tlamina/visuals/crt.py). No image is used.

## 🔤 Fonts and libraries

- Kenvector Future by [Kenney](https://www.kenney.nl), from the Space Shooter Redux pack's `Bonus/` folder (CC0, [license](assets/kenney/space-shooter-redux/license.txt)), used for the title and HUD: `assets/kenney/space-shooter-redux/kenvector_future.ttf`.
- [pygame-ce](https://pyga.me/) (LGPL 2.1), including its bundled default font, FreeSansBold from [GNU FreeFont](https://www.gnu.org/software/freefont/) (GPL with font exception), which ships inside the executable but isn't used by the game.

## 💻 Code

Tlamina started as my version of [Clear Code](https://www.youtube.com/@ClearCode)'s pygame Space Invaders tutorial ([repository](https://github.com/clear-code-projects/Space-invaders)). Since then it has been restructured and extended: delta-time movement, a sprite atlas pipeline, unit tests, CI, and the design documented in [`docs/`](docs/README.md). No art or audio from the tutorial is used.
