# 🛸 Tlamina

![Tlamina: a retro space shooter](docs/banner.png)

[![CI](https://github.com/landoicco/tlamina/actions/workflows/ci.yml/badge.svg)](https://github.com/landoicco/tlamina/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/landoicco/tlamina)](https://github.com/landoicco/tlamina/releases/latest)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
![Python](https://img.shields.io/badge/python-3.11%2B-3776AB?logo=python&logoColor=white)
![pygame-ce](https://img.shields.io/badge/pygame--ce-2.5%2B-5E9A2B)
![Nix flake](https://img.shields.io/badge/nix-flake-5277C3?logo=nixos&logoColor=white)
![Platforms](https://img.shields.io/badge/platforms-Linux%20%7C%20Windows-lightgrey)

A retro space shooter built with [pygame-ce](https://pyga.me/). Hold off an alien fleet that comes back faster every wave: take cover behind the meteors, charge arrows that pierce whole columns, chain hits into a score multiplier, and grab the power-ups the bonus ufo drops. 👾

> 🏹 **Tlamina** is a Nahuatl verb meaning *to shoot arrows* ([Gran Diccionario Náhuatl](https://gdn.iib.unam.mx/diccionario/tlamina)). In this game, your strongest weapon is a charged arrow that flies through every enemy in its path.

## 🎮 How to play

| Key | Action |
|---|---|
| <kbd>←</kbd> <kbd>→</kbd> | Move |
| <kbd>Space</kbd> | Shoot a laser 🔫 |
| Hold <kbd>Space</kbd>, then release | Fire a charged arrow that pierces every enemy in its path 🏹 |
| <kbd>Esc</kbd> | Pause and resume |
| <kbd>Enter</kbd> | Play again after a game over |

> 💡 The charged arrow is the key to a high score: line it up under a column, and every enemy it pierces counts toward your combo.

Clear the fleet and a new wave starts, faster and with a new look. From wave 3, the back row is armored and takes two lasers, or one arrow. You have three lives, and each hit cracks your ship a little more.

### 🏆 Scoring

| Enemy | Points |
|---|---|
| 🔴 Front row | 10 |
| 🟢 Second row | 20 |
| 🔵 Third row | 30 |
| ⚫ Back row | 40 |
| 🛸 Bonus ufo | 100 |

Every 5 hits in a row raise the **combo multiplier** by one, up to ×4. A shot that leaves the screen without hitting anything, or getting hit, resets it. Your best score is saved between runs.

### ⚡ Power-ups

The bonus ufo drops one every time you shoot it down. Each lasts 8 seconds.

| Power-up | Effect |
|---|---|
| ⭐ Volley | Three lasers in a fan per shot |
| ⚡ Rapid fire | Shoot three times as often |
| 🛡️ Shield | Absorbs one hit |

## 📥 Download

Get the latest build for Windows or Linux from the [releases page](https://github.com/landoicco/tlamina/releases/latest). Each package contains a single executable, no installation needed.

- 🪟 **Windows**: unzip `tlamina-windows.zip` and run `Tlamina.exe`. The executable isn't signed, so Windows SmartScreen may warn about it the first time: choose *More info* → *Run anyway*.
- 🐧 **Linux**: extract `tlamina-linux.tar.gz` and run `./Tlamina`. Builds target glibc 2.35 or newer (Ubuntu 22.04 and later).

Builds of every pull request are also available as artifacts on its CI run. Artifacts don't keep file permissions, so on Linux run `chmod +x Tlamina` first.

To build an executable yourself, run `uv run --group build python tools/build_exe.py`; the result goes to `dist/`.

## 🚀 Running from source

Requires Python 3.11 or newer.

❄️ With Nix:

```sh
nix develop
python -m tlamina
```

⚡ With [uv](https://docs.astral.sh/uv/):

```sh
uv run python -m tlamina
```

🐍 With pip:

```sh
pip install pygame-ce
python -m tlamina
```

## 🧪 Development

Lint and tests run on every push and pull request. To run them locally (inside `nix develop`, or prefixed with `uv run`):

```sh
ruff check .
pytest
```

The unit tests cover the game logic without opening a window: scoring and the combo, lives and the shield, waves, the charged arrow, power-ups, scene transitions, and high score storage. A smoke test runs the whole game headless for a few frames to catch crashes.

### 📚 Design docs

How the game is structured and why, based on Robert Nystrom's *Game Programming Patterns*: see [`docs/`](docs/README.md). What the game is trying to be, and what it leaves out, is in the [game design document](docs/game-design.md).

### 📁 Project layout

| Path | Contents |
|---|---|
| `tlamina/__main__.py` | Entry point and game loop |
| `tlamina/game.py` | Game state, collisions, waves, and fleet logic |
| `tlamina/scenes.py` | Splash, playing, pause, and game over screens |
| `tlamina/settings.py` | Tunable constants: speeds (px/s), timers (s), scores |
| `tlamina/resources.py` | Asset loading and sprite atlas lookup (also works inside PyInstaller builds) |
| `tlamina/highscore.py` | Saving the high score in the user's data folder |
| `tlamina/entities/` | Sprites that move and collide: player, enemies, lasers and the arrow, meteors, power-ups |
| `tlamina/visuals/` | Drawing only: background, explosions and other effects, CRT filter, text |
| `assets/atlas.png`, `atlas.json` | Sprite atlas generated by `tools/build_atlas.py` |
| `tools/` | Asset tooling, see [`tools/README.md`](tools/README.md) |
| `tests/` | Unit and smoke tests |

## 🗺️ Roadmap

Each phase is one pull request into `master`.

### 🧰 1. Project setup and CI: `chore/setup-and-ci`
- [x] Nix flake and `pyproject.toml` with pygame-ce
- [x] Resource paths that don't depend on the working directory (PyInstaller-compatible)
- [x] GitHub Actions: `ruff` lint, headless smoke test, and `pytest`
- [x] README with roadmap
- [x] CI status badge

### 🐛 2. Bug fixes: `fix/gameplay-bugs`
- [x] UFO fleet leaves the screen when an edge column loses UFOs
- [x] CRT scanlines are redrawn every frame
- [x] Images are loaded from disk on every shot
- [x] Bonus alien is never removed after leaving the screen
- [x] Enemy lasers use an upward-facing sprite

### 🏗️ 3. Refactor: `refactor/game-structure`
- [x] Remove global variables from `main.py`
- [x] `settings.py` with constants (speeds, cooldowns, scores)
- [x] Game states (playing → game over) instead of exiting the process; screens come in phase 4
- [x] Delta-time based movement
- [x] Unit tests for game logic (collisions, scoring)
- [x] Fix the player ship being drawn past the right edge of the screen

### 🎨 4. Assets and credits: `chore/assets`
- [x] Identify the source, author, and license of every asset
- [x] Lossless sprite atlas built from Kenney's *Space Shooter Redux* (CC0), with only the sprites in use
- [x] Load sprites by name from the atlas, with a global `SPRITE_SCALE`
- [x] Replace assets with no identifiable source or a problematic license: CC0 audio, and the CRT border is now drawn in code
- [x] `CREDITS.md` with per-asset attribution
- [x] Design docs for the patterns already in use (`docs/`)

### 📦 5. Executables: `ci/release-builds`
- [x] Single-file PyInstaller builds for Linux (`ubuntu-22.04`) and Windows, smoke-tested in CI
- [x] Executables uploaded as artifacts on every PR
- [x] Automatic GitHub Release when a `v*` tag is pushed
- [x] Code license (MIT, excluding the assets) and third-party notices for the bundled libraries
- [x] Ship `LICENSE`, `CREDITS.md`, and the notices inside the packages
- [x] Release and license badges

### ✨ 6. Gameplay: `feature/gameplay`
- [x] [Game design document](docs/game-design.md) to set the goals and the scope
- [x] Splash, pause, and game over screens with restart (*State* pattern), and a saved high score
- [x] Endless waves with increasing difficulty, a new enemy model each wave, and an armored back row
- [x] Charged arrow that pierces through enemies, combo multiplier, and power-ups from the bonus ufo
- [x] Visual feedback: explosions, floating points, ship damage cracks, screen shake, drifting star background
- [x] Code moved into a `tlamina` package
- [x] Tests for every mechanic, and design docs for the new pattern
- ~~Waves defined as data (*Type Object* pattern)~~: a formula turned out simpler, see [design docs](docs/README.md#considered-and-left-out)
- ~~Obstacles that shrink as they get damaged~~: left out to keep the scope small

### 📝 7. Documentation: `docs/portfolio`
- [ ] Architecture section in the README linking the design docs
- [ ] Gameplay GIF and download link to the latest release

## 🌱 From tutorial to finished game

Tlamina started in December 2021 as my take on [Clear Code](https://www.youtube.com/@ClearCode)'s [pygame Space Invaders tutorial](https://github.com/clear-code-projects/Space-invaders), and the first commits follow the video step by step. In 2026 I came back to it to turn it into a complete, polished game, and to practice what a small project looks like when it's built properly.

| | Tutorial starting point | Tlamina today |
|---|---|---|
| **Gameplay** | One fleet, one kind of shot | Endless waves, armored enemies, charged arrow, combo multiplier, power-ups |
| **Screens** | The window closes on game over | Splash, pause, and game over screens, and a saved high score |
| **Art and audio** | The tutorial's own files | Kenney's CC0 packs, packed into a sprite atlas by a script; CRT effect drawn in code |
| **Feel** | Sprites disappear on hit | Explosions, floating points, damage cracks, screen shake |
| **Code** | A few modules with global state, frame-based movement | A `tlamina` package organized by role, delta-time movement, design patterns documented in [`docs/`](docs/README.md) |
| **Quality** | No tests | 105 tests, strict linting, CI on every pull request |
| **Distribution** | Run from source | Linux and Windows executables built and released automatically |

### 🤖 Built with AI assistance

The 2026 work was done with [Claude Code](https://claude.com/claude-code) as a pair programmer. I set the direction and made the design decisions, from the [game design document](docs/game-design.md) to how the code is organized, reviewed every change, and made every commit. Claude Code helped write the code, the tests, and the documentation, and reviewed the project for bugs along the way.

## 🎨 Credits

The art and audio in this game are **not my own work**, and I do not own the rights to them. Sprites and sound effects are by [Kenney](https://www.kenney.nl) and the music is by [yd](https://opengameart.org/users/yd), all released under CC0. See [`CREDITS.md`](CREDITS.md) for per-asset attribution.

The code started from [Clear Code](https://www.youtube.com/@ClearCode)'s pygame Space Invaders tutorial; see [From tutorial to finished game](#-from-tutorial-to-finished-game) for how it grew from there.

## 📄 License

The code is released under the [MIT License](LICENSE). The art and audio in `assets/` are not covered by it; see [`CREDITS.md`](CREDITS.md). The executables also bundle third-party libraries under their own licenses; see [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).
