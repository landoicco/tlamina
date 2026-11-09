# 🧩 Update Method

## Problem

The game world holds many independent objects: the player, 24 enemies, the bonus ufo, falling power-ups, a changing number of lasers, and the particles of every explosion. Each one moves differently, and `Game` shouldn't need to know how every object moves.

## Pattern

> The game world maintains a collection of objects. Each object implements an update method that simulates one frame of the object's behavior. Each frame, the game updates every object in the collection.

— [*Game Programming Patterns*, "Update Method"](https://gameprogrammingpatterns.com/update-method.html)

## In Tlamina

Every sprite has an `update(dt)`, and pygame's `Group.update()` calls it on each member:

| Object | `update(dt)` |
|---|---|
| `Player` | Reads input, moves, counts down the cooldown, invulnerability, and power-ups, charges the arrow, updates its lasers |
| `Enemy` | Moves horizontally at the fleet speed and fades its hit flash |
| `Ufo` | Crosses the screen and removes itself when it leaves |
| `Laser`, `Arrow` | Fly straight or at an angle and remove themselves off screen |
| `PowerUp` | Falls and removes itself if nobody catches it |
| `Effects` | Not sprites, but the same idea: moves every particle and floating text, drops the finished ones, and fades the screen shake |

`Game.update(dt)` is the update method of the whole run. It calls the groups in a fixed order (see [architecture](../architecture.md#one-frame)) and handles what involves more than one object: collisions, the combo, and the fleet moving as a unit. One level up, each scene's `update(dt)` decides whether the game advances at all: the pause screen simply doesn't call it.

## Trade-offs

- ✅ Adding an entity type means writing one class. `Game` only needs a group for it, as power-ups showed.
- ✅ Each object can be tested by calling `update(dt)` directly.
- ⚠️ **Update order matters**, as the book points out. Player lasers move before collisions are checked, while enemies, enemy lasers, and the ufo move after, so their hits are detected one frame later. The order is the same every frame, so the delay is consistent.
- ⚠️ **Removing objects mid-update.** Sprites call `kill()` on themselves while their group is being updated. This is safe because pygame iterates over a copy of the group.
- ❌ Fleet movement is not a per-enemy behavior. Every enemy must reverse together when any of them reaches an edge, so that logic lives in `Game`, not in `Enemy.update`.
