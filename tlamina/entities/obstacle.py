from random import choice

import pygame

from tlamina.resources import load_sprite
from tlamina.settings import OBSTACLE_SPRITES


class Rock(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = load_sprite(choice(OBSTACLE_SPRITES))
        self.rect = self.image.get_rect(center=pos)
