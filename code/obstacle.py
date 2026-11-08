import pygame

from resources import load_image


class Rock(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = load_image('sprites/obstacles/meteor_big_brown_1.png')
        self.rect = self.image.get_rect(center=pos)
