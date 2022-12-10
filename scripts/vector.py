import math
from pygame.math import Vector2

def sign(x):
    return (x > 0) - (x < 0)

def move_towards(current, target, maxDelta):
    if (abs(target - current) <= maxDelta):
        return target
    return current + sign(target - current) * maxDelta
    
def get_magnitude(x, y):
    return math.sqrt(x * x + y * y)

def lerp(current, target, delta):
    return current + delta * (target - current)

class Vector2D(Vector2):
    @classmethod
    def Addition(cls, current, target):
        return Vector2(current[0] + target[0], current[1] + target[1])

    @classmethod
    def Subtraction(cls, current, target):
        return Vector2(current[0] - target[0], current[1] - target[1])
    
    @classmethod
    def Distance(cls, vec_1, vec_2):
        return math.sqrt( (vec_2[0] - vec_1[0])**2 + (vec_2[1] - vec_1[1])**2 )

    @classmethod
    def MoveTowards(cls, current, target, maxDelta):
        vector = Vector2D.Subtraction(target, current)
        magnitude = get_magnitude(vector[0], vector[1])

        if (magnitude <= maxDelta or magnitude == 0):
            return target
        
        x = current[0] + vector[0] / magnitude * maxDelta
        y = current[1] + vector[1] / magnitude * maxDelta
        return Vector2(x, y)
    
    @classmethod
    def LerpPoint(cls, current, target, delta):
        return current + delta * (target - current)

    # @classmethod
    # def Lerp(cls, current, target, delta):
    #     x = lerp(current[0], target[0], delta)
    #     y = lerp(current[1], target[1], delta)
    #     return Vector2(x, y)

