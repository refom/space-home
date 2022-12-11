
import pygame, random, math
from .Window import Window
from .Font import Font
from .Clock import Clock
from .objek.enemy import Enemy
from .camera import Camera
from .PlanetManager import PlanetManager

class GameManager:
    player = None
    # start time in seconds
    enemy_start_time = 40
    enemy_start_time_counter = 0
    enemy_limit_time = 20

    enemy_timer_lose = 0.3
    enemy_timer = 0
    enemy_max = 0
    enemys = []

    resource_left = None
    open_planet_goal = False
    win = False
    # 0 = normal
    # 1 = win
    # 2 = lose
    game_state = 0

    panel_rect = None

    icon_position = None
    icon_image_source = None
    icon_image = None
    icon_rect = None
    icon_angle = 0

    text_win = [
        "You Return Home Safely",
        "Gratss!  I can't believe you can return safely",
        "Ah! you're finally home!!",
    ]
    text_lose = [
        "EZ",
        "Unfortunately your journey ends here",
        "Tips: Try Harder",
    ]
    text_index = 0

    @classmethod
    def init(cls, player):
        cls.player = player
        cls.resource_left = len(PlanetManager.instance.planet_resources)
        cls.open_planet_goal = False

        cls.enemys = []
        cls.enemy_max = len(PlanetManager.instance.planets) // 2
        cls.enemy_timer = cls.enemy_start_time
        cls.enemy_start_time_counter = cls.enemy_start_time
        print(f"enemy max : {cls.enemy_max}")

        # create box for panel gameover
        width = Window.display.get_width() / 2
        height = Window.display.get_height() / 2
        x, y = width / 2, height / 2
        cls.panel_rect = pygame.Rect(x, y, width, height)

        # load preset for panel gameover
        cls.icon_position = (
            x + width / 2,
            y + height / 4
        )
        cls.icon_angle = 0
    
    @classmethod
    def update_enemy(cls):
        if (cls.game_state != 0): return
        cls.enemy_timer -= Clock.delta_time
        if (cls.enemy_timer <= 0):
            if (cls.enemy_start_time_counter > cls.enemy_limit_time):
                cls.enemy_start_time_counter -= cls.enemy_timer_lose
            cls.enemy_timer = cls.enemy_start_time_counter
            cls.spawn_enemy()

    @classmethod
    def spawn_enemy(cls):
        planet = None

        for _ in range(5):
            new_planet = PlanetManager.instance.get_neutral_planet()
            if (new_planet.is_enemy_exist):
                continue
            planet = new_planet
            break

        if (planet == None or len(cls.enemys) > cls.enemy_max):
            return

        new_enemy = Enemy(planet.position, Camera.instance)
        new_enemy.current_planet = planet
        cls.enemys.append(new_enemy)

    @classmethod
    def win_condition(cls):
        Clock.stop_time()
        cls.game_state = 1

        # load icon img for win
        cls.icon_image_source = pygame.image.load('assets/earth.png').convert_alpha()
        cls.icon_image_source = pygame.transform.scale(cls.icon_image_source, (cls.panel_rect.h / 4, cls.panel_rect.h / 4))
        cls.icon_image = cls.icon_image_source.copy()
        cls.icon_rect = cls.icon_image.get_rect(center = cls.icon_position)

        cls.text_index = random.randint(0, len(cls.text_win) - 1)

    @classmethod
    def lose_condition(cls):
        Clock.stop_time()
        cls.game_state = 2

        # stop semua enemy
        for now_enemy in cls.enemys:
            now_enemy.active = False

        # load icon img for win
        cls.icon_image_source = pygame.image.load('assets/enemy_ship.png').convert_alpha()
        cls.icon_image_source = pygame.transform.scale(cls.icon_image_source, (cls.panel_rect.h / 4, cls.panel_rect.h / 4))
        cls.icon_image = cls.icon_image_source.copy()
        cls.icon_rect = cls.icon_image.get_rect(center = cls.icon_position)

        cls.text_index = random.randint(0, len(cls.text_lose) - 1)

    @classmethod
    def resource_collected(cls):
        cls.resource_left -= 1
        if (cls.resource_left <= 0):
            # tambah kedalam list, agar dapat dikunjungi
            cls.open_planet_goal = True
            PlanetManager.instance.planet_goal.visible = True
            PlanetManager.instance.planets.append(PlanetManager.instance.planet_goal)

    @classmethod
    def scene_game_over(cls):
        pygame.draw.rect(
            Window.display,
            (24, 29, 49),
            cls.panel_rect,
            border_radius = 17
        )

        # icon rotasi biar gak statis
        cls.icon_angle += 0.02
        if (cls.icon_angle >= 180):
            cls.icon_angle -= 360

        cls.icon_image = pygame.transform.rotate(cls.icon_image_source, cls.icon_angle)
        cls.icon_rect = cls.icon_image.get_rect(center = cls.icon_position)
        Window.display.blit(cls.icon_image, cls.icon_rect)

        # ada teks "You Return Home Safely"
        teks = cls.text_win[cls.text_index]
        if (cls.game_state == 2):
            teks = cls.text_lose[cls.text_index]
        comment = Font.head.render(teks, False, (255,255,255))
        comment_rect = comment.get_rect(center = (cls.panel_rect.centerx, cls.panel_rect.centery + 5))
        Window.display.blit(comment, comment_rect)

        # ada teks time survive
        times_sec = (Clock.get_stop_time_s() % 60)
        times_min = math.floor(Clock.get_current_time_s() / 60)
        times = Font.head.render(f"{times_min:02d} : {times_sec:02d}", False, (255,255,255))
        times_rect = times.get_rect(center = (cls.panel_rect.centerx, cls.panel_rect.centery + 30))
        Window.display.blit(times, times_rect)

        # click anywhere to menu
        click_anywhere = Font.head.render("Click anywhere to back", False, (255,255,255))
        click_anywhere_rect = click_anywhere.get_rect(center = (cls.panel_rect.centerx, cls.panel_rect.centery + 90))
        Window.display.blit(click_anywhere, click_anywhere_rect)


