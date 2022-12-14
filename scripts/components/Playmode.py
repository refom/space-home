
import pygame
from .Clock import Clock
from .Vector import Vector2D
from .Font import Font
from ..manager.camera import Camera

class Playmode:
    modes = [
        {
            "name": "2x Fast",
            "priority": 0,
            "image_source": None,
            "image": None,
            "position": [0,0],
            "size": 0,

            "rocket-speed": 150,
            "resource-amount": [(12, 20),(7, 15)],
            "resource-cooldown": [2,4],
            "enemy-stats": {
                "enemy-speed": 200,
                "enemy-cooldown-move": [1,2],
                "enemy-start-time": 15,
                "enemy-limit-time": 10,
            },
        },
        {
            "name": "Relaxing",
            "priority": 0,
            "image_source": None,
            "image": None,
            "position": [0,0],
            "size": 0,

            "rocket-speed": 100,
            "resource-amount": [(25, 40),(15, 30)],
            "resource-cooldown": [3,5],
            "enemy-stats": {
                "enemy-speed": 100,
                "enemy-cooldown-move": [3,7],
                "enemy-start-time": 25,
                "enemy-limit-time": 10,
            },
        },
        {
            "name": "Invasion",
            "priority": 0,
            "image_source": None,
            "image": None,
            "position": [0,0],
            "size": 0,

            "rocket-speed": 150,
            "resource-amount": [(20, 30),(15, 20)],
            "resource-cooldown": [1,3],
            "enemy-stats": {
                "enemy-speed": 50,
                "enemy-cooldown-move": [0,2],
                "enemy-start-time": 5,
                "enemy-limit-time": 1,
            },
        },
        {
            "name": "Hardcore",
            "priority": 0,
            "image_source": None,
            "image": None,
            "position": [0,0],
            "size": 0,
            
            "rocket-speed": 150,
            "resource-amount": [(5, 10),(10, 15)],
            "resource-cooldown": [0.5,1],
            "enemy-stats": {
                "enemy-speed": 200,
                "enemy-cooldown-move": [0,1],
                "enemy-start-time": 5,
                "enemy-limit-time": 1,
            },
        },
        # {
        #     "name": "Playtest",
        #     "priority": 0,
        #     "image_source": None,
        #     "image": None,
        #     "position": [0,0],
        #     "size": 0,
            
        #     "rocket-speed": 200,
        #     "resource-amount": [(1, 1),(1, 1)],
        #     "resource-cooldown": [0.1,0.1],
        #     "enemy-stats": {
        #         "enemy-speed": 50,
        #         "enemy-cooldown-move": [5,7],
        #         "enemy-start-time": 5,
        #         "enemy-limit-time": 5,
        #     },
        # },
    ]
    
    selected_mode = 1
    mid_position = None
    offset_position = 100
    size = 0
    size_offset = 0
    speed_swipe = 10

    button = None
    is_click = False
    
    @classmethod
    def init(cls):
        x = Camera.instance.display.get_width() / 2
        y = (Camera.instance.display.get_height() / 2) + 30
        cls.mid_position = Vector2D((x, y))

        cls.size = y / 5
        cls.size_offset = cls.size / 3

        cls.button = pygame.image.load('assets/button.png').convert_alpha()
        cls.button.set_alpha(50)

        image_mode = [
            pygame.image.load('assets/mars.png').convert_alpha(),
            pygame.image.load('assets/earth.png').convert_alpha(),
            pygame.image.load('assets/enemy_ship.png').convert_alpha(),
            pygame.image.load('assets/rocket.png').convert_alpha(),
            # pygame.image.load('assets/neptune.png').convert_alpha(),
        ]

        priority = -1
        for i in range(len(cls.modes)):
            cls.modes[i]["image_source"] = image_mode[i]
            cls.modes[i]["image"] = image_mode[i].copy()
            cls.modes[i]["position"] = cls.mid_position
            cls.modes[i]["priority"] = priority
            priority += 1


    @classmethod
    def update(cls):
        cls.movement()
        cls.render()

    @classmethod
    def movement(cls):
        for mode in cls.modes:
            if not (mode["priority"] >= -1 and mode["priority"] <= 1): continue

            # left
            speed = cls.speed_swipe * Clock.delta_time
            if (mode["priority"] == -1):
                mode["position"] = [
                    Vector2D.LerpPoint(
                        mode["position"][0],
                        cls.mid_position.x - cls.offset_position,
                        speed
                    ), mode["position"][1]
                ]
                mode["size"] = Vector2D.LerpPoint(mode["size"], cls.size_offset, speed)
            # mid
            elif (mode["priority"] == 0):
                mode["position"] = [
                    Vector2D.LerpPoint(
                        mode["position"][0],
                        cls.mid_position.x,
                        speed
                    ), mode["position"][1]
                ]
                mode["size"] = Vector2D.LerpPoint(mode["size"], cls.size, speed)
            # right
            elif (mode["priority"] == 1):
                mode["position"] = [
                    Vector2D.LerpPoint(
                        mode["position"][0],
                        cls.mid_position.x + cls.offset_position,
                        speed
                    ), mode["position"][1]
                ]
                mode["size"] = Vector2D.LerpPoint(mode["size"], cls.size_offset, speed)


    @classmethod
    def render(cls):
        # draw left, mid, right mode
        for mode in cls.modes:
            if not (mode["priority"] >= -1 and mode["priority"] <= 1): continue
            mode["image"] = pygame.transform.scale(mode["image_source"], (mode["size"], mode["size"]))
            image_rect = mode["image"].get_rect(center = mode["position"])
            Camera.instance.display.blit(mode["image"], image_rect)
            # print(f"Mode: {mode['name']} \nPosition: {mode['position']} \nPriority: {mode['priority']}")

            if (mode["priority"] != 0): continue
            x = mode["position"][0]
            y = mode["position"][1] + image_rect.h + 10
            text_name = Font.head.render(mode["name"], False, (255,255,255))
            name_rect = text_name.get_rect(center = (x, y))
            Camera.instance.display.blit(text_name, name_rect)


    @classmethod
    def input(cls):
        mouse_pos = Camera.instance.screen_to_world_point(pygame.mouse.get_pos())
        mouse_click = pygame.mouse.get_pressed()

        for idx in range(len(cls.modes)):
            if not (cls.modes[idx]["priority"] >= -1 and cls.modes[idx]["priority"] <= 1): continue
            button = pygame.transform.scale(cls.button, (cls.size, cls.size))
            if (cls.modes[idx]["priority"] == 0):
                button = pygame.transform.scale(cls.button, (cls.size * 1.5, cls.size * 1.5))
            button_rect = button.get_rect(center = cls.modes[idx]["position"])

            # hover
            if (button_rect.collidepoint( Camera.instance.world_to_screen_point(mouse_pos))):
                Camera.instance.display.blit(button, button_rect)

                # click
                if (mouse_click[0] == 1 and not cls.is_click):
                    cls.is_click = True
                    if (cls.modes[idx]["priority"] == 1):
                        cls.select_right_mode()
                    elif (cls.modes[idx]["priority"] == -1):
                        cls.select_left_mode()
                    elif (cls.modes[idx]["priority"] == 0):
                        cls.selected_mode = idx
                        return True
                elif (mouse_click[0] == 0 and cls.is_click):
                    cls.is_click = False
        

    @classmethod
    def select_right_mode(cls):
        for mode in cls.modes:
            priority = mode["priority"] - 1
            if (priority < -1):
                priority = priority + len(cls.modes)
                mode["position"] = [cls.mid_position.x + (cls.offset_position * 1.5), mode["position"][1]]
            mode["priority"] = priority
            print(f"Right: Mode: {mode['name']}, Priority: {mode['priority']}")

    @classmethod
    def select_left_mode(cls):
        for mode in cls.modes:
            priority = mode["priority"] + 1
            if (priority > 1):
                priority = priority - len(cls.modes)
                mode["position"] = [cls.mid_position.x - (cls.offset_position * 1.5), mode["position"][1]]
            mode["priority"] = priority
            print(f"Left: Mode: {mode['name']}, Priority: {mode['priority']}")


