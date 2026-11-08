# 🛸 Tlamina

![Python](https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python&logoColor=white)
![pygame-ce](https://img.shields.io/badge/pygame--ce-2.5%2B-5E9A2B)
![Nix flake](https://img.shields.io/badge/nix-flake-5277C3?logo=nixos&logoColor=white)
![Platforms](https://img.shields.io/badge/platforms-Linux%20%7C%20Windows-lightgrey)
![Status](https://img.shields.io/badge/status-work%20in%20progress-orange)

A retro space shooter built with [pygame-ce](https://pyga.me/). Dodge enemy fire, take cover behind the meteors, and shoot down the UFO fleet before it reaches you. 👾

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
cd code && python main.py
```

🐍 Without Nix:

```sh
pip install pygame-ce
cd code && python main.py
```

## 🗺️ Roadmap

Each phase is one pull request into `master`.

### 🧰 1. Project setup and CI: `chore/setup-and-ci`
- [x] Nix flake and `pyproject.toml` with pygame-ce
- [ ] Resource paths that don't depend on the working directory (PyInstaller-compatible)
- [ ] GitHub Actions: `ruff` lint, headless smoke test, and `pytest`
- [ ] README with roadmap
- [ ] CI status badge

### 🐛 2. Bug fixes: `fix/gameplay-bugs`
- [ ] UFO fleet leaves the screen when an edge column loses UFOs
- [ ] CRT scanlines are redrawn every frame
- [ ] Images are loaded from disk on every shot
- [ ] Bonus alien is never removed after leaving the screen
- [ ] Enemy lasers use an upward-facing sprite

### 🏗️ 3. Refactor: `refactor/game-structure`
- [ ] Remove global variables from `main.py`
- [ ] `settings.py` with constants (speeds, cooldowns, scores)
- [ ] State machine: menu → playing → game over
- [ ] Delta-time based movement
- [ ] Unit tests for game logic (collisions, scoring)

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
