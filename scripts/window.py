
import pygame, sys
from .config import Config

class Window:
    instance = None

    def __init__(self):
        pygame.init()

        self.fps = Config.window["fps"]
        self.clock = pygame.time.Clock()
        self.dt = 0

        self.base_resolution = Config.window["base_resolution"]
        self.scaled_resolution = Config.window["scaled_resolution"]
        self.offset = Config.window["offset"]
        self.scale_ratio = [
            self.base_resolution[0] / self.scaled_resolution[0],
            self.base_resolution[1] / self.scaled_resolution[1]
        ]

        # self.screen = pygame.display.set_mode(self.base_resolution, pygame.DOUBLEBUF | pygame.HWSURFACE)
        self.screen = pygame.display.set_mode(self.base_resolution)
        pygame.display.set_caption(Config.window["caption"])
        self.display = pygame.Surface((self.scaled_resolution[0] - self.offset[0] * 2, self.scaled_resolution[1] - self.offset[1] * 2))

        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])

        if (Window.instance == None):
            Window.instance = self

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    def draw(self):
        width = int(self.display.get_width() * self.scale_ratio[0])
        height = int(self.display.get_height() * self.scale_ratio[1])
        self.screen.blit(pygame.transform.scale(self.display, (width, height)), (0, 0))
        
        pygame.display.update()
        self.dt = self.clock.tick(self.fps) * 0.001
        self.display.fill(Config.window["background_color"])

