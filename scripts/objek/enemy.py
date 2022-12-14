
import pygame, math, random
from ..components.Clock import Clock
from ..components.Vector import Vector2D
from ..manager.PlanetManager import PlanetManager

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, groups, speed, cooldown_move = [3, 7]):
        super().__init__(groups)
        self.img = pygame.image.load('assets/enemy_ship.png').convert_alpha()
        self.image = self.img.copy()
        self.rect = self.image.get_rect(center = pos)

        self.active = True
        self.position = Vector2D(pos)
        self.target_pos = Vector2D(pos)
        self.current_planet = None

        self.speed = speed
        self.cooldown_move_range = cooldown_move
        self.cooldown_move = random.randint(self.cooldown_move_range[0], self.cooldown_move_range[1])
        self.cooldown_timer = 0
        self.can_move = True

    def update(self):
        if (not self.active): return
        self.movement()
        self.render()
        self.rect.center = self.position

    def render(self):
        direction = Vector2D.Subtraction(self.target_pos, self.position)
        angle = math.atan2(direction.y, direction.x) # Radians
        angle = math.degrees(angle) # Degrees
        # dikurang 90 biar angleny mulai dari kanan
        self.image = pygame.transform.rotate(self.img, -angle - 90)

    def movement(self):
        if (not self.can_move):
            self.cooldown()
            return

        if (self.is_arrive()):
            self.set_cooldown()
        self.position = Vector2D.MoveTowards(self.position, self.target_pos, self.speed * Clock.delta_time)

    def set_cooldown(self):
        self.current_planet.is_enemy_arrive = True
        self.can_move = False
        self.cooldown_move = random.randint(self.cooldown_move_range[0], self.cooldown_move_range[1])
        # print(f"Enemy cooldown : {self.cooldown_move}")

    def cooldown(self):
        self.cooldown_timer += Clock.delta_time
        if (self.cooldown_timer >= self.cooldown_move):
            # cooldown selesai
            # print("Cooldown Done")
            self.cooldown_timer -= self.cooldown_move
            self.can_move = True
            self.set_target()

    def is_arrive(self):
        # print("is arrive")
        if (Vector2D.Distance(self.position, self.target_pos) <= (self.speed * Clock.delta_time)):
            return True
        return False

    def set_target(self):
        # ambil closest planet, cek apakah ada enemy disana
        planets = PlanetManager.instance.get_closest_planets(self.position)
        # print(f"Enemy planets option: {[planet.position for planet in planets]}")
        new_planet = None
        for idx in range(len(planets) - 1):
            if (planets[idx].is_enemy_exist or planets[idx] == PlanetManager.instance.planet_goal):
                continue
            new_planet = planets[idx]
            break

        if (new_planet == None):
            # print("set Cooldown from set target")
            self.set_cooldown()
            return
        
        # print(f"Enemy current planet: {self.current_planet.position}")
        # print(f"Enemy new planet: {new_planet.position}")
        self.current_planet.is_enemy_arrive = False
        self.current_planet.is_enemy_exist = False
        self.target_pos = new_planet.position
        self.current_planet = new_planet
        self.current_planet.is_enemy_exist = True

