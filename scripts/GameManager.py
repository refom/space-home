
import pygame, random, math
from .Window import Window
from .Font import Font
from .Clock import Clock
from .PlanetManager import PlanetManager

class GameManager:
    player = None

    resource_left = None
    open_planet_goal = False
    win = False

    win_box_rect = None
    earth_position = None
    earth_image_source = None
    earth_image = None
    earth_rect = None
    earth_angle = 0

    text_win = [
        "You Return Home Safely",
        "Gratss!  I can't believe you can return safely",
        "WHATTT!!!??!?",
    ]
    text_index = 0

    @classmethod
    def init(cls, player):
        cls.player = player
        cls.open_planet_goal = False
        cls.resource_left = len(PlanetManager.instance.planet_resources)
    
    @classmethod
    def win_condition(cls):
        Clock.stop_time()
        cls.win = True

    @classmethod
    def resource_collected(cls):
        cls.resource_left -= 1
        if (cls.resource_left <= 0):
            cls.open_planet_goal = True

            # tambah kedalam list, agar dapat dikunjungi
            PlanetManager.instance.planet_goal.visible = True
            PlanetManager.instance.planets.append(PlanetManager.instance.planet_goal)

            # create box for win
            width = Window.display.get_width() / 2
            height = Window.display.get_height() / 2
            x, y = width / 2, height / 2
            cls.win_box_rect = pygame.Rect(x, y, width, height)

            # create earth img for win
            cls.earth_position = (x + width / 2, y + height / 4)
            cls.earth_image_source = pygame.image.load('assets/earth.png').convert_alpha()
            cls.earth_image_source = pygame.transform.scale(cls.earth_image_source, (height / 4, height / 4))
            cls.earth_image = cls.earth_image_source.copy()
            cls.earth_rect = cls.earth_image.get_rect(center = cls.earth_position)
            cls.earth_angle = 0

            cls.text_index = random.randint(0, len(cls.text_win) - 1)

    @classmethod
    def scene_win(cls):
        # box
        pygame.draw.rect(
            Window.display,
            (24, 29, 49),
            cls.win_box_rect,
            border_radius = 17
        )

        # ada gambar earthnya rotate sama roketnya mengitari earth
        cls.earth_angle += 0.02
        if (cls.earth_angle >= 180):
            cls.earth_angle -= 360

        cls.earth_image = pygame.transform.rotate(cls.earth_image_source, cls.earth_angle)
        cls.earth_rect = cls.earth_image.get_rect(center = cls.earth_position)
        Window.display.blit(cls.earth_image, cls.earth_rect)

        # ada teks "You Return Home Safely"
        comment = Font.head.render(cls.text_win[cls.text_index], False, (255,255,255))
        comment_rect = comment.get_rect(center = (cls.win_box_rect.centerx, cls.win_box_rect.centery + 5))
        Window.display.blit(comment, comment_rect)

        # ada teks time survive
        times_sec = (Clock.get_stop_time_s() % 60)
        times_min = math.floor(times_sec / 60)
        times = Font.head.render(f"{times_min} : {times_sec}", False, (255,255,255))
        times_rect = times.get_rect(center = (cls.win_box_rect.centerx, cls.win_box_rect.centery + 30))
        Window.display.blit(times, times_rect)

        # click anywhere to menu
        click_anywhere = Font.head.render("Click anywhere to back", False, (255,255,255))
        click_anywhere_rect = click_anywhere.get_rect(center = (cls.win_box_rect.centerx, cls.win_box_rect.centery + 90))
        Window.display.blit(click_anywhere, click_anywhere_rect)


