
import pygame, math
from ..window import Window
from ..camera import Camera
from ..vector import Vector2D


class Rocket(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.img = pygame.image.load('assets/rocket.png').convert_alpha()
        self.image = self.img.copy()
        self.rect = self.image.get_rect(center = pos)

        self.position = Vector2D(pos)
        self.target_pos = Vector2D(pos)
        self.isClick = False

    def input(self):
        pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if (click[0] == 1 and not self.isClick):
            self.isClick = True
            self.target_pos = Camera.instance.screen_to_world_point(pos)
        elif (click[0] == 0 and self.isClick):
            self.isClick = False

    def movement(self):
        self.position = Vector2D.MoveTowards(self.position, self.target_pos, 100 * Window.instance.dt)
        # print(f"{self.rect.center} - {self.target_pos} - {self.position}")

    def render(self):
        direction = Vector2D.Subtraction(self.target_pos, self.position)
        angle = math.atan2(direction.y, direction.x) # Radians
        angle = math.degrees(angle) # Degrees
        # dikurang 90 biar angleny mulai dari kanan
        self.image = pygame.transform.rotate(self.img, -angle - 90)

    def update(self):
        self.input()
        self.movement()
        self.render()
        self.rect.center = self.position
