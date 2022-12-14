
import pygame, sys
from .Config import Config
from .components.music import Music

class Window:
    base_resolution = None
    scaled_resolution = None
    scale_ratio = None
    offset = None

    screen = None
    display = None

    @classmethod
    def init(cls):
        pygame.init()

        cls.base_resolution = Config.window["base_resolution"]
        cls.scaled_resolution = Config.window["scaled_resolution"]
        cls.offset = Config.window["offset"]
        cls.scale_ratio = [
            cls.base_resolution[0] / cls.scaled_resolution[0],
            cls.base_resolution[1] / cls.scaled_resolution[1]
        ]

        # cls.screen = pygame.display.set_mode(cls.base_resolution, pygame.DOUBLEBUF | pygame.HWSURFACE)
        cls.display = pygame.Surface((cls.scaled_resolution[0] - cls.offset[0] * 2, cls.scaled_resolution[1] - cls.offset[1] * 2))
        cls.screen = pygame.display.set_mode(cls.base_resolution)
        pygame.display.set_caption(Config.window["caption"])

        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEBUTTONUP])

    @classmethod
    def input(cls):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                Music.click_sound()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        return events

    @classmethod
    def update(cls):
        width = int(cls.display.get_width() * cls.scale_ratio[0])
        height = int(cls.display.get_height() * cls.scale_ratio[1])

        cls.screen.blit(pygame.transform.scale(cls.display, (width, height)), (0, 0))
        
        pygame.display.update()
        cls.display.fill(Config.window["background_color"])

