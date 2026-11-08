# 🪶 Flyweight

## Problem

Every laser, UFO, and meteor needs an image. Before this pattern was applied, each new laser read and decoded its PNG from disk, several times per second during play. The pixels were identical every time.

## Pattern

> Flyweight, like its name implies, comes into play when you have objects that need to be more lightweight, generally because you have too many of them. [...] The pattern solves that by separating out an object's data into two kinds. The first kind of data is the stuff that's not specific to a single instance of that object and can be shared across all of them [...] The rest of the data is the extrinsic state, the stuff that is unique to that instance.

— [*Game Programming Patterns*, "Flyweight"](https://gameprogrammingpatterns.com/flyweight.html)

## In Tlamina

| | Data | Where |
|---|---|---|
| **Intrinsic** (shared) | Image pixels, sound samples | `resources.load_image()`, `resources.load_sound()` |
| **Extrinsic** (per object) | Position (`rect`), speed, point value | Each sprite instance |

`resources.py` caches every loaded asset with `functools.cache`, so all 15 UFOs of the same color, and every laser ever fired, share one surface:

```python
@cache
def load_image(relative_path):
    return pygame.image.load(asset_path(relative_path)).convert_alpha()
```

Sounds are cached by `(path, volume)`, since the volume is stored on the sound object itself.

## Trade-offs

- ✅ Each file is read from disk once per run.
- ⚠️ **Shared surfaces must not be modified.** Drawing on a cached image would change it for every sprite that uses it. `CRT` only draws its scanlines on a scaled copy.
- ⚠️ Downward lasers call `pygame.transform.flip()` on each shot, which creates a new 13×54 surface every time. It's cheap, but the flipped image could be cached as well.
- ❌ The cache never evicts anything. That's fine because the full asset set fits in a few megabytes.
