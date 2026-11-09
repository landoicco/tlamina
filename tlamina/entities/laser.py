from math import radians, tan

import pygame

from tlamina.resources import load_sprite
from tlamina.settings import ARROW_DAMAGE, ARROW_SCALE, ARROW_SPEED, SCREEN_HEIGHT, SCREEN_WIDTH, SPRITE_SCALE


class Shot:
    """One press of the trigger, which may fire several lasers at once.

    The combo needs it: a shot is a miss only if none of its lasers hit an enemy
    and at least one of them left the screen.
    """

    def __init__(self, lasers=1):
        self.remaining = lasers
        self.hit_something = False
        self.escaped = False

    @property
    def missed(self):
        return self.remaining == 0 and self.escaped and not self.hit_something


class Laser(pygame.sprite.Sprite):
    damage = 1
    pierce = False  # whether it flies on after hitting an enemy

    def __init__(self, pos, speed, sprite='laserBlue16', scale=SPRITE_SCALE, angle=0, shot=None):
        """angle is in degrees from vertical; positive leans right."""
        super().__init__()
        self.image = load_sprite(sprite, scale)
        if speed > 0:
            # Lasers moving down point down
            self.image = pygame.transform.flip(self.image, False, True)
        if angle:
            self.image = pygame.transform.rotate(self.image, -angle)
        self.rect = self.image.get_frect(center=pos)
        self.speed = speed
        self.x_speed = abs(speed) * tan(radians(angle))
        self.shot = shot or Shot()

    def kill(self):
        if self.alive():
            self.shot.remaining -= 1
        super().kill()

    def destroy(self):
        off_screen = self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT
        if off_screen or self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.shot.escaped = True
            self.kill()

    def update(self, dt):
        self.rect.x += self.x_speed * dt
        self.rect.y += self.speed * dt
        self.destroy()


class Arrow(Laser):
    """The charged shot: bigger, faster, and it flies through enemies instead of stopping."""

    damage = ARROW_DAMAGE
    pierce = True

    def __init__(self, pos):
        super().__init__(pos, ARROW_SPEED, 'laserBlue12', ARROW_SCALE)
