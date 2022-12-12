
from ..manager.PlanetManager import PlanetManager
from .Vector import Vector2D

class AStar:
    # h = heuristic
    # n = distance from current planet to planet
    # start, target = Planet Object
    @classmethod
    def search(cls, start, target):
        open_list = [start]
        closed_list = []

        distance_planet = {}
        distance_planet[start] = 0
        parent_planet = {}
        parent_planet[start] = start
        
        while len(open_list) > 0:
            current_planet = None

            # Get lowest f(n + h)
            for planet in open_list:
                if (current_planet == None):
                    current_planet = planet

                # F = n (distance planet to planet) + h (distance planet to target planet)
                f_planet = distance_planet[planet] + Vector2D.Distance(planet.position, target.position)
                f_current = distance_planet[current_planet] + Vector2D.Distance(current_planet.position, target.position)

                if (f_planet < f_current):
                    current_planet = planet
            
            if (current_planet.position == target.position):
                path = []

                while parent_planet[current_planet] != current_planet:
                    path.append(current_planet)
                    current_planet = parent_planet[current_planet]
                
                path.append(start)
                path.reverse()
                # print(f"Path Found: {path}")
                return path

            # get neighbors
            neighbors = PlanetManager.instance.get_closest_planets(current_planet.position)
            for planet in neighbors:
                # calculate distance current planet to planet
                new_n = distance_planet[current_planet] + Vector2D.Distance(current_planet.position, planet.position)
                # add planet to open list
                # set parent to current planet
                if (planet not in open_list and planet not in closed_list):
                    open_list.append(planet)
                    parent_planet[planet] = current_planet
                    distance_planet[planet] = new_n
                else:
                    # if jarak planet lebih besar dari current planet ke planet
                    # update jarak planet menjadi jarak current planet ke planet
                    # ganti parentnya ke current planet
                    if (distance_planet[planet] > new_n):
                        distance_planet[planet] = new_n
                        parent_planet[planet] = current_planet

                        # keluarkan lagi dari closed list
                        if planet in closed_list:
                            p = closed_list.pop(closed_list.index(planet))
                            open_list.append(p)
                
            p = open_list.pop(open_list.index(current_planet))
            closed_list.append(p)

        print("No Path")
        return None


                

            


