
import pygame

class Font:
    text = None
    title = None
    head = None

    @classmethod
    def init(cls):
        pygame.font.init()
        cls.text = pygame.font.SysFont('Comic Sans MS', 14)
        cls.title = pygame.font.SysFont('Comic Sans MS', 44)
        cls.head = pygame.font.SysFont('Comic Sans MS', 18)

