from random import randint, uniform

import pygame

from tlamina.resources import load_image
from tlamina.settings import BACKGROUND_DARKEN, SCREEN_HEIGHT, SCREEN_WIDTH, STAR_AMOUNT, STAR_SPEED


class Background:
    """The tiled space background, with stars drifting down to suggest the ship moving forward."""

    def __init__(self):
        self.image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        tile = load_image('assets/kenney/space-shooter-redux/darkPurple.png')
        for x in range(0, SCREEN_WIDTH, tile.get_width()):
            for y in range(0, SCREEN_HEIGHT, tile.get_height()):
                self.image.blit(tile, (x, y))
        # Darken it once here, so the sprites keep their contrast
        shade = pygame.Surface(self.image.get_size())
        shade.set_alpha(BACKGROUND_DARKEN)
        self.image.blit(shade, (0, 0))

        # Each star is [x, y, speed]; faster stars look closer, so they are brighter
        self.stars = [[uniform(0, SCREEN_WIDTH), uniform(0, SCREEN_HEIGHT), uniform(*STAR_SPEED)] for _ in range(STAR_AMOUNT)]

    def update(self, dt):
        for star in self.stars:
            star[1] += star[2] * dt
            if star[1] > SCREEN_HEIGHT:
                star[0], star[1] = randint(0, SCREEN_WIDTH), 0

    def draw(self, surface):
        surface.blit(self.image, (0, 0))
        low, high = STAR_SPEED
        for x, y, speed in self.stars:
            brightness = round(90 + 130 * (speed - low) / (high - low))
            surface.fill((brightness, brightness, brightness), (x, y, 2, 2))
