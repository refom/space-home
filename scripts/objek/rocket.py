
import pygame, math
from ..Clock import Clock
from ..camera import Camera
from ..Vector import Vector2D
from ..planet_manager import PlanetManager

from ..astar import AStar

class Rocket(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.img = pygame.image.load('assets/rocket.png').convert_alpha()
        self.image = self.img.copy()
        self.rect = self.image.get_rect(center = pos)

        self.position = Vector2D(pos)
        self.target_pos = Vector2D(pos)
        self.isClick = False

        self.path = []
        self.speed = 100

    def input(self):
        click = pygame.mouse.get_pressed()

        if (click[0] == 1 and not self.isClick):
            self.isClick = True
            self.set_target()
        elif (click[0] == 0 and self.isClick):
            self.isClick = False

    def movement(self):
        if (len(self.path) > 1):
            self.target_pos = self.path[1].position

            if (Vector2D.Distance(self.position, self.target_pos) < self.speed * Clock.delta_time):
                self.path.pop(0)

        self.position = Vector2D.MoveTowards(self.position, self.target_pos, self.speed * Clock.delta_time)
        # print(f"{self.rect.center} - {self.target_pos} - {self.position}")

    def render(self):
        direction = Vector2D.Subtraction(self.target_pos, self.position)
        angle = math.atan2(direction.y, direction.x) # Radians
        angle = math.degrees(angle) # Degrees
        # dikurang 90 biar angleny mulai dari kanan
        self.image = pygame.transform.rotate(self.img, -angle - 90)

        # Radius Search
        pygame.draw.circle(
            Camera.instance.display,
            (100, 100, 0),
            Camera.instance.world_to_screen_point(self.position),
            PlanetManager.instance.radius_search,
            width=1
        )
        # Path
        for i in range(len(self.path) - 1):
            pygame.draw.line(
                Camera.instance.display,
                (255,255,255),
                Camera.instance.world_to_screen_point(self.path[i].position),
                Camera.instance.world_to_screen_point(self.path[i+1].position),
                width=1
            )

    def update(self):
        self.input()
        self.movement()
        self.render()
        self.rect.center = self.position
    
    def is_arrive(self):
        if (Vector2D.Distance(self.position, self.target_pos) <= (self.speed * Clock.delta_time)):
            return True
        return False
    
    def set_target(self):
        # check collision with planet
        pos = Camera.instance.screen_to_world_point(pygame.mouse.get_pos())
        planet_collide = PlanetManager.instance.check_collision(pos)
        # print(f"planet collide: {planet_collide}")

        # if get planet, set target to planet
        if (len(planet_collide) < 1): return
        # search path to target
        current_planet = self.get_current_planet() # Planet object
        if (current_planet == None): return

        path_planets = AStar.search(current_planet, planet_collide[0])
        if (not path_planets): return
        print(f"Planet Path: {[planet.position for planet in path_planets]}")
        self.path = path_planets

        # self.target_pos = planet_collide[0].rect.center
        # print(self.target_pos)

    def get_current_planet(self):
        planet = PlanetManager.instance.check_collision(self.target_pos)
        if (len(planet) > 0):
            print(f"Current Planet: {planet[0].position}")
            return planet[0]
        return None