import pygame
import pytest

from tlamina.settings import (
    EXPLOSION_LIFE,
    EXPLOSION_PARTICLES,
    FLOATING_TEXT_SPEED,
    FLOATING_TEXT_TIME,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SHAKE_STRENGTH,
    SHAKE_TIME,
    SPARK_TIME,
)
from tlamina.visuals.effects import Effects, FloatingText, Particle


def run(effects, seconds, fps=60):
    for _ in range(round(seconds * fps)):
        effects.update(1 / fps)


def test_an_explosion_adds_colored_and_white_particles():
    effects = Effects()

    effects.explosion((100, 100), (255, 0, 0))

    colors = [item.color for item in effects.items]
    assert colors.count((255, 0, 0)) == EXPLOSION_PARTICLES
    assert colors.count('white') == EXPLOSION_PARTICLES // 3


def test_particles_fly_out_and_slow_down():
    particle = Particle((100, 100), 'white')
    speed_before = abs(particle.vx) + abs(particle.vy)

    particle.update(0.1)

    assert (particle.x, particle.y) != (100, 100)
    assert abs(particle.vx) + abs(particle.vy) < speed_before


def test_every_effect_disappears_after_its_lifetime():
    effects = Effects()
    effects.explosion((100, 100), 'red')
    effects.floating_text((100, 100), '+10')
    effects.spark((100, 100))

    run(effects, max(EXPLOSION_LIFE[1], FLOATING_TEXT_TIME, SPARK_TIME) + 0.1)

    assert effects.items == []


def test_floating_text_rises():
    text = FloatingText((100, 100), '+10', 'white')

    text.update(0.5)

    assert text.y == pytest.approx(100 - FLOATING_TEXT_SPEED * 0.5)


def test_the_shake_fades_out():
    effects = Effects()
    assert effects.shake_offset() == (0, 0)

    effects.shake()
    offsets = [effects.shake_offset() for _ in range(20)]
    assert all(abs(x) <= SHAKE_STRENGTH and abs(y) <= SHAKE_STRENGTH for x, y in offsets)
    assert any(offset != (0, 0) for offset in offsets)

    run(effects, SHAKE_TIME + 0.05)
    assert effects.shake_offset() == (0, 0)


def test_effects_draw_without_errors():
    surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    effects = Effects()
    effects.explosion((100, 100), 'red')
    effects.floating_text((100, 100), '+10')
    effects.spark((100, 100))

    for _ in range(30):
        effects.update(1 / 60)
        effects.draw(surface)
