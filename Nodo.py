# En Raro.py
import random
from math import sqrt

class Nodo:

    def __init__(self, id, area_x, area_y, v_min=1, v_max=5, pause_time=3, modelo_movilidad = "random_waypoint"):
        self.id = id
        self.area_x = area_x
        self.area_y = area_y
        self.v_min = v_min
        self.v_max = v_max
        self.max_pause = pause_time
        self.modelo_movilidad = modelo_movilidad

        self.x = random.uniform(0, self.area_x)
        self.y = random.uniform(0, self.area_y)

        self.dest_x = random.uniform(0, self.area_x)
        self.dest_y = random.uniform(0, self.area_y)
        self.speed = random.uniform(self.v_min, self.v_max)
        self.connections = 0
        self.pause_timer = 0

        self.mensajes_enviados = 0
        self.mensajes_entregados = 0
        self.mensajes_perdidos = 0
        self.desconexiones = 0


    def move_step(self, time_step=1):
        if self.modelo_movilidad == "random_waypoint":
            self.random_waypoint_move(time_step)
        elif self.modelo_movilidad == "lineal":
            self.lineal_move(time_step)


    def random_waypoint_move(self, time_step):
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

    def lineal_move(self, time_step):
        dx = self.dest_x - self.x
        dy = self.dest_y - self.y
        distancia_total = sqrt(dx**2 + dy**2)   

        if distancia_total == 0:
            # Si ya está en destino, elige uno nuevo
            self.dest_x = random.uniform(0, self.area_x)
            self.dest_y = random.uniform(0, self.area_y)
            self.speed = random.uniform(self.v_min, self.v_max)
            return

        distancia_movimiento = self.speed * time_step

        if distancia_total <= distancia_movimiento:
            self.x = self.dest_x
            self.y = self.dest_y
            self.dest_x = random.uniform(0, self.area_x)
            self.dest_y = random.uniform(0, self.area_y)
            self.speed = random.uniform(self.v_min, self.v_max)
        else:
            self.x += (dx / distancia_total) * distancia_movimiento
            self.y += (dy / distancia_total) * distancia_movimiento

        # Rebote en bordes
        self.x = max(0, min(self.x, self.area_x))
        self.y = max(0, min(self.y, self.area_y))

