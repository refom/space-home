import pygame, random

from scripts.Window import Window
from scripts.Clock import Clock
from scripts.camera import Camera
from scripts.Font import Font
from scripts.planet_manager import PlanetManager
from scripts.objek.rocket import Rocket

Window.init()
Clock.init()
Font.init()
camera = Camera()
planet_manager = PlanetManager()

# Neutral
planet_manager.add_image('assets/planet.png')
# Resource
planet_manager.add_image('assets/mars.png')
planet_manager.add_image('assets/neptune.png')
# Goal
planet_manager.add_image('assets/earth.png')
planet_manager.generate(96, (Window.base_resolution[0] * 3, Window.base_resolution[1] * 3), 5)

rocket = Rocket(planet_manager.get_neutral_planet().position, camera)
# rocket = Rocket((100, 50), camera)

while True:
    Clock.update()
    camera.update()
    camera.custom_draw(rocket)

    fps_text = Font.font.render(f"FPS : {Clock.clock.get_fps():.1f}", False, (255,255,255))
    Window.display.blit(fps_text, (20, 20))

    Window.input()
    Window.update()


