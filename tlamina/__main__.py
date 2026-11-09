import os

import pygame

from tlamina.resources import load_sound, load_sprite
from tlamina.scenes import SplashScene
from tlamina.settings import FPS, MAX_DT, SCREEN_HEIGHT, SCREEN_WIDTH
from tlamina.visuals.background import Background
from tlamina.visuals.crt import CRT


def window_icon():
    """The player ship centered on a transparent square, the same image as assets/icon.ico."""
    ship = load_sprite('playerShip1_blue', 1)
    icon = pygame.Surface((max(ship.get_size()),) * 2, pygame.SRCALPHA)
    icon.blit(ship, ship.get_rect(center=icon.get_rect().center))
    return icon


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Tlamina')
    pygame.display.set_icon(window_icon())
    clock = pygame.time.Clock()
    scene = SplashScene()
    background = Background()
    crt = CRT()

    # Started once here, so it keeps playing across scenes and new runs
    load_sound('assets/music/spacecrusher.ogg', 0.2).play(loops=-1)

    # Lets automated tests run the game for a fixed number of frames
    max_frames = int(os.environ.get('TLAMINA_MAX_FRAMES', '0'))
    frame = 0
    running = True
    dt = 0

    while running and (not max_frames or frame < max_frames):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                scene = scene.handle_event(event)

        # The background keeps drifting in every scene, even while paused
        background.update(dt)
        scene = scene.update(dt)

        background.draw(screen)
        scene.draw(screen)
        crt.draw(screen)

        pygame.display.flip()
        dt = min(clock.tick(FPS) / 1000, MAX_DT)
        frame += 1

    pygame.quit()


if __name__ == '__main__':
    main()
