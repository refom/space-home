
import random
from .objek.planet import Planet
from .camera import Camera

class PlanetManager:
    # Singleton
    instance = None

    def __init__(self) -> None:

        self.planets = []
        self.groups = Camera.instance
        
        if (PlanetManager.instance == None):
            PlanetManager.instance = self

    def generate(self, amount):
        for i in range(amount):
            x = random.randint(0, 640)
            y = random.randint(0, 360)
            planet = Planet((x, y), 'assets/planet.png', self.groups)
            planet.angle = random.randint(-180, 180)
            self.planets.append(planet)

    def check_collision(self, point):
        return [planet for planet in self.planets if planet.collider.collidepoint(point)]
