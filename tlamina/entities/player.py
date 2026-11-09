import pygame

from tlamina.entities.laser import Laser
from tlamina.resources import load_sound, load_sprite
from tlamina.settings import (
    ENGINE_FLAME_FRAME_TIME,
    ENGINE_FLAME_FRAMES,
    PLAYER_BLINK_RATE,
    PLAYER_INVULNERABLE_TIME,
    PLAYER_LASER_COOLDOWN,
    PLAYER_LASER_SPEED,
    PLAYER_SPEED,
    SCREEN_WIDTH,
)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.ship_image = load_sprite('playerShip1_blue')
        self.image = self.ship_image
        self.rect = self.image.get_frect(midbottom=pos)
        self.invulnerable_left = 0
        self.speed = PLAYER_SPEED
        self.cooldown_left = 0
        self.flame_frames = [load_sprite(name) for name in ENGINE_FLAME_FRAMES]
        self.flame_time = 0

        self.lasers = pygame.sprite.Group()

        self.laser_sfx = load_sound('assets/kenney/space-shooter-redux/sfx_laser1.ogg', 0.3)

    def get_input(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed * dt
        elif keys[pygame.K_LEFT]:
            self.rect.x -= self.speed * dt

        if keys[pygame.K_SPACE] and self.cooldown_left <= 0:
            self.shoot_laser()
            self.cooldown_left = PLAYER_LASER_COOLDOWN
            self.laser_sfx.play()

    def recharge(self, dt):
        self.cooldown_left = max(self.cooldown_left - dt, 0)

    def shoot_laser(self):
        self.lasers.add(Laser(self.rect.center, PLAYER_LASER_SPEED))

    def constraint(self):
        self.rect.right = min(self.rect.right, SCREEN_WIDTH)
        self.rect.left = max(self.rect.left, 0)

    @property
    def invulnerable(self):
        return self.invulnerable_left > 0

    @property
    def visible(self):
        # Blinks while invulnerable
        return not self.invulnerable or int(self.invulnerable_left * PLAYER_BLINK_RATE) % 2 == 0

    def take_hit(self, hits_taken):
        """Become briefly invulnerable and show cracks for the total number of hits taken."""
        self.invulnerable_left = PLAYER_INVULNERABLE_TIME
        cracks = load_sprite(f'playerShip1_damage{min(hits_taken, 3)}')
        # A copy, because the ship sprite is cached and shared
        self.image = self.ship_image.copy()
        self.image.blit(cracks, cracks.get_rect(center=self.image.get_rect().center))

    def draw_engine_flame(self, surface):
        frame = self.flame_frames[int(self.flame_time / ENGINE_FLAME_FRAME_TIME) % len(self.flame_frames)]
        # Tucked a few pixels under the hull, so it looks attached to the engine
        surface.blit(frame, frame.get_rect(midtop=(self.rect.centerx, self.rect.bottom - 4)))

    def update(self, dt):
        self.flame_time += dt
        self.invulnerable_left = max(self.invulnerable_left - dt, 0)
        self.recharge(dt)
        self.get_input(dt)
        self.constraint()
        self.lasers.update(dt)
