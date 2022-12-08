
import pygame
from .window import Window
from .vector import Vector2D

class Camera(pygame.sprite.Group):
    instance = None

    def __init__(self):
        super().__init__()
        self.display = Window.instance.display
        self.offset = Vector2D()

        self.half_w = self.display.get_size()[0] // 2
        self.half_h = self.display.get_size()[1] // 2

        self.speed_lerp = 2
        
        if (Camera.instance == None):
            Camera.instance = self

    def camera_target_center(self, target):
        self.offset.x = Vector2D.LerpPoint(self.offset.x, target.rect.centerx - self.half_w, self.speed_lerp * Window.instance.dt)
        self.offset.y = Vector2D.LerpPoint(self.offset.y, target.rect.centery - self.half_h, self.speed_lerp * Window.instance.dt)

    def custom_draw(self, target):
        if (target):
            self.camera_target_center(target)

        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.display.blit(sprite.image, offset_pos)

    def screen_to_world_point(self, point):
        x = point[0] / Window.instance.scale_ratio[0]
        y = point[1] / Window.instance.scale_ratio[1]
        return self.offset + (x, y)
