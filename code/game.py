from random import choice, uniform

import pygame

from enemy import Enemy, Ufo
from laser import Laser
from obstacle import Rock
from player import Player
from resources import load_sound, load_sprite
from settings import (
    ARMORED_FROM_WAVE,
    ENEMY_COLS,
    ENEMY_DROP,
    ENEMY_LASER_INTERVAL,
    ENEMY_LASER_SPEED,
    ENEMY_MODELS,
    ENEMY_ROW_COLORS,
    ENEMY_SPEED,
    ENEMY_X_DISTANCE,
    ENEMY_X_OFFSET,
    ENEMY_Y_DISTANCE,
    ENEMY_Y_OFFSET,
    OBSTACLE_AMOUNT,
    OBSTACLE_Y,
    PLAYER_LIVES,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    UFO_FIRST_SPAWN,
    UFO_POINTS,
    UFO_SPAWN,
    WAVE_BANNER_TIME,
    WAVE_FIRE_RATE_UP,
    WAVE_SPEED_UP,
)
from ui import draw_text

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

        # Enemy fleet setup
        self.enemies = pygame.sprite.Group()
        self.enemy_lasers = pygame.sprite.Group()
        self.wave = 0
        self.start_next_wave()

        # Bonus ufo setup
        self.ufo = pygame.sprite.GroupSingle()
        self.ufo_spawn_time = uniform(*UFO_FIRST_SPAWN)

        # Audio
        self.explosion_sfx = load_sound('assets/kenney/sci-fi-sounds/explosionCrunch_000.ogg', 0.5)
        self.player_hit_sfx = load_sound('assets/kenney/sci-fi-sounds/explosionCrunch_001.ogg', 0.5)
        self.laser_sfx = load_sound('assets/kenney/space-shooter-redux/sfx_laser1.ogg', 0.3)

    def update(self, dt):
        self.player.update(dt)
        self.ufo_timer(dt)
        self.enemy_shoot_timer(dt)
        self.collision_checks()
        if not self.enemies:
            self.start_next_wave()

        self.enemies.update(self.enemy_x_speed, dt)
        self.enemy_position_checker()
        self.enemy_lasers.update(dt)
        self.ufo.update(dt)
        self.wave_banner_left = max(self.wave_banner_left - dt, 0)

    def draw(self, surface):
        self.player.sprite.lasers.draw(surface)
        self.player.draw(surface)
        self.display_lives(surface)
        self.display_score(surface)
        self.enemies.draw(surface)
        self.enemy_lasers.draw(surface)
        self.obstacles.draw(surface)
        self.ufo.draw(surface)
        if self.wave_banner_left:
            draw_text(surface, f'WAVE {self.wave}', 36, center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

    def create_multiple_obstacles(self, x_start, y_start, *offset):
        for offset_x in offset:
            new_obstacle = Rock((x_start + offset_x, y_start))
            self.obstacles.add(new_obstacle)

    def start_next_wave(self):
        # Every wave is the same formation, faster, shooting more often, and with a new enemy model
        self.wave += 1
        level = self.wave - 1
        self.enemy_x_speed = ENEMY_SPEED * WAVE_SPEED_UP**level
        self.enemy_laser_interval = ENEMY_LASER_INTERVAL / WAVE_FIRE_RATE_UP**level
        self.enemy_shoot_time = self.enemy_laser_interval
        self.enemies_setup(model=level % ENEMY_MODELS + 1, armored=self.wave >= ARMORED_FROM_WAVE)
        self.wave_banner_left = WAVE_BANNER_TIME

    def enemies_setup(self, model, armored):
        for row_index, color in enumerate(ENEMY_ROW_COLORS):
            health = 2 if armored and row_index == 0 else 1
            for col_index in range(ENEMY_COLS):
                x = col_index * ENEMY_X_DISTANCE + ENEMY_X_OFFSET
                y = row_index * ENEMY_Y_DISTANCE + ENEMY_Y_OFFSET
                self.enemies.add(Enemy(color, model, x, y, health))

    def enemy_position_checker(self):
        # Reverse once per edge hit, no matter how many enemies touch it
        if not self.enemies:
            return
        overshoot_right = max(enemy.rect.right for enemy in self.enemies) - SCREEN_WIDTH
        overshoot_left = -min(enemy.rect.left for enemy in self.enemies)
        if overshoot_right >= 0 and self.enemy_x_speed > 0:
            self.enemy_bounce(-2 * overshoot_right)
        elif overshoot_left >= 0 and self.enemy_x_speed < 0:
            self.enemy_bounce(2 * overshoot_left)

    def enemy_bounce(self, x_correction):
        # Reflect the distance travelled past the edge, so bounces don't depend on the frame rate
        for enemy in self.enemies:
            enemy.rect.x += x_correction
        self.enemy_x_speed *= -1
        self.enemy_move_down(ENEMY_DROP)

    def enemy_move_down(self, distance):
        for enemy in self.enemies:
            enemy.rect.y += distance

    def enemy_shoot_timer(self, dt):
        self.enemy_shoot_time -= dt
        if self.enemy_shoot_time <= 0:
            self.enemy_shoot()
            self.enemy_shoot_time += self.enemy_laser_interval

    def enemy_shoot(self):
        if self.enemies:
            random_enemy = choice(self.enemies.sprites())
            self.enemy_lasers.add(Laser(random_enemy.rect.center, ENEMY_LASER_SPEED, 'laserRed16'))
            self.laser_sfx.play()

    def ufo_timer(self, dt):
        self.ufo_spawn_time -= dt
        if self.ufo_spawn_time <= 0:
            self.ufo.add(Ufo(choice(['right', 'left'])))
            self.ufo_spawn_time = uniform(*UFO_SPAWN)

    def collision_checks(self):
        # Player lasers
        for laser in self.player.sprite.lasers:
            # Obstacle collisions
            if pygame.sprite.spritecollide(laser, self.obstacles, True):
                laser.kill()

            # Enemy collisions; armored enemies survive their first hit
            enemies_hit = pygame.sprite.spritecollide(laser, self.enemies, False)
            if enemies_hit:
                destroyed = [enemy for enemy in enemies_hit if enemy.hit()]
                for enemy in destroyed:
                    self.score += enemy.value
                if destroyed:
                    self.explosion_sfx.play()
                laser.kill()

            # Ufo collisions
            if pygame.sprite.spritecollide(laser, self.ufo, True):
                self.score += UFO_POINTS
                self.explosion_sfx.play()
                laser.kill()

        # Enemy lasers
        for laser in self.enemy_lasers:
            # Player collisions
            if pygame.sprite.spritecollide(laser, self.player, False):
                laser.kill()
                self.lives -= 1
                self.player_hit_sfx.play()
                if self.lives <= 0:
                    self.state = GAME_OVER

            # Obstacle collisions
            if pygame.sprite.spritecollide(laser, self.obstacles, True):
                laser.kill()

        # Enemies
        for enemy in self.enemies:
            pygame.sprite.spritecollide(enemy, self.obstacles, True)
            if pygame.sprite.spritecollide(enemy, self.player, False):
                self.state = GAME_OVER

    def display_lives(self, surface):
        for live in range(self.lives - 1):
            x = self.live_x_start_pos + (live * (self.live_surface.get_size()[0] + 5))
            surface.blit(self.live_surface, (x, 15))

    def display_score(self, surface):
        score_surface = self.font.render(f'Score: {self.score}', False, 'white')
        score_rect = score_surface.get_rect(topleft=(5, 5))
        surface.blit(score_surface, score_rect)
