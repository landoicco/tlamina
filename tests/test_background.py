import pygame

from tlamina.settings import SCREEN_HEIGHT, SCREEN_WIDTH, STAR_AMOUNT, STAR_SPEED
from tlamina.visuals.background import Background


def test_stars_drift_down():
    background = Background()
    before = [star[1] for star in background.stars]

    background.update(0.1)

    # A star near the bottom may have wrapped to the top, so compare the ones that didn't
    moved = [after - y for y, (_, after, _) in zip(before, background.stars, strict=True) if after > y]
    assert len(moved) >= STAR_AMOUNT * 0.8
    assert all(STAR_SPEED[0] * 0.1 <= distance <= STAR_SPEED[1] * 0.1 + 1e-9 for distance in moved)


def test_stars_wrap_to_the_top():
    background = Background()
    background.stars = [[100, SCREEN_HEIGHT - 1, STAR_SPEED[1]]]

    background.update(1)

    x, y, _ = background.stars[0]
    assert y == 0
    assert 0 <= x <= SCREEN_WIDTH


def test_background_covers_the_screen():
    surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    surface.fill('red')

    Background().draw(surface)

    for corner in [(0, 0), (SCREEN_WIDTH - 1, 0), (0, SCREEN_HEIGHT - 1), (SCREEN_WIDTH - 1, SCREEN_HEIGHT - 1)]:
        assert surface.get_at(corner) != pygame.Color('red')
