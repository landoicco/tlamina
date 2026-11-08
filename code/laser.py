import pygame

from resources import load_image


class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, speed, screen_height):
        super().__init__()
        self.image = load_image('sprites/lasers/laser_blue_up.png')
        if speed > 0:
            # Lasers moving down point down
            self.image = pygame.transform.flip(self.image, False, True)
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed
        self.height_y_constraint = screen_height

    def destroy(self):
        if self.rect.y <= -50 or self.rect.y >= self.height_y_constraint - 50:
            self.kill()

    def update(self):
        self.rect.y += self.speed
        self.destroy()
