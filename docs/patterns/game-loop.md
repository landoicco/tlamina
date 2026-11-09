# 🔁 Game Loop

## Problem

The game has to keep running whether or not the player presses anything: the fleet moves, lasers fly, timers count down, and stars drift even while paused. It also has to run at the same speed on a fast desktop and a slow laptop.

## Pattern

> A game loop runs continuously during gameplay. Each turn of the loop, it processes user input without blocking, updates the game state, and renders the game. It tracks the passage of time to control the rate of gameplay.

— [*Game Programming Patterns*, "Game Loop"](https://gameprogrammingpatterns.com/game-loop.html)

The book compares several ways to handle time. Tlamina uses a **variable time step with a frame cap**: each update receives the real time since the previous frame (`dt`), and the loop sleeps to stay at or below 60 FPS.

## In Tlamina

`tlamina/__main__.py`:

```python
while running:
    for event in pygame.event.get():   # input, non-blocking
        scene = scene.handle_event(event)
    background.update(dt)               # simulation
    scene = scene.update(dt)
    background.draw(screen)             # rendering
    scene.draw(screen)
    crt.draw(screen)
    pygame.display.flip()
    dt = min(clock.tick(FPS) / 1000, MAX_DT)
```

The loop runs the current [scene](state.md) rather than the game directly, so the same loop serves the splash, the game, and the pause and game over screens.

- `clock.tick(FPS)` sleeps to cap the frame rate and returns the elapsed milliseconds.
- `MAX_DT` (0.05 s) clamps long frames, for example while the window is being dragged, so objects can't jump through each other.
- All speeds in `settings.py` are in pixels per second, so movement is `speed * dt`.

## Trade-offs

- ✅ Simple, and the game plays the same at 30, 60, or 144 FPS. `test_fleet_movement_does_not_depend_on_frame_rate` checks this.
- ⚠️ The book warns that variable time steps make the simulation **non-deterministic**: rounding differs with frame timing. This is fine for a single-player arcade game. Tests stay deterministic by passing a fixed `dt`.
- ⚠️ A step that bypasses `dt` reintroduces frame-rate dependence. Fleet bounces hit this: the overshoot past the edge grew with the frame time, so `Game.enemy_bounce` reflects it back. The arrow charge and every power-up timer count `dt` too, so they last the same at any frame rate.
- ❌ Not used: **fixed update time step with variable rendering**, the book's most robust option. It would make the simulation reproducible, but it needs interpolation when rendering, which this game doesn't need yet.
