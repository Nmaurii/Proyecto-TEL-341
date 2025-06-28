import random
import time
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


#funcion que desde un nodo mas paquetes a todos los de la red
def broadcast(g,nodo,nodos,LATENCIA,ACK,MENSAJES):

    ACK,MENSAJES,LAT = 0,0,0

    for _ in range(len(nodos)):

        if(_ != nodo):
            distancia, ruta = g.dijkstra(str(nodo), str(_))
            MENSAJES+=1

            if(distancia != float('inf') and distancia != 0):
                lat = latencia(ruta)
                #print(f"Ruta más corta de {nodo} a {_}: {ruta}, Distancia: {distancia} \nLatencia: {lat}")
                ACK+=1
                LAT+=lat
            #else:
                #print(f"No hay ruta desde {nodo} hasta {_}")

    LATENCIA.append((LAT/len(nodos),len(nodos)))

    return ACK,MENSAJES

def simular(nodos,enlaces,TIEMPO_SIMULACION_EXTRA,TIME_STEP,TIEMPO,TOLERANCIA_CONEXION,CONEXIONES_MAX_NODO, AREA_X, AREA_Y,LATENCIA,ACK,MENSAJES,PROMEDIOS_MENSAJES_aCK):

    cantidad_total_nodos = len(nodos)
    for t in range(TIEMPO_SIMULACION_EXTRA):
        TIEMPO +=1

        # Mover TODOS los nodos (los antiguos y los nuevos)
        for nodo in nodos:
            nodo.move_step(TIME_STEP)

        generar_conexiones(nodos, enlaces, TOLERANCIA_CONEXION, CONEXIONES_MAX_NODO - 1)

        # Recrear los grafos para reflejar el nuevo número de nodos
        G = crear_grafo(nodos, enlaces)
        g = Graph(cantidad_total_nodos)

        for i in range(len(nodos)):
            g.add_vertex_data(i, str(i))
        for n1, n2, peso in enlaces:
            g.add_edge(n1, n2, peso)

        visualizar_red(G, AREA_X, AREA_Y, f"Red con {len(nodos)} nodos.")
        plt.show()

        ack,mensajes = broadcast(g,0,nodos,LATENCIA,ACK,MENSAJES)
        ACK+=ack
        MENSAJES+=mensajes
        PROMEDIOS_MENSAJES_aCK.append((len(nodos),(ACK/MENSAJES)))
        print(f"Mensajes entregados {(ACK/MENSAJES)*100}%")

        time.sleep(0.1)
