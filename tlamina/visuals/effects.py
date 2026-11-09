from math import cos, sin, tau
from random import uniform

from tlamina.resources import load_font, load_sprite
from tlamina.settings import (
    EXPLOSION_DRAG,
    EXPLOSION_LIFE,
    EXPLOSION_PARTICLES,
    EXPLOSION_SPEED,
    FLOATING_TEXT_SIZE,
    FLOATING_TEXT_SPEED,
    FLOATING_TEXT_TIME,
    SHAKE_STRENGTH,
    SHAKE_TIME,
    SPARK_TIME,
)


class Particle:
    """A square flying out of an explosion, slowing down and shrinking until it's gone."""

    def __init__(self, pos, color):
        angle = uniform(0, tau)
        speed = uniform(*EXPLOSION_SPEED)
        self.x, self.y = pos
        self.vx, self.vy = cos(angle) * speed, sin(angle) * speed
        self.life = self.max_life = uniform(*EXPLOSION_LIFE)
        self.color = color

    @property
    def alive(self):
        return self.life > 0

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        damping = EXPLOSION_DRAG**dt
        self.vx *= damping
        self.vy *= damping
        self.life -= dt

    def draw(self, surface):
        size = max(1, round(4 * self.life / self.max_life))
        surface.fill(self.color, (self.x - size / 2, self.y - size / 2, size, size))


class FloatingText:
    """Text that rises from where something happened and fades out, like the points of a kill."""

    def __init__(self, pos, text, color):
        self.image = load_font(FLOATING_TEXT_SIZE).render(text, True, color)
        self.x, self.y = pos
        self.life = FLOATING_TEXT_TIME

    @property
    def alive(self):
        return self.life > 0

    def update(self, dt):
        self.y -= FLOATING_TEXT_SPEED * dt
        self.life -= dt

    def draw(self, surface):
        # Fully visible for the first half, then fading
        self.image.set_alpha(round(255 * min(1, 2 * self.life / FLOATING_TEXT_TIME)))
        surface.blit(self.image, self.image.get_rect(center=(self.x, self.y)))


class Spark:
    """A short flash where a laser hits something that doesn't explode."""

    def __init__(self, pos):
        self.image = load_sprite('laserBlue08')
        self.pos = pos
        self.life = SPARK_TIME

    @property
    def alive(self):
        return self.life > 0

    def update(self, dt):
        self.life -= dt

    def draw(self, surface):
        surface.blit(self.image, self.image.get_rect(center=self.pos))


class Effects:
    """Everything purely visual that happens in the game world. None of it affects the game."""

    def __init__(self):
        self.items = []
        self.shake_left = 0

    def explosion(self, pos, color, amount=EXPLOSION_PARTICLES):
        # A few white particles make the center look hot
        self.items += [Particle(pos, color) for _ in range(amount)]
        self.items += [Particle(pos, 'white') for _ in range(amount // 3)]

    def floating_text(self, pos, text, color='white'):
        self.items.append(FloatingText(pos, text, color))

    def spark(self, pos):
        self.items.append(Spark(pos))

    def shake(self):
        self.shake_left = SHAKE_TIME

    def shake_offset(self):
        if self.shake_left <= 0:
            return (0, 0)
        strength = SHAKE_STRENGTH * self.shake_left / SHAKE_TIME
        return (round(uniform(-strength, strength)), round(uniform(-strength, strength)))

    def update(self, dt):
        for item in self.items:
            item.update(dt)
        self.items = [item for item in self.items if item.alive]
        self.shake_left = max(self.shake_left - dt, 0)

    def draw(self, surface):
        for item in self.items:
            item.draw(surface)
