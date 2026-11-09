import pygame

from tlamina.resources import load_sprite
from tlamina.settings import POWERUP_FALL_SPEED, POWERUP_SCALE, POWERUP_SPRITES, SCREEN_HEIGHT


class PowerUp(pygame.sprite.Sprite):
    """A capsule falling from where the bonus ufo was shot down, until the player catches it."""

    def __init__(self, pos, kind):
        super().__init__()
        self.kind = kind
        self.image = load_sprite(POWERUP_SPRITES[kind], POWERUP_SCALE)
        self.rect = self.image.get_frect(center=pos)

    def update(self, dt):
        self.rect.y += POWERUP_FALL_SPEED * dt
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
