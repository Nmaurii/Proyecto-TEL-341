import random
import time
from math import sqrt
import networkx as nx
import matplotlib.pyplot as plt
import collections

from Nodo import *
from Graph import *

def inicializar_nodos(cantidad, area_x, area_y, v_min, v_max, pause_time, modelo_movilidad):
    return [Nodo(i, area_x, area_y, v_min, v_max, pause_time, modelo_movilidad) for i in range(cantidad)]

def reiniciar_conexiones(nodos_obj):

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

def generar_conexiones(nodos_obj, enlaces, rango_transmision, max_conexiones):
    enlaces.clear()
    reiniciar_conexiones(nodos_obj)
    for i in range(len(nodos_obj)):
        for j in range(i + 1, len(nodos_obj)):
            dist = distancia(nodos_obj[i].x, nodos_obj[i].y, nodos_obj[j].x, nodos_obj[j].y)

            if dist <= rango_transmision and (nodos_obj[i].connections <= max_conexiones and nodos_obj[j].connections <= max_conexiones):
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

def topologia_red(G, area_x, area_y, titulo="Red MANET"):

    plt.figure(figsize=(8, 6))
    pos = nx.get_node_attributes(G, 'pos')
    nx.draw(G, pos, with_labels=True, node_size=300, node_color='skyblue', font_size=8, font_weight='bold')
    edge_labels = nx.get_edge_attributes(G, 'weight')
    edge_labels = {k: v for k, v in edge_labels.items() if isinstance(k, tuple) and len(k) == 2}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7)
    plt.title(titulo)
    plt.xlim(-5, area_x + 5)
    plt.ylim(-5, area_y + 5)
    plt.grid(True)


def latencia(ruta, latencias=[0.005, 0.005, 0.003, 0.020]):

    enrutamiento = len(ruta[1:len(ruta)-1])
    return float(latencias[0] + latencias[1] + enrutamiento * latencias[2]) + (enrutamiento + 1) * latencias[3]

def desconexiones(anteriores, actuales, nodos):
    set_anteriores = set(tuple(sorted((e[0], e[1]))) for e in anteriores)
    set_actuales = set(tuple(sorted((e[0], e[1]))) for e in actuales)

    desconexiones = set_anteriores - set_actuales  # Enlaces que desaparecieron
    for nodo1, nodo2 in desconexiones:
        nodos[nodo1].desconexiones += 1
        nodos[nodo2].desconexiones += 1
    return len(desconexiones), desconexiones

#funcion que desde un nodo mas paquetes a todos los de la red
def broadcast(grafo,nodo_emisor,nodos,hist_latencias):

    ack,totales,latencia_total = 0,0,0

    for nodo_receptor in range(len(nodos)):
        

        if(nodo_receptor != nodo_emisor):
            distancia, ruta = grafo.dijkstra(str(nodo_emisor), str(nodo_receptor))
            totales += 1
            nodos[nodo_emisor].mensajes_enviados += 1

            if(distancia != float('inf') and distancia != 0):
                lat = latencia(ruta)
                #print(f"Ruta más corta de {nodo} a {_}: {ruta}, Distancia: {distancia} \nLatencia: {lat}")
                if lat <= 1000:
                    # Mensaje entregado dentro del timeout
                    ack += 1
                    latencia_total += lat
                    nodos[nodo_receptor].mensajes_entregados += 1
                else:
                    # Mensaje perdido por timeout
                    nodos[nodo_receptor].mensajes_perdidos += 1
            else:
                nodos[nodo_receptor].mensajes_perdidos += 1
            #else:
                #print(f"No hay ruta desde {nodo} hasta {_}")
                
                
    if(latencia_total != 0):
        
        hist_latencias.append((len(nodos),latencia_total/ack))

    return ack, totales



def simular(nodos,enlaces,TIEMPO_TOTAL_SIMULACION,duracion_simulacion,TIME_STEP,TIEMPO,rango_transmision,CONEXIONES_MAX_NODO, AREA_X, AREA_Y,LATENCIA,ACK,M_ENVIADOS,TASA_ENTREGA, TASA_ENVIO):

    total_desconexiones = 0
    cantidad_total_nodos = len(nodos)

    for t in range(duracion_simulacion):
        TIEMPO +=1
        TIEMPO_TOTAL_SIMULACION+=1
        # Mover TODOS los nodos (los antiguos y los nuevos)
        for nodo in nodos:
            nodo.move_step(TIME_STEP)

        enlaces_anteriores = enlaces.copy()
        generar_conexiones(nodos, enlaces, rango_transmision, CONEXIONES_MAX_NODO - 1)

        num_desconexiones, enlaces_desconectados = desconexiones(enlaces_anteriores, enlaces, nodos)

        total_desconexiones += num_desconexiones
        # Recrear los grafos para reflejar el nuevo número de nodos
        G = crear_grafo(nodos, enlaces)
        g = Graph(cantidad_total_nodos)

        for i in range(len(nodos)):
            g.add_vertex_data(i, str(i))
        for n1, n2, peso in enlaces:
            g.add_edge(n1, n2, peso)

        if TIEMPO % TASA_ENVIO == 0:

            topologia_red(G, AREA_X, AREA_Y, f"Red con {len(nodos)} nodos en t={TIEMPO_TOTAL_SIMULACION} [s].")
            plt.show()

            ack, mensajes = broadcast(g, 0, nodos, LATENCIA)
            ACK += ack
            M_ENVIADOS += mensajes

            TASA_ENTREGA.append((len(nodos), ACK / M_ENVIADOS))
            print(f"Mensajes entregados {(ACK / M_ENVIADOS) * 100:.2f}%")
            print(f"Desconexiones en este paso: {num_desconexiones}")
            print(f"Desconexiones totales: {total_desconexiones}")

            print("\n📊 Estadísticas por nodo:")
            for nodo in nodos:
                print(f"Nodo {nodo.id} -> Enviados: {nodo.mensajes_enviados}, "
                f"Entregados: {nodo.mensajes_entregados}, Perdidos: {nodo.mensajes_perdidos}, "
                f"Desconexiones: {nodo.desconexiones}")
        time.sleep(0.1)

    return TIEMPO


def promedios(lista):
    
    grupos = collections.defaultdict(list)
    
    for clave,valor in lista:
        grupos[clave].append(valor)
        
    promedios = {clave: sum(valores) / len(valores) for clave, valores in grupos.items()}

    return promedios