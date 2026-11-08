import pygame

from laser import Laser
from resources import load_image, load_sound
from settings import PLAYER_LASER_COOLDOWN, PLAYER_LASER_SPEED, PLAYER_SPEED, SCREEN_WIDTH


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = load_image('sprites/player_blue.png')
        self.rect = self.image.get_frect(midbottom=pos)
        self.speed = PLAYER_SPEED
        self.cooldown_left = 0

        self.lasers = pygame.sprite.Group()

        self.laser_sfx = load_sound('assets/sfx/laser_1.wav', 0.3)

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

    def update(self, dt):
        self.recharge(dt)
        self.constraint()
        self.get_input(dt)
        self.lasers.update(dt)
