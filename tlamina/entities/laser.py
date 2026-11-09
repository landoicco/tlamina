import pygame

from tlamina.resources import load_sprite
from tlamina.settings import SCREEN_HEIGHT


class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, speed, sprite='laserBlue16'):
        super().__init__()
        self.image = load_sprite(sprite)
        if speed > 0:
            # Lasers moving down point down
            self.image = pygame.transform.flip(self.image, False, True)
        self.rect = self.image.get_frect(center=pos)
        self.speed = speed

    def destroy(self):
        if self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()

    def update(self, dt):
        self.rect.y += self.speed * dt
        self.destroy()
