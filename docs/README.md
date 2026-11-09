# 📚 Design docs

Short notes on how Tlamina is built and why. Most of the structure follows patterns from Robert Nystrom's [*Game Programming Patterns*](https://gameprogrammingpatterns.com) (2014), and each pattern doc uses the same layout:

- **Problem**: what goes wrong in this game without the pattern
- **Pattern**: the idea in a few lines, with a link to the book chapter
- **In Tlamina**: where it lives in the code
- **Trade-offs**: what it costs, and what was left out on purpose

Start with the [architecture overview](architecture.md).

## Patterns

| Pattern | Book chapter | Status | Where |
|---|---|---|---|
| [Game Loop](patterns/game-loop.md) | Sequencing Patterns | ✅ In use | `tlamina/__main__.py` |
| [Update Method](patterns/update-method.md) | Sequencing Patterns | ✅ In use | `update(dt)` on `Game` and every sprite |
| [Double Buffer](patterns/double-buffer.md) | Sequencing Patterns | ✅ In use (via pygame) | `pygame.display.flip()` in `tlamina/__main__.py` |
| [Flyweight](patterns/flyweight.md) | Design Patterns Revisited | ✅ In use | `tlamina/resources.py` |
| State | Design Patterns Revisited | 🗓️ Planned (phase 5) | Start, gameplay, and game over scenes |
| Type Object | Behavioral Patterns | 🗓️ Planned (phase 5) | Waves and enemy types defined as data |
| Observer | Design Patterns Revisited | 🤔 Under consideration | Decoupling audio and effects from collisions |

## Considered and left out

| Pattern | Why not |
|---|---|
| [Object Pool](https://gameprogrammingpatterns.com/object-pool.html) | Fewer than 20 lasers are alive at once, so allocating them is not a measurable cost. A pool would add reset logic for no gain. |
| [Component](https://gameprogrammingpatterns.com/component.html) / ECS | Every entity has a fixed, small set of behaviors. Plain sprite classes are easier to read at this size (~400 lines). |
| [Spatial Partition](https://gameprogrammingpatterns.com/spatial-partition.html) | Collisions are checked between a few dozen sprites per frame. Brute force takes about 0.1 ms with 20 lasers on screen. |
