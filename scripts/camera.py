
import pygame
from .Window import Window
from .Clock import Clock
from .Vector import Vector2D

class Camera(pygame.sprite.Group):
    # Singleton
    instance = None

    def __init__(self):
        super().__init__()
        self.display = Window.display
        self.offset = Vector2D()
        self.center = Vector2D(
            self.display.get_size()[0] // 2,
            self.display.get_size()[1] // 2
        )

        self.speed_lerp = 2
        
        if (Camera.instance == None):
            Camera.instance = self

    def camera_target_center(self, target):
        spd = self.speed_lerp * Clock.delta_time
        self.offset = self.offset.lerp(target.rect.center - self.center, spd if (spd < 1) else 1)

    def custom_draw(self, target=None):
        if (target):
            self.camera_target_center(target)

        for sprite in self.sprites():
            if not sprite.image: continue
            offset_pos = sprite.rect.topleft - self.offset
            self.display.blit(sprite.image, offset_pos)

    def screen_to_world_point(self, point):
        x = point[0] / Window.scale_ratio[0]
        y = point[1] / Window.scale_ratio[1]
        return self.offset + (x, y)

    def world_to_screen_point(self, point):
        return point - self.offset

    def parallax_point(self, point, strength):
        return point - (self.offset * strength)