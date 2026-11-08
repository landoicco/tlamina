from random import randint

import pygame

from settings import CRT_ALPHA, CRT_CORNER_RADIUS, CRT_LINE_HEIGHT, CRT_VIGNETTE_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH


class CRT:
    def __init__(self):
        self.tv = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.create_vignette()
        self.create_crt_lines()

    def create_vignette(self):
        # Start fully dark, then draw rounded rectangles from the edge inwards,
        # each one more transparent, so the borders fade like an old TV screen
        self.tv.fill((0, 0, 0, 255))
        for inset in range(1, CRT_VIGNETTE_SIZE + 1):
            alpha = round(255 * (1 - inset / CRT_VIGNETTE_SIZE) ** 2)
            rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT).inflate(-2 * inset, -2 * inset)
            radius = max(CRT_CORNER_RADIUS - inset, 0)
            pygame.draw.rect(self.tv, (0, 0, 0, alpha), rect, border_radius=radius)

    def create_crt_lines(self):
        line_amount = int(SCREEN_HEIGHT / CRT_LINE_HEIGHT)
        for line in range(line_amount):
            y_pos = line * CRT_LINE_HEIGHT
            pygame.draw.line(self.tv, 'black', (0, y_pos), (SCREEN_WIDTH, y_pos), 1)

    def draw(self, surface):
        self.tv.set_alpha(randint(*CRT_ALPHA))
        surface.blit(self.tv, (0, 0))
