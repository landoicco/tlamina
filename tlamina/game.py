from random import choice, uniform

import pygame

from tlamina.entities.enemy import Enemy, Ufo
from tlamina.entities.laser import Laser
from tlamina.entities.obstacle import Rock
from tlamina.entities.player import Player
from tlamina.entities.powerup import PowerUp
from tlamina.resources import load_sound, load_sprite
from tlamina.settings import (
    ARMORED_FROM_WAVE,
    COMBO_COLOR,
    COMBO_MAX,
    COMBO_STEP,
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
    EXPLOSION_COLORS,
    EXPLOSION_PARTICLES,
    FIRST_WAVE_BANNER_TIME,
    HUD_FONT_SIZE,
    HUD_MARGIN,
    OBSTACLE_AMOUNT,
    OBSTACLE_Y,
    PLAYER_LIVES,
    PLAYER_Y,
    POWERUP_COLORS,
    POWERUP_NAMES,
    POWERUP_SPRITES,
    POWERUP_TIME,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    UFO_FIRST_SPAWN,
    UFO_POINTS,
    UFO_SPAWN,
    WAVE_BANNER_TIME,
    WAVE_FIRE_RATE_UP,
    WAVE_SPEED_UP,
)
from tlamina.visuals.effects import Effects
from tlamina.visuals.ui import draw_text

PLAYING = 'playing'
GAME_OVER = 'game_over'


