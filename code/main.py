import os

import pygame

from crt import CRT
from resources import load_sound
from scenes import SplashScene
from settings import FPS, MAX_DT, SCREEN_HEIGHT, SCREEN_WIDTH


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Tlamina')
    clock = pygame.time.Clock()
    scene = SplashScene()
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

        scene = scene.update(dt)

        screen.fill((0, 0, 0))
        scene.draw(screen)
        crt.draw(screen)

        pygame.display.flip()
        dt = min(clock.tick(FPS) / 1000, MAX_DT)
        frame += 1

    pygame.quit()


if __name__ == '__main__':
    main()
