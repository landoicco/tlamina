import pygame

from tlamina.resources import load_sprite
from tlamina.settings import ARROW_DAMAGE, ARROW_SCALE, ARROW_SPEED, SCREEN_HEIGHT, SPRITE_SCALE


class Laser(pygame.sprite.Sprite):
    damage = 1
    pierce = False  # whether it flies on after hitting an enemy

    def __init__(self, pos, speed, sprite='laserBlue16', scale=SPRITE_SCALE):
        super().__init__()
        self.image = load_sprite(sprite, scale)
        if speed > 0:
            # Lasers moving down point down
            self.image = pygame.transform.flip(self.image, False, True)
        self.rect = self.image.get_frect(center=pos)
        self.speed = speed
        # For the combo: a player shot that escapes without hitting anything is a miss
        self.hit_something = False
        self.escaped = False

    def destroy(self):
        if self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.escaped = True
            self.kill()

    def update(self, dt):
        self.rect.y += self.speed * dt
        self.destroy()


class Arrow(Laser):
    """The charged shot: bigger, faster, and it flies through enemies instead of stopping."""

    damage = ARROW_DAMAGE
    pierce = True

    def __init__(self, pos):
        super().__init__(pos, ARROW_SPEED, 'laserBlue12', ARROW_SCALE)
