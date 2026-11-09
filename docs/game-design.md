# 🎯 Game design

What Tlamina is trying to be, and what it is not. Numbers below are starting values; the real ones live in `tlamina/settings.py` and get tuned by playing.

## 🏹 Pitch

A short-session space shooter in the spirit of the fixed-shooter classics. You hold the bottom of the screen against a fleet that grows faster every wave, and your best weapon is a charged arrow that pierces a whole column of enemies.

*Tlamina* is a Nahuatl verb meaning *to shoot arrows*. The game takes that literally: precise shots are what it rewards.

## 🧭 Pillars

1. **Every shot counts.** Accuracy is rewarded with a combo multiplier, and the charged arrow pays off for lining up enemies.
2. **Short sessions.** From launch to playing in one key press, from game over to a new run in another.
3. **Readable at a glance.** Every enemy, shot, and power-up looks different, and every hit has visible and audible feedback.

## 🔁 Game loop

```
Splash ──any key──▶ Playing ◀──Esc──▶ Paused
                      │
                  lives = 0
                      ▼
                  Game over ──Enter──▶ Playing
```

- **Splash**: title, "by Lando Icaza", a clickable [licaza.dev](https://licaza.dev) link, and a blinking "Press any key to start" over the fleet moving in the background.
- **Playing**: clear a wave and the next one starts, with no end.
- **Game over**: final score, high score, and "Press Enter to play again".

## 🎮 Controls

| Key | Action |
|---|---|
| ⬅️ / ➡️ | Move |
| Space (tap) | Shoot a laser |
| Space (hold, then release) | Charge and fire a piercing arrow |
| Esc | Pause and resume |
| Enter | Play again after a game over |

## ⚙️ Mechanics

### Charged arrow

Pressing Space fires a normal laser right away. Keep holding it for 0.8 s to charge the arrow, shown by a glow on the ship; releasing it fires an arrow that goes through every enemy in its path. Releasing early fires nothing extra. Meteors still stop it.

### Combo

Every 5 hits in a row raise the score multiplier by one, up to x4. Missing a shot or getting hit resets it to x1. A shot only counts as a miss when it leaves the screen without hitting an enemy: if any laser of a Volley hits, the Volley is not a miss.

### Power-ups

The bonus UFO always drops one when it is shot down. It falls slowly and lasts 8 s once picked up.

| Power-up | Sprite | Effect |
|---|---|---|
| Volley | `powerupBlue_star` | Three lasers in a fan per shot |
| Rapid fire | `powerupYellow_bolt` | Laser cooldown from 0.6 s to 0.2 s |
| Shield | `powerupGreen_shield` | Absorbs one hit, then breaks |

### Waves

Each wave is the same formation with a new look and a little more pressure:

- The fleet moves 10 % faster and shoots 8 % more often than in the previous wave.
- The enemy model changes every wave (`enemy*1` to `enemy*5`, then it cycles).
- From wave 3, the back row is armored: it takes two hits and flashes on the first one.

### Lives

Three lives. Each hit cracks the ship a bit more (`playerShip1_damage1` to `3`) and makes it invulnerable for 1.5 s, blinking. The fleet reaching the player ends the run.

## 👾 Enemies and scoring

| Enemy | Sprite | Points |
|---|---|---|
| Front row | `enemyRed` | 10 |
| Second row | `enemyGreen` | 20 |
| Third row | `enemyBlue` | 30 |
| Back row | `enemyBlack` | 40 |
| Bonus UFO | `ufo*` (random color) | 100 |

Points are multiplied by the current combo. The high score is saved in the user's data folder (`~/.local/share/tlamina/` on Linux, `%APPDATA%\tlamina\` on Windows).

## 🎨 Art and audio

Everything comes from Kenney's [Space Shooter Redux](https://kenney.nl/assets/space-shooter-redux) and Sci-Fi Sounds packs (CC0), plus the existing music. See [CREDITS](../CREDITS.md).

- **Look**: the `darkPurple` background with drifting stars, under the existing CRT filter. Blue lasers are the player's, red ones the enemies'.
- **Text**: the pack's Kenvector Future font for the title and HUD.
- **Feedback**: explosion particles drawn in code, floating points where an enemy dies, a light screen shake when the player is hit, and engine fire on the ship.
- **Sounds**: `sfx_zap` for picking up a power-up, `sfx_shieldUp` / `sfx_shieldDown` for the shield, `sfx_twoTone` when the combo goes up, and `sfx_lose` on game over.

## ✂️ Scope

In v0.2.0: everything above.

Left out on purpose, to keep the game small and finished:

- A main menu, options, or key remapping
- Meteors that break into smaller pieces
- Bosses or handmade wave layouts
- Online leaderboards
