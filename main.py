import pygame, random

from scripts.window import Window
from scripts.camera import Camera
from scripts.objek.planet import Planet
from scripts.objek.rocket import Rocket

window = Window()
camera = Camera()

list_planet = []
for i in range(10):
    x = random.randint(0, 640)
    y = random.randint(0, 360)
    planet = Planet((x, y), camera)
    planet.image = pygame.transform.rotate(planet.image, random.randint(-180, 180))
    list_planet.append(planet)


rocket = Rocket(random.choice(list_planet).rect.center, camera)
# rocket = Rocket((100, 50), camera)

while True:
    camera.update()
    camera.custom_draw(rocket)

    window.input()
    window.draw()


