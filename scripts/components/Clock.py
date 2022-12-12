
import pygame, math
from ..Config import Config

class Clock:
    fps = None
    clock = None
    delta_time = None
    start_timer = None
    stop_timer = None

    @classmethod
    def init(cls):
        cls.fps = Config.window["fps"]
        cls.clock = pygame.time.Clock()
        cls.delta_time = 0

    @classmethod
    def update(cls):
        cls.delta_time = cls.clock.tick(cls.fps) * 0.001

    @classmethod
    def start_time(cls):
        cls.start_timer = pygame.time.get_ticks()

    @classmethod
    def stop_time(cls):
        cls.stop_timer = pygame.time.get_ticks()

    @classmethod
    def get_current_time_ms(cls):
        return pygame.time.get_ticks() - cls.start_timer

    @classmethod
    def get_current_time_s(cls):
        return math.ceil((pygame.time.get_ticks() - cls.start_timer) * 0.001)

    @classmethod
    def get_stop_time_ms(cls):
        return cls.stop_timer - cls.start_timer

    @classmethod
    def get_stop_time_s(cls):
        return math.ceil((cls.stop_timer - cls.start_timer) * 0.001)