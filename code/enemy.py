import pygame

from resources import asset_path


class Ufo(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        file_path = asset_path(f'sprites/ufo/{color}.png')
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

        if color == 'red':
            self.value = 10
        elif color == 'yellow':
            self.value = 20
        else:
            self.value = 30

    def update(self, x_speed):
        self.rect.x += x_speed


class Alien(pygame.sprite.Sprite):
    def __init__(self, side, screen_width, y_offset):
        super().__init__()
        self.image = pygame.image.load(asset_path('sprites/alien/black.png')).convert_alpha()
        if side == 'right':
            x = screen_width + 80
            self.speed = -3
        else:
            x = -50
            self.speed = 3
        self.rect = self.image.get_rect(topleft=(x, y_offset))

    def update(self):
        self.rect.x += self.speed
