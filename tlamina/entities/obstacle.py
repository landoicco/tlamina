from random import choice

import pygame

from tlamina.resources import load_sprite
from tlamina.settings import OBSTACLE_SPRITES


class Rock(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        name = choice(OBSTACLE_SPRITES)
        self.image = load_sprite(name)
        self.rect = self.image.get_rect(center=pos)
        # 'meteorBrown' or 'meteorGrey', for the color of its debris
        self.material = name.split('_')[0]
