
import pygame, math

from .Font import Font
from .Clock import Clock
from .camera import Camera
from .Window import Window
from .objek.rocket import Rocket
from .PlanetManager import PlanetManager
from .GameManager import GameManager

class Menu:
    # 0 = default menu
    # 1 = gameplay
    scene = 0
    init_game = False

    @classmethod
    def input(cls, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                cls.change_menu()

    @classmethod
    def change_menu(cls):
        if (cls.scene == 0):
            cls.scene = 1
        if (cls.scene == 1 and GameManager.win):
            cls.scene = 0
            GameManager.win = False
            cls.init_game = False

    @classmethod
    def update(cls):
        if (cls.scene == 0):
            cls.scene_default()
        elif (cls.scene == 1):
            cls.scene_gameplay()

    @classmethod
    def scene_default(cls):
        cls.draw_text_menu()

    @classmethod
    def draw_text_menu(cls):
        title = Font.title.render("Space Home", False, (255,255,255))
        title_rect = title.get_rect(center = (Window.display.get_width()/2, Window.display.get_height()/3))
        Window.display.blit(title, title_rect)

        click = Font.head.render("Click anywhere to Play", False, (255,255,255))
        click_rect = click.get_rect(center = (Window.display.get_width()/2, Window.display.get_height()/2))
        Window.display.blit(click, click_rect)

    @classmethod
    def scene_gameplay(cls):
        if (not cls.init_game):
            cls.init_gameplay()
        
        Camera.instance.update()
        Camera.instance.custom_draw(GameManager.player)
        cls.draw_text_gameplay()

        if (GameManager.win):
            GameManager.scene_win()

    @classmethod
    def init_gameplay(cls):
        cls.init_game = True

        Camera.instance.empty()
        PlanetManager.instance.init()
        # Neutral | image path , jumlah
        PlanetManager.instance.add_image('assets/planet.png', -1)
        # Resource
        PlanetManager.instance.add_image('assets/mars.png', 1)
        PlanetManager.instance.add_image('assets/neptune.png', 0)
        # Goal
        PlanetManager.instance.add_image('assets/earth.png', -1)

        # Generate world
        PlanetManager.instance.generate(
            radius = 96,
            map_size = (Window.base_resolution[0] * 3, Window.base_resolution[1] * 3),
            try_length = 5
        )
        rocket = Rocket(PlanetManager.instance.get_neutral_planet().position, Camera.instance)
        GameManager.init(rocket)

        # Start clock
        Clock.start_time()

    @classmethod
    def draw_text_gameplay(cls):
        fps = Font.text.render(f"FPS : {Clock.clock.get_fps():.0f}", False, (255,255,255))
        fps_rect = fps.get_rect(topright = (Window.display.get_width() - 20, 20))
        Window.display.blit(fps, fps_rect)

        resource = Font.text.render(f"Resource Left : {GameManager.resource_left}", False, (255,255,255))
        resource_rect = fps.get_rect(topleft = (20, 20))
        Window.display.blit(resource, resource_rect)

        if (GameManager.win): return
        times_sec = (Clock.get_current_time_s() % 60)
        times_min = math.floor(times_sec / 60)
        timer = Font.text.render(f"{times_min} : {times_sec}", False, (255,255,255))
        timer_rect = timer.get_rect(midtop = (Window.display.get_width()/2, 20))
        Window.display.blit(timer, timer_rect)

