import pygame

from resources import load_image


class Ufo(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        self.image = load_image(f'sprites/ufo/{color}.png')
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
        self.image = load_image('sprites/alien/black.png')
        if side == 'right':
            x = screen_width + 80
            self.speed = -3
        else:
            x = -50
            self.speed = 3
        self.rect = self.image.get_rect(topleft=(x, y_offset))
        self.screen_width = screen_width

    def destroy(self):
        if (self.speed < 0 and self.rect.right < 0) or (self.speed > 0 and self.rect.left > self.screen_width):
            self.kill()

    def update(self):
        self.rect.x += self.speed
        self.destroy()
