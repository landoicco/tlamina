# 📚 Design docs

Short notes on how Tlamina is built and why. Most of the structure follows patterns from Robert Nystrom's [*Game Programming Patterns*](https://gameprogrammingpatterns.com) (2014), and each pattern doc uses the same layout:

- **Problem**: what goes wrong in this game without the pattern
- **Pattern**: the idea in a few lines, with a link to the book chapter
- **In Tlamina**: where it lives in the code
- **Trade-offs**: what it costs, and what was left out on purpose

Start with the [architecture overview](architecture.md). What the game is trying to be, its mechanics, and its scope are in the [game design document](game-design.md).

## Patterns

| Pattern | Book chapter | Status | Where |
|---|---|---|---|
| [Game Loop](patterns/game-loop.md) | Sequencing Patterns | ✅ In use | `tlamina/__main__.py` |
| [Update Method](patterns/update-method.md) | Sequencing Patterns | ✅ In use | `update(dt)` on `Game`, every sprite, and the effects |
| [Double Buffer](patterns/double-buffer.md) | Sequencing Patterns | ✅ In use (via pygame) | `pygame.display.flip()` in `tlamina/__main__.py` |
| [Flyweight](patterns/flyweight.md) | Design Patterns Revisited | ✅ In use | `tlamina/resources.py` |
| [State](patterns/state.md) | Design Patterns Revisited | ✅ In use | `tlamina/scenes.py` |

## Considered and left out

| Pattern | Why not |
|---|---|
| [Type Object](https://gameprogrammingpatterns.com/type-object.html) | It was planned for waves and enemy types defined as data. Every wave ended up being the same formation with scaled numbers and the next enemy model, which a short formula in `Game.start_next_wave` and a few constants express better than a data format. It would pay off with handmade waves or enemies that behave differently. |
| [Observer](https://gameprogrammingpatterns.com/observer.html) | It was considered for decoupling sounds and effects from collisions. Each collision has exactly one reaction, written right where it happens in `Game.collision_checks`, so an event system would add indirection without a second listener to justify it. |
| [Object Pool](https://gameprogrammingpatterns.com/object-pool.html) | Fewer than 30 lasers and a few hundred particles are alive at once, so allocating them is not a measurable cost. A pool would add reset logic for no gain. |
| [Component](https://gameprogrammingpatterns.com/component.html) / ECS | Every entity has a fixed, small set of behaviors. Plain sprite classes are easier to read at this size (~1,300 lines). |
| [Spatial Partition](https://gameprogrammingpatterns.com/spatial-partition.html) | Collisions are checked between a few dozen sprites per frame. Brute force takes about 0.1 ms with 20 lasers on screen. |
