# 🎯 Game design

What Tlamina is trying to be, and what it leaves out. The controls are in the [README](../README.md#-how-to-play), and the exact tuning values live in `tlamina/settings.py`.

## 🏹 Pitch

A short-session space shooter in the spirit of the fixed-shooter classics. You hold the bottom of the screen against a fleet that grows faster every wave, and your best weapon is a charged arrow that pierces a whole column of enemies.

*Tlamina* is a Nahuatl verb meaning *to shoot arrows*. The game takes that literally: precise shots are what it rewards.

## 🧭 Pillars

1. **Every shot counts.** Accuracy is rewarded with a combo multiplier, and the charged arrow pays off for lining up enemies.
2. **Short sessions.** From launch to playing in one key press, from game over to a new run in another.
3. **Readable at a glance.** Every enemy, shot, and power-up looks different, and every hit has visible and audible feedback.

## 🔁 Screens

- **Splash**: title, "by Lando Icaza", a clickable [licaza.dev](https://licaza.dev) link, and a blinking "Press any key to start" over the fleet moving in the background.
- **Playing**: clear a wave and the next one starts, with no end. Esc, or the window losing focus, pauses the game.
- **Game over**: final score, high score, and "Press Enter to play again".

How the screens are implemented is in [architecture](architecture.md#-state).

## ⚙️ Mechanics

### Charged arrow

Each press of Space fires one normal laser right away; holding it doesn't keep firing. Keep holding it for 0.8 s to charge the arrow, shown by a glow on the ship's nose that pulses when ready; releasing it fires an arrow that goes through every enemy in its path and destroys armored ones in one hit. Releasing early fires nothing extra. Meteors still stop it.

### Combo

Every 5 hits in a row raise the score multiplier by one, up to ×4. Missing a shot or getting hit resets it to ×1. A shot only counts as a miss when it leaves the screen without hitting an enemy: if any laser of a Volley hits, the Volley is not a miss.

### Power-ups

The bonus UFO always drops one when it is shot down. It falls slowly and lasts 8 s once picked up.

| Power-up | Effect |
|---|---|
| ⭐ Volley | Three lasers in a fan per shot |
| ⚡ Rapid fire | Laser cooldown from 0.6 s to 0.2 s |
| 🛡️ Shield | Absorbs one hit, then breaks |

### Waves

Each wave is the same formation with a new look and a little more pressure:

- The fleet moves 10 % faster and shoots 8 % more often than in the previous wave.
- The enemy model changes every wave, cycling through five.
- From wave 3, the back row is armored: it takes two hits and flashes on the first one.

### Lives

Three lives. Each hit cracks the ship a bit more and makes it invulnerable for 1.5 s, blinking. The fleet reaching the player ends the run.

## 👾 Enemies and scoring

| Enemy | Points |
|---|---|
| 🔴 Front row | 10 |
| 🟢 Second row | 20 |
| 🔵 Third row | 30 |
| ⚫ Back row | 40 |
| 🛸 Bonus UFO | 100 |

Points are multiplied by the current combo. The high score is saved in the user's data folder (`~/.local/share/tlamina/` on Linux, `%APPDATA%\tlamina\` on Windows, `~/Library/Application Support/tlamina/` on macOS).

## 🎨 Look and feel

All art and audio come from CC0 packs; see [CREDITS](../CREDITS.md).

- **Look**: Kenney's `darkPurple` background with drifting stars, under a CRT filter drawn in code. Blue lasers are the player's, red ones the enemies'.
- **Text**: Kenney's Kenvector Future font for the title and HUD.
- **Feedback**: explosion particles, floating points where an enemy dies, a light screen shake when the player is hit, engine fire on the ship, and a sound for every event that matters: hits, power-ups, the shield, the combo going up, and game over.

## ✂️ Scope

Left out on purpose, to keep the game small and finished:

- A main menu, options, or key remapping
- Meteors that break into smaller pieces
- Bosses or handmade wave layouts
- Online leaderboards
