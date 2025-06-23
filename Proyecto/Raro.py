from math import sqrt
import random

import networkx as nx
import matplotlib.pyplot as plt


def distancia(x1,y1,x2,y2):
    return sqrt((x2-x1)**2+(y2-y1)**2)


def inicializar_nodos(cantidad,x,y):
    return [[random.randint(0,x),random.randint(0,y)] for _ in range(cantidad)]

def generar_conexiones(nodos, enlaces, tolerancia):

    enlaces.clear()
    for i in range(len(nodos)):
        for j in range(i + 1, len(nodos)):
            dist = distancia(nodos[i][0], nodos[i][1], nodos[j][0], nodos[j][1])
            if dist <= tolerancia:
                peso = int(dist)
                enlaces.append([i, j, peso])

def generar_pesos(enlaces,posiciones):
    for nodos in enlaces:
        calcular_peso(nodos,posiciones)

def calcular_peso(nodos,posiciones):
    x1,y1 = posiciones[nodos[0]][0],posiciones[nodos[0]][1]
    x2,y2 = posiciones[nodos[1]][0],posiciones[nodos[1]][1]
    peso = distancia(x1,y1,x2,y2)
    nodos[2] = int(peso)

def generar_movimiento(nodos,enlaces,veces,cantidad,x,y):

    print(nodos)

    for variacion in range(veces):
        nodo = random.randint(0,cantidad-1)

        nodos[nodo][0] = abs(nodos[nodo][0] + random.randint(-1,1))
        nodos[nodo][1] = abs(nodos[nodo][1] + random.randint(-1,+1))


        generar_pesos(enlaces,nodos)

        print(nodos)

def crear_grafo(nodos, enlaces):

    G = nx.Graph()
    for i, (x, y) in enumerate(nodos):
        G.add_node(str(i), pos=(x, y))

    for enlace in enlaces:
        nodo1, nodo2, peso = enlace
        G.add_edge(str(nodo1), str(nodo2), weight=peso)

    return G

#AQUI USE GPT PARA VISUALIZAR
def visualizar_red(G, area_x, area_y, titulo="Red MANET"):

    plt.figure(figsize=(10, 8))

    pos = nx.get_node_attributes(G, 'pos')

    try:
        nx.draw(G, pos, with_labels=True, node_size=500,
               node_color='skyblue', font_weight='bold')

        edge_labels = nx.get_edge_attributes(G, 'weight')
        if edge_labels:
            try:
                nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
            except:
                nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels,
                                           label_pos=0.5, font_size=8)

        plt.title(titulo)
        plt.xlim(-5, area_x + 5)
        plt.ylim(-5, area_y + 5)
        plt.grid(True)
        plt.show()
    except Exception as e:
        print(f"Error al visualizar el grafo: {e}")
        plt.close()

#ESTE CODIGO ES EL QUE HICE PERO NO ERA BUENO
'''
def print_grafo(G):

    pos = nx.circular_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=700, node_color="skyblue")
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title("Grafo Ponderado")
    plt.show()
'''
