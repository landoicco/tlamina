from random import choice, uniform

import pygame

from enemy import Alien, Ufo
from laser import Laser
from obstacle import Rock
from player import Player
from resources import load_sound, load_sprite
from settings import (
    ALIEN_FIRST_SPAWN,
    ALIEN_POINTS,
    ALIEN_SPAWN,
    OBSTACLE_AMOUNT,
    OBSTACLE_Y,
    PLAYER_LIVES,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    UFO_COLS,
    UFO_DROP,
    UFO_LASER_INTERVAL,
    UFO_LASER_SPEED,
    UFO_ROW_COLORS,
    UFO_SPEED,
    UFO_X_DISTANCE,
    UFO_X_OFFSET,
    UFO_Y_DISTANCE,
    UFO_Y_OFFSET,
)

PLAYING = 'playing'
GAME_OVER = 'game_over'


class Game:
    def __init__(self):
        self.state = PLAYING

        player_sprite = Player((SCREEN_WIDTH / 2, SCREEN_HEIGHT - 5))
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # Health and score setup
        self.lives = PLAYER_LIVES
        self.live_surface = load_sprite('playerLife1_blue')
        self.live_x_start_pos = SCREEN_WIDTH - (self.live_surface.get_size()[0] * 2 + 20)
        self.score = 0
        self.font = pygame.font.Font(None, 20)

        # Obstacles setup
        self.obstacles = pygame.sprite.Group()
        obstacle_x_positions = [num * (SCREEN_WIDTH / OBSTACLE_AMOUNT) for num in range(OBSTACLE_AMOUNT)]
        self.create_multiple_obstacles(SCREEN_WIDTH / 8, OBSTACLE_Y, *obstacle_x_positions)

        # Ufo setup
        self.ufos = pygame.sprite.Group()
        self.ufos_setup()
        self.ufo_x_speed = UFO_SPEED
        self.ufo_lasers = pygame.sprite.Group()
        self.ufo_shoot_time = UFO_LASER_INTERVAL

        # Extra alien setup
        self.alien = pygame.sprite.GroupSingle()
        self.extra_spawn_time = uniform(*ALIEN_FIRST_SPAWN)

        # Audio
        self.bg_music = load_sound('assets/music/wind.mp3', 0.2)
        self.bg_music.play(loops=-1)
        self.explosion_sfx = load_sound('assets/sfx/explosion.wav', 0.5)
        self.laser_sfx = load_sound('assets/sfx/laser_1.wav', 0.3)

    def update(self, dt):
        self.player.update(dt)
        self.extra_alien_timer(dt)
        self.ufo_shoot_timer(dt)
        self.collision_checks()

        self.ufos.update(self.ufo_x_speed, dt)
        self.ufo_position_checker()
        self.ufo_lasers.update(dt)
        self.alien.update(dt)

    def draw(self, surface):
        self.player.sprite.lasers.draw(surface)
        self.player.draw(surface)
        self.display_lives(surface)
        self.display_score(surface)
        self.ufos.draw(surface)
        self.ufo_lasers.draw(surface)
        self.obstacles.draw(surface)
        self.alien.draw(surface)

    def create_multiple_obstacles(self, x_start, y_start, *offset):
        for offset_x in offset:
            new_obstacle = Rock((x_start + offset_x, y_start))
            self.obstacles.add(new_obstacle)

    def ufo_position_checker(self):
        # Reverse once per edge hit, no matter how many ufo's touch it
        if not self.ufos:
            return
        overshoot_right = max(ufo.rect.right for ufo in self.ufos) - SCREEN_WIDTH
        overshoot_left = -min(ufo.rect.left for ufo in self.ufos)
        if overshoot_right >= 0 and self.ufo_x_speed > 0:
            self.ufo_bounce(-2 * overshoot_right)
        elif overshoot_left >= 0 and self.ufo_x_speed < 0:
            self.ufo_bounce(2 * overshoot_left)

    def ufo_bounce(self, x_correction):
        # Reflect the distance travelled past the edge, so bounces don't depend on the frame rate
        for ufo in self.ufos:
            ufo.rect.x += x_correction
        self.ufo_x_speed *= -1
        self.ufo_move_down(UFO_DROP)

    def ufo_move_down(self, distance):
        for ufo in self.ufos:
            ufo.rect.y += distance

    def ufo_shoot_timer(self, dt):
        self.ufo_shoot_time -= dt
        if self.ufo_shoot_time <= 0:
            self.ufo_shoot()
            self.ufo_shoot_time += UFO_LASER_INTERVAL

    def ufo_shoot(self):
        if self.ufos:
            random_ufo = choice(self.ufos.sprites())
            self.ufo_lasers.add(Laser(random_ufo.rect.center, UFO_LASER_SPEED))
            self.laser_sfx.play()

    def ufos_setup(self):
        for row_index, color in enumerate(UFO_ROW_COLORS):
            for col_index in range(UFO_COLS):
                x = col_index * UFO_X_DISTANCE + UFO_X_OFFSET
                y = row_index * UFO_Y_DISTANCE + UFO_Y_OFFSET
                self.ufos.add(Ufo(color, x, y))

    def extra_alien_timer(self, dt):
        self.extra_spawn_time -= dt
        if self.extra_spawn_time <= 0:
            self.alien.add(Alien(choice(['right', 'left'])))
            self.extra_spawn_time = uniform(*ALIEN_SPAWN)

    def collision_checks(self):
        # Player lasers
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
                self.score += ALIEN_POINTS
                self.explosion_sfx.play()
                laser.kill()

        # Ufo lasers
        for laser in self.ufo_lasers:
            # Player collisions
            if pygame.sprite.spritecollide(laser, self.player, False):
                laser.kill()
                self.lives -= 1
                if self.lives <= 0:
                    self.state = GAME_OVER

            # Obstacle collisions
            if pygame.sprite.spritecollide(laser, self.obstacles, True):
                laser.kill()

        # Ufo's
        for ufo in self.ufos:
            pygame.sprite.spritecollide(ufo, self.obstacles, True)
            if pygame.sprite.spritecollide(ufo, self.player, False):
                self.state = GAME_OVER

    def display_lives(self, surface):
        for live in range(self.lives - 1):
            x = self.live_x_start_pos + (live * (self.live_surface.get_size()[0] + 5))
            surface.blit(self.live_surface, (x, 15))

    def display_score(self, surface):
        score_surface = self.font.render(f'Score: {self.score}', False, 'white')
        score_rect = score_surface.get_rect(topleft=(5, 5))
        surface.blit(score_surface, score_rect)
