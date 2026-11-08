# 🛸 Tlamina

[![CI](https://github.com/landoicco/tlamina/actions/workflows/ci.yml/badge.svg)](https://github.com/landoicco/tlamina/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python&logoColor=white)
![pygame-ce](https://img.shields.io/badge/pygame--ce-2.5%2B-5E9A2B)
![Nix flake](https://img.shields.io/badge/nix-flake-5277C3?logo=nixos&logoColor=white)
![Platforms](https://img.shields.io/badge/platforms-Linux%20%7C%20Windows-lightgrey)
![Status](https://img.shields.io/badge/status-work%20in%20progress-orange)

A retro space shooter built with [pygame-ce](https://pyga.me/). Dodge enemy fire, take cover behind the meteors, and shoot down the UFO fleet before it reaches you. 👾

> 🏹 **Tlamina** is a Nahuatl verb meaning *to shoot arrows* ([Gran Diccionario Náhuatl](https://gdn.iib.unam.mx/diccionario/tlamina)). In this game, your ship's lasers are the arrows, aimed at the invaders from above.

> 🚧 Work in progress. See the [roadmap](#-roadmap) for the current status.

## 🎮 How to play

| Key | Action |
|---|---|
| ⬅️ / ➡️ | Move |
| Space | Shoot 🔫 |

### 🏆 Scoring

| Enemy | Points |
|---|---|
| 🔴 Red UFO | 10 |
| 🟡 Yellow UFO | 20 |
| 🟢 Green UFO | 30 |
| 👽 Bonus alien | 100 |

## 🚀 Running from source

Requires Python 3.10 or newer.

❄️ With Nix:

```sh
nix develop
python code/main.py
```

⚡ With [uv](https://docs.astral.sh/uv/):

```sh
uv run python code/main.py
```

🐍 With pip:

```sh
pip install pygame-ce
python code/main.py
```

## 🧪 Development

Lint and tests run on every push and pull request. To run them locally (inside `nix develop`, or prefixed with `uv run`):

```sh
ruff check .
pytest
```

The unit tests cover the game logic (scoring, lives, fleet movement, cooldowns) without opening a window, and a smoke test runs the whole game headless for a few frames to catch crashes.

### 📁 Project layout

| Path | Contents |
|---|---|
| `code/main.py` | Entry point and game loop |
| `code/game.py` | Game state, collisions, and fleet logic |
| `code/settings.py` | Tunable constants: speeds (px/s), timers (s), scores |
| `code/player.py`, `enemy.py`, `laser.py`, `obstacle.py` | Sprites |
| `code/crt.py` | CRT screen effect |
| `code/resources.py` | Asset loading (also works inside PyInstaller builds) |
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

### ✨ 4. Gameplay: `feat/gameplay`
- [ ] Start screen
- [ ] Game over screen with restart
- [ ] Waves: a new fleet spawns when the current one is cleared, with increasing difficulty
- [ ] Obstacles that take several hits
- [ ] Tests for waves and obstacles

### 📦 5. Executables: `ci/release-builds`
- [ ] PyInstaller builds for Linux (`ubuntu-22.04`) and Windows
- [ ] Executables uploaded as artifacts on every PR
- [ ] Automatic GitHub Release when a `v*` tag is pushed
- [ ] Ship `LICENSE` and `CREDITS.md` inside the packages
- [ ] Latest release badge

### 📝 6. Documentation: `docs/portfolio`
- [ ] Identify the source, author, and license of every asset on OpenGameArt
- [ ] Replace assets with no identifiable source or a problematic license
- [ ] `CREDITS.md` with per-asset attribution
- [ ] Code license (excluding the assets) and license badge
- [ ] Gameplay GIF and download link to the latest release

## 🎨 Credits

The art and audio in this game are **not my own work**, and I do not own the rights to them. They were obtained from [OpenGameArt.org](https://opengameart.org/) and belong to their respective authors, who released them under free licenses. Detailed per-asset attribution will be provided in `CREDITS.md`.