class Game:
    def __init__(self):
        self.state = PLAYING

        player_sprite = Player((SCREEN_WIDTH / 2, PLAYER_Y))
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # Health and score setup
        self.lives = PLAYER_LIVES
        self.life_icon = load_sprite('playerLife1_blue')
        self.score = 0
        self.combo_hits = 0

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
        self.powerups = pygame.sprite.Group()
        self.ufo_spawn_time = uniform(*UFO_FIRST_SPAWN)

        # Effects are drawn on a layer of their own with the rest of the world, so it can shake under the HUD
        self.effects = Effects()
        self.world = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

        # Audio
        self.explosion_sfx = load_sound('assets/kenney/sci-fi-sounds/explosionCrunch_000.ogg', 0.5)
        self.player_hit_sfx = load_sound('assets/kenney/sci-fi-sounds/explosionCrunch_001.ogg', 0.5)
        self.laser_sfx = load_sound('assets/kenney/space-shooter-redux/sfx_laser1.ogg', 0.3)
        self.combo_sfx = load_sound('assets/kenney/space-shooter-redux/sfx_twoTone.ogg', 0.4)
        self.powerup_sfx = load_sound('assets/kenney/space-shooter-redux/sfx_zap.ogg', 0.5)
        self.shield_up_sfx = load_sound('assets/kenney/space-shooter-redux/sfx_shieldUp.ogg', 0.5)
        self.shield_down_sfx = load_sound('assets/kenney/space-shooter-redux/sfx_shieldDown.ogg', 0.5)

    def update(self, dt):
        lasers_before = set(self.player.sprite.lasers)
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
        self.powerups.update(dt)
        self.effects.update(dt)
        self.wave_banner_left = max(self.wave_banner_left - dt, 0)
        # Lasers can leave the screen or hit something at any point of the frame
        self.check_misses(lasers_before - set(self.player.sprite.lasers))

    def draw(self, surface):
        world = self.world
        world.fill((0, 0, 0, 0))
        self.player.sprite.lasers.draw(world)
        if self.player.sprite.visible:
            self.player.sprite.draw_engine_flame(world)
            self.player.draw(world)
            self.player.sprite.draw_shield(world)
            self.player.sprite.draw_charge_glow(world)
        self.enemies.draw(world)
        self.enemy_lasers.draw(world)
        self.obstacles.draw(world)
        self.ufo.draw(world)
        self.powerups.draw(world)
        self.effects.draw(world)
        surface.blit(world, self.effects.shake_offset())

        self.draw_hud(surface)
        if self.wave_banner_left:
            draw_text(surface, f'WAVE {self.wave}', 36, center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            if self.wave == 1:
                # Moving is obvious; the charged arrow is the one control nobody would guess
                hint = 'Tap Space to shoot, hold to charge an arrow'
                draw_text(surface, hint, 13, 'gray70', center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 40))

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
        self.wave_banner_left = FIRST_WAVE_BANNER_TIME if self.wave == 1 else WAVE_BANNER_TIME

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
            if rocks := pygame.sprite.spritecollide(laser, self.obstacles, True):
                self.break_rocks(rocks)
                laser.kill()

            # Enemy collisions; armored enemies survive a normal laser, and the arrow flies on
            enemies_hit = pygame.sprite.spritecollide(laser, self.enemies, False)
            if enemies_hit:
                laser.shot.hit_something = True
                for _ in enemies_hit:
                    self.register_hit()
                destroyed = [enemy for enemy in enemies_hit if enemy.hit(laser.damage)]
                for enemy in destroyed:
                    points = enemy.value * self.multiplier
                    self.score += points
                    self.effects.explosion(enemy.rect.center, EXPLOSION_COLORS[enemy.color])
                    self.effects.floating_text(enemy.rect.center, f'+{points}')
                if destroyed:
                    self.explosion_sfx.play()
                else:
                    self.effects.spark(laser.rect.midtop)
                if not laser.pierce:
                    laser.kill()

            # Ufo collisions
            for ufo in pygame.sprite.spritecollide(laser, self.ufo, True):
                laser.shot.hit_something = True
                self.register_hit()
                points = UFO_POINTS * self.multiplier
                self.score += points
                self.effects.explosion(ufo.rect.center, EXPLOSION_COLORS['ufo'], 2 * EXPLOSION_PARTICLES)
                self.effects.floating_text(ufo.rect.center, f'+{points}', EXPLOSION_COLORS['ufo'])
                self.explosion_sfx.play()
                self.powerups.add(PowerUp(ufo.rect.center, choice(list(POWERUP_SPRITES))))
                if not laser.pierce:
                    laser.kill()

        # Power-ups
        for powerup in pygame.sprite.spritecollide(self.player.sprite, self.powerups, True):
            self.pick_up(powerup.kind)

        # Enemy lasers
        player = self.player.sprite
        for laser in self.enemy_lasers:
            # Player collisions; while invulnerable, lasers fly through the ship
            if not player.invulnerable and pygame.sprite.spritecollide(laser, self.player, False):
                laser.kill()
                self.hit_player()

            # Obstacle collisions
            if rocks := pygame.sprite.spritecollide(laser, self.obstacles, True):
                self.break_rocks(rocks)
                laser.kill()

        # Enemies
        for enemy in self.enemies:
            self.break_rocks(pygame.sprite.spritecollide(enemy, self.obstacles, True))
            if pygame.sprite.spritecollide(enemy, self.player, False):
                self.effects.explosion(player.rect.center, EXPLOSION_COLORS['player'], 2 * EXPLOSION_PARTICLES)
                self.state = GAME_OVER

    def hit_player(self):
        player = self.player.sprite
        if player.has('shield'):
            # The shield takes the hit instead: no life lost, and the combo survives
            player.break_shield()
            self.shield_down_sfx.play()
            self.effects.explosion(player.rect.midtop, POWERUP_COLORS['shield'], EXPLOSION_PARTICLES // 2)
            return
        self.lives -= 1
        self.combo_hits = 0
        self.player_hit_sfx.play()
        self.effects.shake()
        if self.lives <= 0:
            self.effects.explosion(player.rect.center, EXPLOSION_COLORS['player'], 2 * EXPLOSION_PARTICLES)
            self.state = GAME_OVER
        else:
            self.effects.explosion(player.rect.center, EXPLOSION_COLORS['player'])
            player.take_hit(PLAYER_LIVES - self.lives)

    def pick_up(self, kind):
        self.player.sprite.apply_powerup(kind)
        (self.shield_up_sfx if kind == 'shield' else self.powerup_sfx).play()
        player = self.player.sprite
        self.effects.floating_text((player.rect.centerx, player.rect.top - 20), POWERUP_NAMES[kind], POWERUP_COLORS[kind])

    def break_rocks(self, rocks):
        for rock in rocks:
            self.effects.explosion(rock.rect.center, EXPLOSION_COLORS[rock.material], EXPLOSION_PARTICLES // 2)

    @property
    def multiplier(self):
        return min(1 + self.combo_hits // COMBO_STEP, COMBO_MAX)

    def register_hit(self):
        before = self.multiplier
        self.combo_hits += 1
        if self.multiplier > before:
            self.combo_sfx.play()
            player = self.player.sprite
            self.effects.floating_text((player.rect.centerx, player.rect.top - 20), f'×{self.multiplier}', COMBO_COLOR)

    def check_misses(self, gone_lasers):
        if any(laser.shot.missed for laser in gone_lasers):
            self.combo_hits = 0

    def draw_hud(self, surface):
        score_rect = draw_text(surface, f'Score {self.score}', HUD_FONT_SIZE, topleft=(HUD_MARGIN, HUD_MARGIN))
        if self.multiplier > 1:
            draw_text(surface, f'×{self.multiplier}', HUD_FONT_SIZE, COMBO_COLOR, topleft=(score_rect.right + 10, HUD_MARGIN))
        draw_text(surface, f'Wave {self.wave}', HUD_FONT_SIZE, 'gray70', midtop=(SCREEN_WIDTH / 2, HUD_MARGIN))
        # One icon per life left, right-aligned
        icon_width = self.life_icon.get_width() + 6
        for life in range(self.lives):
            surface.blit(self.life_icon, self.life_icon.get_rect(topright=(SCREEN_WIDTH - HUD_MARGIN - life * icon_width, HUD_MARGIN)))
        self.draw_powerup_timers(surface, score_rect.bottom + 10)

    def draw_powerup_timers(self, surface, top):
        # An icon and a shrinking bar for each active power-up, under the score
        for kind, time_left in self.player.sprite.powerups.items():
            icon = load_sprite(POWERUP_SPRITES[kind], 0.5)
            icon_rect = surface.blit(icon, (HUD_MARGIN, top))
            bar = pygame.Rect(icon_rect.right + 6, icon_rect.centery - 2, 50 * time_left / POWERUP_TIME, 4)
            surface.fill(POWERUP_COLORS[kind], bar)
            top = icon_rect.bottom + 6
