# 🧩 Update Method

## Problem

The game world holds many independent objects: the player, 15 UFOs, the bonus alien, and a changing number of lasers. Each one moves differently, and `Game` shouldn't need to know how every object moves.

## Pattern

> The game world maintains a collection of objects. Each object implements an update method that simulates one frame of the object's behavior. Each frame, the game updates every object in the collection.

— [*Game Programming Patterns*, "Update Method"](https://gameprogrammingpatterns.com/update-method.html)

## In Tlamina

Every sprite has an `update(dt)`, and pygame's `Group.update()` calls it on each member:

| Sprite | `update(dt)` |
|---|---|
| `Player` | Reads input, moves, counts down the shooting cooldown, updates its lasers |
| `Ufo` | Moves horizontally at the fleet speed |
| `Alien` | Crosses the screen and removes itself when it leaves |
| `Laser` | Moves vertically and removes itself off screen |

`Game.update(dt)` is the update method of the whole world. It calls the groups in a fixed order (see [architecture](../architecture.md#one-frame)) and handles what involves more than one object: collisions and the fleet bouncing as a unit.

## Trade-offs

- ✅ Adding an entity type means writing one class. `Game` only needs a group for it.
- ✅ Each sprite can be tested by calling `update(dt)` directly.
- ⚠️ **Update order matters**, as the book points out. Player lasers move before collisions are checked, while UFOs, enemy lasers, and the alien move after, so their hits are detected one frame later. The order is the same every frame, so the delay is consistent.
- ⚠️ **Removing objects mid-update.** Sprites call `kill()` on themselves while their group is being updated. This is safe because pygame iterates over a copy of the group.
- ❌ Fleet movement is not a per-UFO behavior. Every UFO must reverse together when any of them reaches an edge, so that logic lives in `Game`, not in `Ufo.update`.
