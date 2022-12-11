
import pygame, random
from ..vector import Vector2D

class Planetgoal(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.img = pygame.image.load('assets/planetgoal.png').convert_alpha()
        self.image = self.img.copy()
        self.rect = self.image.get_rect(center = pos)
        
        self.position = Vector2D(pos)
        self.angle = 0
        self.rotate_direction = 0.01 if (random.random() > 0.5) else -0.01

    def rotate_image(self):
        self.angle += self.rotate_direction
        if (self.angle >= 180):
            self.angle -= 180
        elif (self.angle <= -180):
            self.angle += 180

        self.image = pygame.transform.rotate(self.img, self.angle)
        self.rect = self.image.get_rect(center = self.position)


    def update(self):
        self.rotate_image()
