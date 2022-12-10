
import random, math
from .objek.planet import Planet
from .camera import Camera
from .Vector import Vector2D

class PlanetManager:
    # Singleton
    instance = None

    def __init__(self) -> None:
        self.image_path = []

        self.planets = []
        self.planet_resources = []
        self.planet_goal = None
        self.groups = Camera.instance

        self.radius_search = 192

        if (PlanetManager.instance == None):
            PlanetManager.instance = self
    
    def spawn_planet(self, pos):
        # last item adalah path ke planet goal
        end = len(self.image_path) - 2
        if (self.planet_goal == None):
            end = len(self.image_path) - 1
        index = random.randint(0, random.randint(0, random.randint(0, end)))

        planet = Planet(pos, self.image_path[index], self.groups, (32, 32))
        planet.angle = random.randint(-180, 180)

        # jika planet goal
        if (index == len(self.image_path) - 1):
            planet.visible = False
            self.planet_goal = planet
            return
        # jika planet resource
        elif (index != 0 and index != len(self.image_path) - 1):
            planet.is_resource = True
            self.planet_resources.append(planet)

        self.planets.append(planet)
    
    def add_image(self, path):
        self.image_path.append(path)
    
    def get_neutral_planet(self):
        while True:
            index = random.randint(0, len(self.planets))
            if (self.planets[index] not in self.planet_resources):
                return self.planets[index]

    # random generate with blue noise/poisson disc sampling
    def generate(self, radius, map_size, try_length=30):
        random.seed(random.randint(1, 5))
        map_size = map_size
        cell_size = radius / math.sqrt(2)
        maps = [
            [0 for _ in range(math.ceil(map_size[1] / cell_size))]
            for _ in range(math.ceil(map_size[0] / cell_size))
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
                if (self.is_valid(candidate, radius, points, map_size, cell_size, maps)):
                    points.append(candidate)
                    spawn_points.append(candidate)
                    maps[int(candidate.x / cell_size)][int(candidate.y / cell_size)] = len(points)
                    candidate_accepted = True
                    break
            if (not candidate_accepted):
                del spawn_points[spawn_index]
        
        for i in range(len(points)):
            self.spawn_planet(points[i])
        
        print(f"Planets : {len(points)}")
        print(f"Planet Resources : {len(self.planet_resources)}")
        print(f"Planet Goal : {self.planet_goal}, {self.planet_goal.position}")

    def is_valid(self, candidate, radius, points, map_size, cell_size, maps):
        # in maps
        if (candidate.x > 0 and
            candidate.x < map_size[0] and
            candidate.y > 0 and
            candidate.y < map_size[1]):
            
            cell_x = int(candidate.x / cell_size)
            cell_y = int(candidate.y / cell_size)

            search_start_x = max(0, cell_x - 2)
            search_end_x = min(cell_x + 2, len(maps))

            search_start_y = max(0, cell_y - 2)
            search_end_y = min(cell_y + 2, len(maps[0]))

            for x in range(search_start_x, search_end_x):
                for y in range(search_start_y, search_end_y):
                    point_index = maps[x][y] - 1
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
