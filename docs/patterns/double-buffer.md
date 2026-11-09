# 🖼️ Double Buffer

## Problem

Each frame is drawn in several steps: the background, the sprites and effects, the HUD, any pause or game over text, then the CRT overlay. If the monitor showed the screen in the middle of that, the player would see flicker and half-drawn frames.

## Pattern

> A buffered class encapsulates a buffer: a piece of state that can be modified. This buffer is edited incrementally, but we want all outside code to see the edit as a single atomic change. To do this, the class keeps two instances of the buffer: a next buffer and a current buffer.

— [*Game Programming Patterns*, "Double Buffer"](https://gameprogrammingpatterns.com/double-buffer.html)

## In Tlamina

This is the one pattern the game gets for free. The surface returned by `pygame.display.set_mode()` is the **next buffer**: everything is drawn there, and the monitor only sees it after `pygame.display.flip()` swaps the buffers.

```python
background.draw(screen)  # cover the whole next buffer
scene.draw(screen)       # sprites, effects, HUD, and any overlay text
crt.draw(screen)         # the CRT filter on top
pygame.display.flip()    # swap: the finished frame becomes visible
```

The whole frame is redrawn every time, so there is no state left over from the previous frame to track.

## Trade-offs

- ✅ No flicker or partial frames, with no code of our own.
- ⚠️ Redrawing the full 800×800 screen every frame does more work than strictly needed. A busy frame, with explosions, power-ups, and 20 lasers on screen, takes about 6 ms to draw (median; 11 ms at the 95th percentile), background and CRT overlay included, out of the 16.7 ms available at 60 FPS, and it keeps the drawing code trivial.
- ❌ Not used: **dirty rectangles** (`pygame.display.update(rects)`), which only redraw the areas that changed. The CRT overlay covers the whole screen every frame, so every pixel is dirty anyway.
- ❌ Not used: double-buffering **game state**, the book's other use case. Collisions read and write the same groups in a fixed order (see [Update Method](update-method.md)), which is deterministic enough for this game.
