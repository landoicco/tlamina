# 🔁 Game Loop

## Problem

The game has to keep running whether or not the player presses anything: UFOs move, lasers fly, timers count down. It also has to run at the same speed on a fast desktop and a slow laptop.

## Pattern

> A game loop runs continuously during gameplay. Each turn of the loop, it processes user input without blocking, updates the game state, and renders the game. It tracks the passage of time to control the rate of gameplay.

— [*Game Programming Patterns*, "Game Loop"](https://gameprogrammingpatterns.com/game-loop.html)

The book compares several ways to handle time. Tlamina uses a **variable time step with a frame cap**: each update receives the real time since the previous frame (`dt`), and the loop sleeps to stay at or below 60 FPS.

## In Tlamina

`main.py`:

```python
while running:
    for event in pygame.event.get():   # input, non-blocking
        ...
    game.update(dt)                     # simulation
    game.draw(screen)                   # rendering
    pygame.display.flip()
    dt = min(clock.tick(FPS) / 1000, MAX_DT)
```

- `clock.tick(FPS)` sleeps to cap the frame rate and returns the elapsed milliseconds.
- `MAX_DT` (0.05 s) clamps long frames, for example while the window is being dragged, so objects can't jump through each other.
- All speeds in `settings.py` are in pixels per second, so movement is `speed * dt`.

## Trade-offs

- ✅ Simple, and the game plays the same at 30, 60, or 144 FPS. `test_fleet_movement_does_not_depend_on_frame_rate` checks this.
- ⚠️ The book warns that variable time steps make the simulation **non-deterministic**: rounding differs with frame timing. This is fine for a single-player arcade game. Tests stay deterministic by passing a fixed `dt`.
- ⚠️ A step that bypasses `dt` reintroduces frame-rate dependence. Fleet bounces hit this: the overshoot past the edge grew with the frame time, so `Game.ufo_bounce` reflects it back.
- ❌ Not used: **fixed update time step with variable rendering**, the book's most robust option. It would make the simulation reproducible, but it needs interpolation when rendering, which this game doesn't need yet.
