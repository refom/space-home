
import pygame, random
from ..Window import Window
from ..camera import Camera
from ..Vector import Vector2D

class Planet(pygame.sprite.Sprite):
    def __init__(self, pos, img_path, groups, collider=(10, 10)):
        super().__init__(groups)
        self.image_source = pygame.image.load(img_path).convert_alpha()
        self.image = self.image_source.copy()
        self.rect = self.image.get_rect(center = pos)

        self.collider = self.image.get_rect(
            width = self.rect.w + collider[0],
            height = self.rect.h + collider[1],
            center = pos
        )
        
        self.visible = True
        self.is_resource = False
        self.position = Vector2D(pos)
        self.angle = 0
        self.rotate_direction = 0.01 if (random.random() > 0.5) else -0.01

    def rotate_image(self):
        self.angle += self.rotate_direction
        if (self.angle >= 180):
            self.angle -= 180
        elif (self.angle <= -180):
            self.angle += 180

        self.image = pygame.transform.rotate(self.image_source, self.angle)
        self.rect = self.image.get_rect(center = self.position)

    def input(self):
        pos = Camera.instance.screen_to_world_point(pygame.mouse.get_pos())

        # Hover
        if (self.collider.collidepoint(pos)):
            pygame.draw.circle(
                Window.display,
                (0,255,0),
                Camera.instance.world_to_screen_point(self.collider.center),
                self.collider.w/3,
                width=1
            )

    def update(self):
        if not self.visible:
            self.image = None
            return
        self.input()
        self.rotate_image()
