
import pygame

class Font:
    font = None

    @classmethod
    def init(cls):
        pygame.font.init()
        cls.font = pygame.font.SysFont('Comic Sans MS', 20)

