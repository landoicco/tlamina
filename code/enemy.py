from random import choice

import pygame

from resources import load_silhouette, load_sprite
from settings import ENEMY_FLASH_TIME, ENEMY_POINTS, SCREEN_WIDTH, UFO_SPEED, UFO_SPRITES, UFO_Y


def enemy_sprite(color, model):
    return f'enemy{color.capitalize()}{model}'


class Enemy(pygame.sprite.Sprite):
    def __init__(self, color, model, x, y, health=1):
        super().__init__()
        name = enemy_sprite(color, model)
        self.normal_image = load_sprite(name)
        self.flash_image = load_silhouette(name)
        self.image = self.normal_image
        self.rect = self.image.get_frect(topleft=(x, y))
        self.value = ENEMY_POINTS[color]
        self.health = health
        self.flash_left = 0

    def hit(self):
        """Take one hit and return whether it destroyed the enemy."""
        self.health -= 1
        if self.health <= 0:
            self.kill()
            return True
        self.image = self.flash_image
        self.flash_left = ENEMY_FLASH_TIME
        return False

    def update(self, x_speed, dt):
        self.rect.x += x_speed * dt
        if self.flash_left > 0:
            self.flash_left -= dt
            if self.flash_left <= 0:
                self.image = self.normal_image


class Ufo(pygame.sprite.Sprite):
    def __init__(self, side):
        super().__init__()
        self.image = load_sprite(choice(UFO_SPRITES))
        # Start just off screen on the given side
        if side == 'right':
            self.rect = self.image.get_frect(topleft=(SCREEN_WIDTH, UFO_Y))
            self.speed = -UFO_SPEED
        else:
            self.rect = self.image.get_frect(topright=(0, UFO_Y))
            self.speed = UFO_SPEED

    def destroy(self):
        if (self.speed < 0 and self.rect.right < 0) or (self.speed > 0 and self.rect.left > SCREEN_WIDTH):
            self.kill()

    def update(self, dt):
        self.rect.x += self.speed * dt
        self.destroy()
