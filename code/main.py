import sys
import pygame
from player import Player
from obstacle import Rock
from enemy import Ufo, Alien
from random import choice, randint
from laser import Laser


class Game:
    def __init__(self):
        player_sprite = Player((screen_width / 2, screen_height - 5), screen_width, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # Health and score setup
        self.lives = 3
        self.live_surface = pygame.image.load('../sprites/hud/playerlifes/blue.png').convert_alpha()
        self.live_x_start_pos = screen_width - (self.live_surface.get_size()[0] * 2 + 20)
        self.score = 0
        self.font = pygame.font.Font(None, 20)

        # Obstacles setup
        self.obstacles = pygame.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_positions = [num * (screen_width / self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacles(screen_width / 8, 650, *self.obstacle_x_positions)

        # Ufo setup
        self.ufos = pygame.sprite.Group()
        self.ufos_setup(3, 5, x_offset=50, y_offset=130)
        self.ufo_x_speed = 1
        self.ufo_lasers = pygame.sprite.Group()

        # Extra alien setup
        self.alien = pygame.sprite.GroupSingle()
        self.extra_spawn_time = randint(40, 80)

        # Audio
        self.bg_music = pygame.mixer.Sound('../assets/music/wind.mp3')
        self.bg_music.set_volume(0.2)
        self.bg_music.play(loops=-1)
        self.explosion_sfx = pygame.mixer.Sound('../assets/sfx/explosion.wav')
        self.explosion_sfx.set_volume(0.5)
        self.laser_sfx = pygame.mixer.Sound('../assets/sfx/laser_1.wav')
        self.laser_sfx.set_volume(0.3)

    def run(self):
        self.player.update()
        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)

        self.extra_alien_timer()
        self.collision_checks()
        self.display_lives()
        self.display_score()

        self.ufos.update(self.ufo_x_speed)
        self.ufo_position_checker()
        self.ufos.draw(screen)
        self.ufo_lasers.update()
        self.ufo_lasers.draw(screen)

        self.obstacles.draw(screen)
        self.alien.draw(screen)
        self.alien.update()

    def create_multiple_obstacles(self, x_start, y_start, *offset):
        for offset_x in offset:
            new_obstacle = Rock((x_start + offset_x,
                                 y_start))
            self.obstacles.add(new_obstacle)

    def ufo_position_checker(self):
        all_ufos = self.ufos.sprites()
        for ufo in all_ufos:
            if ufo.rect.left <= 0 or ufo.rect.right >= screen_width:
                # Invert direction of ufo's
                self.ufo_x_speed *= -1
                self.ufo_move_down(3)

    def ufo_move_down(self, distance):
        if self.ufos:
            all_ufos = self.ufos.sprites()
            for ufo in all_ufos:
                ufo.rect.y += distance

    def ufo_shoot(self):
        if self.ufos.sprites():
            random_ufo = choice(self.ufos.sprites())
            laser_sprite = Laser(random_ufo.rect.center, 6, screen_height)
            self.ufo_lasers.add(laser_sprite)
            self.laser_sfx.play()

    def ufos_setup(self, rows, cols, x_distance=120, y_distance=120, x_offset=120, y_offset=50):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset
                if row_index == 0:
                    ufo_sprite = Ufo('yellow', x, y)
                elif 1 <= row_index < 2:
                    ufo_sprite = Ufo('green', x, y)
                else:
                    ufo_sprite = Ufo('red', x, y)
                self.ufos.add(ufo_sprite)

    def extra_alien_timer(self):
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
            self.alien.add(Alien(choice(['right', 'left']), screen_width, 15))
            self.extra_spawn_time = randint(400, 800)

    def collision_checks(self):

        # Player lasers
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                # Obstacle collisions
                if pygame.sprite.spritecollide(laser, self.obstacles, True):
                    laser.kill()

                # Ufo collisions
                ufos_hit = pygame.sprite.spritecollide(laser, self.ufos, True)
                if ufos_hit:
                    for ufo in ufos_hit:
                        self.score += ufo.value
                    self.explosion_sfx.play()
                    laser.kill()

                # Alien collisions
                if pygame.sprite.spritecollide(laser, self.alien, True):
                    self.score += 100
                    self.explosion_sfx.play()
                    laser.kill()

        # Ufo lasers
        if self.ufo_lasers:
            for laser in self.ufo_lasers:
                # Player collisions
                if pygame.sprite.spritecollide(laser, self.player, False):
                    laser.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        pygame.quit()
                        sys.exit()

                # Obstacle collisions
                if pygame.sprite.spritecollide(laser, self.obstacles, True):
                    laser.kill()

        # Ufo's
        if self.ufos:
            for ufo in self.ufos:
                pygame.sprite.spritecollide(ufo, self.obstacles, True)
                if pygame.sprite.spritecollide(ufo, self.player, False):
                    pygame.quit()
                    sys.exit()

    def display_lives(self):
        for live in range(self.lives - 1):
            x = self.live_x_start_pos + (live * (self.live_surface.get_size()[0] + 5))
            screen.blit(self.live_surface, (x, 15))

    def display_score(self):
        score_surface = self.font.render(f'Score: {self.score}', False, 'white')
        score_rect = score_surface.get_rect(topleft=(5, 5))
        screen.blit(score_surface, score_rect)


class CRT:
    def __init__(self):
        self.tv = pygame.image.load('../sprites/tv.png').convert_alpha()
        self.tv = pygame.transform.scale(self.tv, (screen_width, screen_height))

    def create_crt_lines(self):
        line_height = 3
        line_amount = int(screen_height / line_height)
        for line in range(line_amount):
            y_pos = line * line_height
            pygame.draw.line(self.tv, 'black', (0, y_pos), (screen_width, y_pos), 1)

    def draw(self):
        self.tv.set_alpha(randint(80, 90))
        self.create_crt_lines()
        screen.blit(self.tv, (0, 0))


if __name__ == '__main__':
    pygame.init()
    screen_width = 800
    screen_height = 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Tlamina')
    clock = pygame.time.Clock()
    game = Game()
    crt = CRT()

    UFO_LASER = pygame.USEREVENT + 1
    pygame.time.set_timer(UFO_LASER, 800)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == UFO_LASER:
                game.ufo_shoot()

        screen.fill((0, 0, 0))
        game.run()
        crt.draw()

        pygame.display.flip()
        clock.tick(60)
