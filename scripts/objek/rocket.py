
import pygame, math, random
from ..Clock import Clock
from ..camera import Camera
from ..Vector import Vector2D
from ..GameManager import GameManager
from ..PlanetManager import PlanetManager
from ..Particle import Particle

from ..AStar import AStar

class Rocket(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.img = pygame.image.load('assets/rocket.png').convert_alpha()
        self.image = self.img.copy()
        self.rect = self.image.get_rect(center = pos)

        self.active = True
        self.position = Vector2D(pos)
        self.target_pos = Vector2D(pos)
        self.is_click = False
        self.can_move = True

        self.path = []
        self.last_path = None
        self.current_planet = None
        self.speed = 100
        self.radar_color = {
            "default": (100, 100, 0),
            "goal": (50, 205, 50),
        }
        self.arrow_color = {
            "default": (244, 157, 26),
            "goal": (173, 231, 146),
        }
        self.radar_radius = PlanetManager.instance.radius2
        
        self.particle = Particle(
            [(255, 255, 100), (180, 180, 100)],
            lifetime = 0.80,
            radius = (5, 7)
        )

        self.timer_radar = 0
        self.timer_radar_cooldown = 0
        self.timer_resource = 0

    def input(self):
        if (not self.can_move): return
        click = pygame.mouse.get_pressed()

        if (click[0] == 1 and not self.is_click):
            self.is_click = True
            self.set_target()
        elif (click[0] == 0 and self.is_click):
            self.is_click = False

    def movement(self):
        # Saat sampai tujuan
        if self.is_arrive():
            self.can_move = True

            # masih ada target tujuan
            if (len(self.path) > 1):
                self.can_move = False
                self.target_pos = self.path[1].position

                if self.is_arrive():
                    self.path.pop(0)
            return

        # particle boost
        direction = Vector2D.Subtraction(self.position, self.target_pos).normalize()
        # directiony = Vector2D.MultiplyByPointY(direction, random.randint(5, 10))
        offset = self.position + (direction * 7)
        self.particle.add_particle(offset, direction)
        self.particle.add_particle(offset, direction)
        # self.particle.add_particle(offset, directiony)

        self.position = Vector2D.MoveTowards(self.position, self.target_pos, self.speed * Clock.delta_time)
        # print(f"{self.rect.center} - {self.target_pos} - {self.position}")

    def render(self):
        direction = Vector2D.Subtraction(self.target_pos, self.position)
        angle = math.atan2(direction.y, direction.x) # Radians
        angle = math.degrees(angle) # Degrees
        # dikurang 90 biar angleny mulai dari kanan
        self.image = pygame.transform.rotate(self.img, -angle - 90)

        self.particle.emit()
        self.draw_radar()
        self.draw_path()
        self.draw_arrow()

    def check_event(self):
        # cek apakah sedang jalan
        if (not self.can_move):
            self.timer_resource = 0
            return

        # apakah current planet ada?
        if (self.current_planet == None):
            self.current_planet = self.get_current_planet()

        # apakah current planet adalah planet yang sama dengan target
        if (self.current_planet.position != self.target_pos):
            print("adalah bukan planet yang sama")
            self.current_planet = self.get_current_planet()

        # apakah planet goal
        if (self.current_planet == PlanetManager.instance.planet_goal):
            # win
            GameManager.win_condition()
            self.active = False
            return

        # apakah ada enemy sampai di planet ini
        if (self.current_planet.is_enemy_arrive):
            # dead
            GameManager.lose_condition()
            self.active = False
            return

        # apakah planet resource dan belum diambil
        if (self.current_planet.collected or not self.current_planet.is_resource):
            # print("planet sudah diambil atau bukan planet resource")
            return

        # Cooldown ngambil resource
        # print("cooldown")
        self.timer_resource += Clock.delta_time
        self.current_planet.draw_load_resource(self.timer_resource)
        if (self.timer_resource >= self.current_planet.resource_cooldown):
            # resource diambil
            print("resource diambil")
            self.current_planet.collected = True
            self.timer_resource = 0
            GameManager.resource_collected()

    def update(self):
        if (not self.active): return
        self.input()
        self.movement()
        self.check_event()
        self.render()
        self.rect.center = self.position
    
    def draw_path(self):
        # Draw line path
        for i in range(len(self.path) - 1):
            pygame.draw.line(
                Camera.instance.display,
                (100,100,100),
                Camera.instance.world_to_screen_point(self.path[i].position),
                Camera.instance.world_to_screen_point(self.path[i+1].position),
                width=1
            )

    def draw_radar(self):
        if (self.timer_radar_cooldown > 0):
            self.timer_radar_cooldown -= self.speed * Clock.delta_time
            return

        self.timer_radar += Clock.delta_time
        if (self.timer_radar > 1):
            self.timer_radar -= 1
            self.timer_radar_cooldown += self.radar_radius
            
        # Radius dan width circle for radar
        timer = Vector2D.EaseOutCubic(self.timer_radar)
        radius = timer * self.radar_radius
        width = (1 - timer) * self.radar_radius
        color = self.radar_color["default"]
        if (GameManager.open_planet_goal):
            color = self.radar_color["goal"]

        pygame.draw.circle(
            Camera.instance.display,
            color,
            Camera.instance.world_to_screen_point(self.position),
            radius = radius,
            width = math.ceil(width)
        )

    def draw_arrow(self):
        if (GameManager.open_planet_goal):
            planet = PlanetManager.instance.planet_goal
            color = self.arrow_color["goal"]
        else:
            planet = PlanetManager.instance.get_closest_resource_planet(self.position)
            color = self.arrow_color["default"]

        if (planet == None): return
        if (planet.position == self.target_pos): return

        direction = (planet.position - self.position).normalize()
        perpendicular = Vector2D.PerpendicularCounterClockwise(direction)
        offset = self.position + (direction * 23)

        triangle = [
            Camera.instance.world_to_screen_point(offset + (direction * 17)),
            Camera.instance.world_to_screen_point(offset + (perpendicular * 9)),
            Camera.instance.world_to_screen_point(offset + (perpendicular * -9))
        ]
        pygame.draw.polygon(
            Camera.instance.display,
            color,
            triangle
        )

    def is_arrive(self):
        if (Vector2D.Distance(self.position, self.target_pos) <= (self.speed * Clock.delta_time)):
            return True
        return False
    
    def set_target(self):
        # check collision with planet
        pos = Camera.instance.screen_to_world_point(pygame.mouse.get_pos())
        planet_collide = PlanetManager.instance.check_collision(pos)
        # print(f"planet collide: {planet_collide}")

        # cek kalau yang di klik adalah planet
        if (len(planet_collide) < 1): return
        current_planet = self.get_current_planet() # Planet object
        if (current_planet == None): return

        # Search path to planet target
        path_planets = AStar.search(current_planet, planet_collide[0])
        if (not path_planets): return
        print(f"Planet Path: {[planet.position for planet in path_planets]}")
        self.path = path_planets
        self.can_move = False

        # self.target_pos = planet_collide[0].rect.center
        # print(self.target_pos)

    def get_current_planet(self):
        planet = PlanetManager.instance.check_collision(self.target_pos)
        if (len(planet) > 0):
            print(f"Current Planet: {planet[0].position}")
            return planet[0]
        return None