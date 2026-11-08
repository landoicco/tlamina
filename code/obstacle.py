import pygame

from resources import load_sprite


class Rock(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = load_sprite('meteorBrown_big2')
        self.rect = self.image.get_rect(center=pos)
