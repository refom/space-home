
import pygame, random
from ..manager.camera import Camera
from ..components.Vector import Vector2D

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
        self.collected = False
        self.is_resource = False
        self.is_hover = False
        self.is_enemy_exist = False
        self.is_enemy_arrive = False
        
        self.resource_cooldown = 0
        self.angle = 0
        self.rotate_direction = 0.02 if (random.random() > 0.5) else -0.02
        self.position = Vector2D(pos)

        self.timer_load_resource = 0

        self.color = {
            "default": (100, 7, 9),
            "active": (200, 7, 9),
            "load": (7, 100, 9),
            "finished": (7, 200, 9),
        }

    def render(self):
        self.rotate_image()
        if (self.is_hover or self.is_resource):
            self.draw_border()

    def input(self):
        pos = Camera.instance.screen_to_world_point(pygame.mouse.get_pos())

        # Hover
        self.is_hover = True if (self.collider.collidepoint(pos)) else False


    def update(self):
        if not self.visible:
            self.image = None
            return
        self.input()
        self.render()

    def rotate_image(self):
        self.angle += self.rotate_direction
        if (self.angle >= 180):
            self.angle -= 360
        elif (self.angle <= -180):
            self.angle += 360

        self.image = pygame.transform.rotate(self.image_source, self.angle)
        self.rect = self.image.get_rect(center = self.position)

    def draw_border(self):
        color = self.color["default"]
        if (self.is_hover):
            color = self.color["active"]
        if (self.collected):
            color = self.color["finished"]

        pygame.draw.circle(
            Camera.instance.display,
            color,
            Camera.instance.world_to_screen_point(self.position),
            radius = self.collider.w / 3,
            width = 2
        )
    
    def draw_load_resource(self, time):
        radius = Vector2D.NormalizePoint(time, self.resource_cooldown) * (self.collider.w / 3)
        pygame.draw.circle(
            Camera.instance.display,
            self.color["load"],
            Camera.instance.world_to_screen_point(self.position),
            radius = radius
        )
    
    def set_cooldown(self, index):
        if (index == 1):
            self.resource_cooldown = 3
        if (index == 2):
            self.resource_cooldown = 5