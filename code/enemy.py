import pygame

from resources import load_image
from settings import ALIEN_SPEED, ALIEN_Y, SCREEN_WIDTH, UFO_POINTS


class Ufo(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        self.image = load_image(f'sprites/ufo/{color}.png')
        self.rect = self.image.get_rect(topleft=(x, y))
        self.value = UFO_POINTS[color]

    def update(self, x_speed):
        self.rect.x += x_speed


class Alien(pygame.sprite.Sprite):
    def __init__(self, side):
        super().__init__()
        self.image = load_image('sprites/alien/black.png')
        if side == 'right':
            x = SCREEN_WIDTH + 80
            self.speed = -ALIEN_SPEED
        else:
            x = -50
            self.speed = ALIEN_SPEED
        self.rect = self.image.get_rect(topleft=(x, ALIEN_Y))

    def destroy(self):
        if (self.speed < 0 and self.rect.right < 0) or (self.speed > 0 and self.rect.left > SCREEN_WIDTH):
            self.kill()

    def update(self):
        self.rect.x += self.speed
        self.destroy()
