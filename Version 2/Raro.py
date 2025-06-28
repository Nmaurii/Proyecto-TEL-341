import random
from math import sqrt
import networkx as nx
import matplotlib.pyplot as plt

from Nodo import *
from Graph import *

def inicializar_nodos(cantidad, x, y, v_min, v_max, pause_time):
    return [Nodo(i, x, y, v_min, v_max, pause_time) for i in range(cantidad)]

def reiniciar(nodos_obj):

    if len(nodos_obj) != 0:
        for nodo in nodos_obj:
            nodo.connections = 0

def distancia(x1, y1, x2, y2):
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)

def agregar_nodos(nodos_existentes, n_nuevos, area_x, area_y, v_min, v_max, pause_time):

    id_inicial = len(nodos_existentes)
    nuevos_nodos = []
    for i in range(n_nuevos):
        nuevo_id = id_inicial + i
        nodo = Nodo(nuevo_id, area_x, area_y, v_min, v_max, pause_time)
        nuevos_nodos.append(nodo)
    nodos_existentes.extend(nuevos_nodos)

def generar_conexiones(nodos_obj, enlaces, tolerancia, maximo):
    enlaces.clear()
    reiniciar(nodos_obj)
    for i in range(len(nodos_obj)):
        for j in range(i + 1, len(nodos_obj)):
            dist = distancia(nodos_obj[i].x, nodos_obj[i].y, nodos_obj[j].x, nodos_obj[j].y)

            if dist <= tolerancia and (nodos_obj[i].connections <= maximo and nodos_obj[j].connections <= maximo):
                peso = int(dist)
                enlaces.append([nodos_obj[i].id, nodos_obj[j].id, peso])
                nodos_obj[i].connections += 1
                nodos_obj[j].connections += 1

def crear_grafo(nodos_obj, enlaces):

    G = nx.Graph()
    for nodo in nodos_obj:

        G.add_node(str(nodo.id), pos=(nodo.x, nodo.y))

    for enlace in enlaces:
        nodo1_id, nodo2_id, peso = enlace
        G.add_edge(str(nodo1_id), str(nodo2_id), weight=peso)
    return G

def visualizar_red(G, area_x, area_y, titulo="Red MANET"):

    plt.figure(figsize=(8, 6))
    pos = nx.get_node_attributes(G, 'pos')
    nx.draw(G, pos, with_labels=True, node_size=300, node_color='skyblue', font_size=8, font_weight='bold')
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7)
    plt.title(titulo)
    plt.xlim(-5, area_x + 5)
    plt.ylim(-5, area_y + 5)
    plt.grid(True)

def latencia(ruta, latencias=[0.005, 0.005, 0.003, 0.020]):

    enrutamiento = len(ruta[1:len(ruta)-1])
    return float(latencias[0] + latencias[1] + enrutamiento * latencias[2]) + (enrutamiento + 1) * latencias[3]
