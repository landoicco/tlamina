# 🪶 Flyweight

## Problem

Every laser, enemy, meteor, and particle effect needs an image. Before this pattern was applied, each new laser read and decoded its PNG from disk, several times per second during play. The pixels were identical every time.

## Pattern

> Flyweight, like its name implies, comes into play when you have objects that need to be more lightweight, generally because you have too many of them. [...] The pattern solves that by separating out an object's data into two kinds. The first kind of data is the stuff that's not specific to a single instance of that object and can be shared across all of them [...] The rest of the data is the extrinsic state, the stuff that is unique to that instance.

— [*Game Programming Patterns*, "Flyweight"](https://gameprogrammingpatterns.com/flyweight.html)

## In Tlamina

| | Data | Where |
|---|---|---|
| **Intrinsic** (shared) | Image pixels, hit-flash silhouettes, sound samples, fonts | `resources.load_sprite()`, `load_silhouette()`, `load_sound()`, `load_font()` |
| **Extrinsic** (per object) | Position (`rect`), speed, health, point value | Each sprite instance |

`resources.py` caches every loaded asset with `functools.cache`, so all enemies of the same color and model, and every laser ever fired, share one surface:

```python
@cache
def load_sprite(name, scale=SPRITE_SCALE):
    sprite = load_image('assets/atlas.png').subsurface(index[name])
    ...
```

The sharing goes one level further with a **texture atlas**: every sprite comes from a single image, `assets/atlas.png`, built by [`tools/build_atlas.py`](../../tools/README.md). The game reads one file at startup, and each sprite is cut out of it, and scaled by `SPRITE_SCALE`, the first time it's requested.

Sounds are cached by `(path, volume)`, since the volume is stored on the sound object itself.

## Trade-offs

- ✅ The atlas is read from disk once per run, and each sprite is cut and scaled once.
- ✅ Changing `SPRITE_SCALE` resizes every sprite without touching the art.
- ⚠️ **Shared surfaces must not be modified.** Drawing on a cached image would change it for every sprite that uses it. `CRT` draws its vignette and scanlines on a surface of its own instead, and the player's damage cracks are drawn on a copy of the ship.
- ⚠️ Downward and angled lasers call `pygame.transform.flip()` or `rotate()` on each shot, which creates a new small surface every time. It's cheap, but those images could be cached as well.
- ❌ The cache never evicts anything. That's fine because the full asset set fits in a few megabytes.
