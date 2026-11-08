from random import randint

import pygame

from resources import load_image
from settings import CRT_ALPHA, CRT_LINE_HEIGHT, SCREEN_HEIGHT, SCREEN_WIDTH


class CRT:
    def __init__(self):
        self.tv = load_image('sprites/tv.png')
        self.tv = pygame.transform.scale(self.tv, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.create_crt_lines()

    def create_crt_lines(self):
        line_amount = int(SCREEN_HEIGHT / CRT_LINE_HEIGHT)
        for line in range(line_amount):
            y_pos = line * CRT_LINE_HEIGHT
            pygame.draw.line(self.tv, 'black', (0, y_pos), (SCREEN_WIDTH, y_pos), 1)

    def draw(self, surface):
        self.tv.set_alpha(randint(*CRT_ALPHA))
        surface.blit(self.tv, (0, 0))
