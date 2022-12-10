
import pygame
from .Config import Config

class Clock:
    fps = None
    clock = None
    delta_time = None
    time = None

    @classmethod
    def init(cls):
        cls.fps = Config.window["fps"]
        cls.clock = pygame.time.Clock()
        cls.delta_time = 0

    @classmethod
    def update(cls):
        cls.delta_time = cls.clock.tick(cls.fps) * 0.001

