import os

import pygame

from crt import CRT
from game import GAME_OVER, Game
from settings import FPS, SCREEN_HEIGHT, SCREEN_WIDTH, UFO_LASER_INTERVAL


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Tlamina')
    clock = pygame.time.Clock()
    game = Game()
    crt = CRT()

    ufo_laser_event = pygame.USEREVENT + 1
    pygame.time.set_timer(ufo_laser_event, UFO_LASER_INTERVAL)

    # Lets automated tests run the game for a fixed number of frames
    max_frames = int(os.environ.get('TLAMINA_MAX_FRAMES', '0'))
    frame = 0
    running = True

    while running and (not max_frames or frame < max_frames):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == ufo_laser_event:
                game.ufo_shoot()

        game.update()
        # No game over screen yet, so losing still closes the game
        if game.state == GAME_OVER:
            running = False

        screen.fill((0, 0, 0))
        game.draw(screen)
        crt.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)
        frame += 1

    pygame.quit()


if __name__ == '__main__':
    main()
