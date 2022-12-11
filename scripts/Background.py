
import pygame, random
from .Window import Window
from .camera import Camera
from .Vector import Vector2D

# stars berisi posisi bintang, ukurannya, jauhnya, dan warna
class Stars:
    def __init__(self, position, size, z, color):
        self.position = Vector2D(position)
        self.size = size
        self.z = z
        self.color = color

class Background:
    stars = []
    width = 0
    height = 0
    stars_color = {
        "default": (255, 255, 240),
        "far": (255, 255, 100),
    }

    @classmethod
    def init(cls):
        cls.width = Window.base_resolution[0] * 2
        cls.height = Window.base_resolution[1] * 2
        for _ in range(Window.scaled_resolution[0] // 1.5):
            x = random.randint(-cls.width, cls.width)
            y = random.randint(-cls.height, cls.height)
            z = random.random() / 2
            size = z * 2.5
            color = cls.stars_color["far"] if (z <= 0.25) else cls.stars_color["default"]
            new_star = Stars((x, y), size, z, color)
            cls.stars.append(new_star)

    @classmethod
    def create_new_stars(cls):
        x = random.randint(-cls.width, 0)
        y = random.randint(-cls.height, 0)
        z = random.random() / 2
        size = z * 2.5
        color = cls.stars_color["far"] if (z <= 0.25) else cls.stars_color["default"]
        new_star = Stars((x, y), size, z, color)
        cls.stars.append(new_star)

    @classmethod
    def update(cls):
        for i in range(len(cls.stars) - 1):
            # update movement
            cls.stars[i].position.x += 0.01
            cls.stars[i].position.y += 0.01

            if (cls.stars[i].position.x >= cls.width and
                cls.stars[i].position.y >= cls.height):
                cls.stars.remove(cls.stars[i])
                cls.create_new_stars()

            # draw
            pygame.draw.circle(
                Camera.instance.display,
                cls.stars[i].color,
                Camera.instance.parallax_point(cls.stars[i].position, cls.stars[i].z),
                cls.stars[i].size,
            )

