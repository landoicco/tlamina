import pygame

from laser import Laser
from resources import asset_path


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, constraint, speed):
        super().__init__()
        self.image = pygame.image.load(asset_path('sprites/player_blue.png')).convert_alpha()
        self.rect = self.image.get_rect(midbottom=pos)
        self.speed = speed
        self.max_x_constraint = constraint
        self.ready = True
        self.laser_time = 0
        self.laser_cooldown = 600

        self.lasers = pygame.sprite.Group()

        self.laser_sfx = pygame.mixer.Sound(asset_path('assets/sfx/laser_1.wav'))
        self.laser_sfx.set_volume(0.3)

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
        self.lasers.add(Laser(self.rect.center, -8, self.rect.bottom))

    def constraint(self):
        self.rect.right = min(self.rect.right, self.max_x_constraint)
        self.rect.left = max(self.rect.left, 0)

    def update(self):
        self.recharge()
        self.constraint()
        self.get_input()
        self.lasers.update()
