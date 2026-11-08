import pygame

from laser import Laser
from resources import load_image, load_sound
from settings import PLAYER_LASER_COOLDOWN, PLAYER_LASER_SPEED, PLAYER_SPEED, SCREEN_WIDTH


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = load_image('sprites/player_blue.png')
        self.rect = self.image.get_rect(midbottom=pos)
        self.speed = PLAYER_SPEED
        self.ready = True
        self.laser_time = 0
        self.laser_cooldown = PLAYER_LASER_COOLDOWN

        self.lasers = pygame.sprite.Group()

        self.laser_sfx = load_sound('assets/sfx/laser_1.wav', 0.3)

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        elif keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        if keys[pygame.K_SPACE] and self.ready:
            self.shoot_laser()
            self.ready = False
            self.laser_time = pygame.time.get_ticks()
            self.laser_sfx.play()

    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cooldown:
                self.ready = True

    def shoot_laser(self):
        self.lasers.add(Laser(self.rect.center, PLAYER_LASER_SPEED))

    def constraint(self):
        self.rect.right = min(self.rect.right, SCREEN_WIDTH)
        self.rect.left = max(self.rect.left, 0)

    def update(self):
        self.recharge()
        self.constraint()
        self.get_input()
        self.lasers.update()
