
import random, math
from .objek.planet import Planet
from .camera import Camera
from .Vector import Vector2D

class PlanetManager:
    # Singleton
    instance = None

    def __init__(self) -> None:

        self.planets = []
        self.groups = Camera.instance

        self.radius_search = 256

        self.map_size = ()
        self.cell_size = 0
        self.maps = []
        
        if (PlanetManager.instance == None):
            PlanetManager.instance = self
    
    def spawn_planet(self, pos):
        planet = Planet(pos, 'assets/planet.png', self.groups, (32, 32))
        planet.angle = random.randint(-180, 180)
        self.planets.append(planet)

    # random generate with blue noise/poisson disc sampling
    def generate(self, radius, map_size, try_length=30):
        random.seed(random.randint(1, 5))
        self.map_size = map_size
        self.cell_size = radius / math.sqrt(2)
        self.maps = [
            [0 for _ in range(math.ceil(map_size[1] / self.cell_size))]
            for _ in range(math.ceil(map_size[0] / self.cell_size))
        ]

        points = []
        spawn_points = []
        spawn_points.append(Vector2D(map_size)/2)

        while (len(spawn_points) > 0):
            spawn_index = random.randint(0, len(spawn_points)-1)
            spawn_center = spawn_points[spawn_index]
            candidate_accepted = False

            for i in range(try_length):
                # get random point terdekat dengan spawn point
                angle = random.random() * math.pi * 2
                dir = Vector2D(math.sin(angle), math.cos(angle))
                candidate = spawn_center + dir * random.randint(radius, 2*radius)

                # cek apakah jarak random point dekat dengan spawn point
                if (self.is_valid(candidate, radius, points)):
                    points.append(candidate)
                    spawn_points.append(candidate)
                    self.maps[int(candidate.x / self.cell_size)][int(candidate.y / self.cell_size)] = len(points)
                    candidate_accepted = True
                    break
            if (not candidate_accepted):
                del spawn_points[spawn_index]
        
        print(f"Planets : {len(points)}")
        for i in range(len(points)):
            self.spawn_planet(points[i])

    def is_valid(self, candidate, radius, points):
        # in maps
        if (candidate.x > 0 and
            candidate.x < self.map_size[0] and
            candidate.y > 0 and
            candidate.y < self.map_size[1]):
            
            cell_x = int(candidate.x / self.cell_size)
            cell_y = int(candidate.y / self.cell_size)

            search_start_x = max(0, cell_x - 2)
            search_end_x = min(cell_x + 2, len(self.maps))

            search_start_y = max(0, cell_y - 2)
            search_end_y = min(cell_y + 2, len(self.maps[0]))

            for x in range(search_start_x, search_end_x):
                for y in range(search_start_y, search_end_y):
                    point_index = self.maps[x][y] - 1
                    if (point_index != -1):
                        sqr_dist = (candidate - points[point_index]).magnitude_squared()
                        if (sqr_dist < radius * radius):
                            return False
            return True
        return False

    def check_collision(self, point):
        return [planet for planet in self.planets if planet.collider.collidepoint(point)]

    def get_closest_planets(self, current):
        open_planets = []
        for planet in self.planets:
            distance = Vector2D.Distance(current, planet.position)

            if (distance <= self.radius_search and distance != 0):
                open_planets.append(planet)

        return open_planets
