
import random, pygame
from .camera import Camera

class Particle:
    def __init__(self, color, lifetime, radius = (3, 5)):
        # color = [(), ()] color isinya list warna
        self.color = color
        self.radius_range = radius
        self.lifetime = lifetime
        # isi dari particle {pos, radius, direction, color}
        self.particles = []
    
    def emit(self):
        self.remove_particle()
        if self.particles:
            for particle in self.particles:
                particle["pos"][0] += particle["direction"][0]
                particle["pos"][1] += particle["direction"][1]
                particle["radius"] -= self.lifetime
                # particle["direction"][0] += particle["direction"][0]
                # particle["direction"][1] += particle["direction"][1]
                
                pygame.draw.circle(
                    Camera.instance.display,
                    particle["color"],
                    Camera.instance.world_to_screen_point(particle["pos"]),
                    particle["radius"]
                )

    def add_particle(self, position, direction):
        radius = random.randint(self.radius_range[0], self.radius_range[0])
        color = random.choice(self.color)
        # Make Particle
        particle = {"pos": position, "radius": radius, "direction": direction, "color": color}
        self.particles.append(particle)

    def remove_particle(self):
        particle_copy = [particle for particle in self.particles if particle["radius"] > 0]
        self.particles = particle_copy


