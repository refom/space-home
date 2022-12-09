import pygame, random

from scripts.Window import Window
from scripts.Clock import Clock
from scripts.camera import Camera
from scripts.planet_manager import PlanetManager
from scripts.objek.rocket import Rocket

Window.init()
Clock.init()
camera = Camera()
planet_manager = PlanetManager()
planet_manager.generate(15)

rocket = Rocket(random.choice(planet_manager.planets).rect.center, camera)
# rocket = Rocket((100, 50), camera)

while True:
    Clock.update()
    camera.update()
    camera.custom_draw(rocket)

    Window.input()
    Window.update()


