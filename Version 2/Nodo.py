# En Raro.py
import random
from math import sqrt

class Nodo:
    def __init__(self, id, area_x, area_y, v_min=1, v_max=5, pause_time=3):
        self.id = id
        self.area_x = area_x
        self.area_y = area_y
        self.v_min = v_min
        self.v_max = v_max
        self.max_pause = pause_time

        self.x = random.uniform(0, self.area_x)
        self.y = random.uniform(0, self.area_y)

        self.dest_x = random.uniform(0, self.area_x)
        self.dest_y = random.uniform(0, self.area_y)
        self.speed = random.uniform(self.v_min, self.v_max)
        self.connections = 0
        self.pause_timer = 0

    def move_step(self, time_step=1):

        if self.pause_timer > 0:
            self.pause_timer -= time_step
            return

        dx = self.dest_x - self.x
        dy = self.dest_y - self.y
        distancia_total = sqrt(dx**2 + dy**2)

        distancia_movimiento = self.speed * time_step

        if distancia_total <= distancia_movimiento:

            self.x = self.dest_x
            self.y = self.dest_y
            self.pause_timer = self.max_pause
            self.dest_x = random.uniform(0, self.area_x)
            self.dest_y = random.uniform(0, self.area_y)
            self.speed = random.uniform(self.v_min, self.v_max)
        else:
            self.x += (dx / distancia_total) * distancia_movimiento
            self.y += (dy / distancia_total) * distancia_movimiento
