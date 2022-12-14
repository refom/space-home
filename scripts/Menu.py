
import pygame, math, random

from .Window import Window
from .objek.rocket import Rocket

from .manager.camera import Camera
from .manager.PlanetManager import PlanetManager
from .manager.GameManager import GameManager

from .components.Playmode import Playmode
from .components.Font import Font
from .components.Clock import Clock
from .components.Background import Background
from .components.Vector import Vector2D


class Menu:
    # 0 = default menu
    # 1 = gameplay
    scene = 0
    init_game = False
    title = None

    waves = []

    info_active = True
    info_time = 10
    info_timer = 0

    @classmethod
    def init(cls):
        cls.title = pygame.image.load('assets/logo.png').convert_alpha()
        Playmode.init()

    @classmethod
    def input(cls, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                cls.create_wave()

    @classmethod
    def create_wave(cls):
        position = Camera.instance.screen_to_world_point(pygame.mouse.get_pos())
        cls.waves.append([position, 0, 30])

    @classmethod
    def draw_click(cls):
        done = 0
        for i in range(len(cls.waves)):
            cls.waves[i][1] += Clock.delta_time

            if (cls.waves[i][1] > 1):
                done += 1
                continue

            # Radius dan width circle
            timer = Vector2D.EaseOutCubic(cls.waves[i][1])
            radius = timer * cls.waves[i][2]
            width = (1 - timer) * cls.waves[i][2]

            pygame.draw.circle(
                Camera.instance.display,
                (100, 100, 100),
                Camera.instance.world_to_screen_point(cls.waves[i][0]),
                radius = radius,
                width = math.ceil(width)
            )
        if (done > 0):
            cls.waves = [wave for wave in cls.waves if wave[1] <= 1]

    @classmethod
    def change_menu(cls):
        if (cls.scene == 0):
            cls.scene = 1
        if (cls.scene == 1 and GameManager.game_state != 0):
            cls.scene = 0
            GameManager.game_state = 0
            cls.init_game = False
            Camera.instance.empty()

    @classmethod
    def update(cls):
        Background.update()
        cls.draw_click()
        if (cls.scene == 0):
            cls.scene_default()
        elif (cls.scene == 1):
            cls.scene_gameplay()

    @classmethod
    def scene_default(cls):
        cls.draw_text_menu()
        is_change_menu = Playmode.input()
        Playmode.update()

        if (is_change_menu):
            cls.change_menu()

    @classmethod
    def draw_text_menu(cls):
        title_rect = cls.title.get_rect(center = (Window.display.get_width()/2, Window.display.get_height()/3))
        Window.display.blit(cls.title, title_rect)

        # click = Font.head.render("Click anywhere to Play", False, (255,255,255))
        # click_rect = click.get_rect(center = (Window.display.get_width()/2, Window.display.get_height()/2))
        # Window.display.blit(click, click_rect)
        
        quit = Font.head.render("Press ESC to quit the game", False, (255,255,255))
        quit_rect = quit.get_rect(center = (Window.display.get_width()/2, Window.display.get_height()/2 + 250 ))
        Window.display.blit(quit, quit_rect)

    @classmethod
    def scene_gameplay(cls):
        if (not cls.init_game):
            cls.init_gameplay()
        
        cls.draw_text_gameplay()

        GameManager.update_enemy()
        Camera.instance.update()

        Camera.instance.custom_draw(GameManager.player)
        if (GameManager.game_state != 0):
            is_change_menu = GameManager.input()
            GameManager.scene_game_over()

            if (is_change_menu):
                cls.change_menu()

    @classmethod
    def init_gameplay(cls):
        cls.init_game = True

        mode = Playmode.modes[Playmode.selected_mode]
        Camera.instance.empty()
        PlanetManager.instance.init()
        # Neutral | image path , jumlah
        PlanetManager.instance.add_image('assets/planet.png', -1)
        # Resource
        PlanetManager.instance.add_image(
            'assets/mars.png',
            random.randint(mode["resource-amount"][0][0], mode["resource-amount"][0][1]),
            mode["resource-cooldown"][0]
        )
        PlanetManager.instance.add_image(
            'assets/neptune.png',
            random.randint(mode["resource-amount"][1][0], mode["resource-amount"][1][1]),
            mode["resource-cooldown"][1]
        )
        # Goal
        PlanetManager.instance.add_image('assets/earth.png', -1)

        # Generate world
        PlanetManager.instance.generate(
            radius = 96,
            map_size = (Window.base_resolution[0] * 3, Window.base_resolution[1] * 3),
            try_length = 5
        )

        rocket = Rocket(
            PlanetManager.instance.get_neutral_planet().position,
            mode["rocket-speed"],
            Camera.instance
        )
        GameManager.init(rocket, mode["name"], mode["enemy-stats"], mode["image_source"])
        print(f"Selected Mode: {mode['name']}")
        print(f"Rocket Speed: {mode['rocket-speed']}")
        print(f"Resource Amount: {mode['resource-amount']}")
        print(f"Resource Cooldown: {mode['resource-cooldown']}")
        print(f"Enemy stats: {mode['enemy-stats']}")

        # Start clock
        Clock.start_time()

    @classmethod
    def draw_text_gameplay(cls):
        fps = Font.text.render(f"FPS : {Clock.clock.get_fps():.0f}", False, (255,255,255))
        fps_rect = fps.get_rect(topright = (Window.display.get_width() - 20, 20))
        Window.display.blit(fps, fps_rect)

        resource = Font.text.render(f"Resource Left : {GameManager.resource_left}", False, (255,255,255))
        resource_rect = resource.get_rect(topleft = (20, 20))
        Window.display.blit(resource, resource_rect)

        if (cls.info_timer <= cls.info_time):
            cls.info_timer += Clock.delta_time
            text1 = "You're stranded!"
            text2 = "Fix your radar by collecting resource so you can return to your home!"
            info_text1 = Font.text.render(text1, False, (255,255,255))
            info_text2 = Font.text.render(text2, False, (255,255,255))
            info_rect1 = info_text1.get_rect(center = (Window.display.get_width() / 2, (Window.display.get_height() / 4) * 3))
            info_rect2 = info_text2.get_rect(center = (Window.display.get_width() / 2, (Window.display.get_height() / 4) * 3 + 25))
            Window.display.blit(info_text1, info_rect1)
            Window.display.blit(info_text2, info_rect2)

        if (GameManager.game_state != 0): return
        times_sec = (Clock.get_current_time_s() % 60)
        times_min = math.floor(Clock.get_current_time_s() / 60)
        timer = Font.text.render(f"{times_min:02d} : {times_sec:02d}", False, (255,255,255))
        timer_rect = timer.get_rect(midtop = (Window.display.get_width()/2, 20))
        Window.display.blit(timer, timer_rect)


