from Graph import Graph
from Raro import *

# conf inicial
cantidad_nodos = 5
area_x, area_y = 30, 30
tolerancia_conexion = 20
conexione_maxima_nodo = 5


#_____METRICAS
LATENCIA = []

# nodos y enlaces
nodos = inicializar_nodos(cantidad_nodos, area_x, area_y)
enlaces = []
generar_conexiones(nodos, enlaces, tolerancia_conexion,conexione_maxima_nodo-1)

# objeto clase grafo y objeto clase de NetwoekX, esta ultima se encarga de visualizar el grafo

G = crear_grafo(nodos, enlaces)  # Grafo NetworkX para visualización
g = Graph(len(nodos))  # Grafo para Dijkstra

# Configurar grafo de Dijkstra
#NOTAR QUE SE AGREGAR EL LA ETIQUETA SEGUIDO DEL IDENTIFICADOR DEL GRAFO
for i in range(len(nodos)):
    g.add_vertex_data(i, str(i))

for nodo1, nodo2, peso in enlaces:
    g.add_edge(nodo1, nodo2, peso)

# VISULIZAR inicial
print("\n--- ESTADO INICIAL ---")
visualizar_red(G, area_x, area_y, "Estado Inicial")

# Calcular ruta corta inicial ESTA DEBERIA CALCULARSE DESDE EL NODO Tx HASTA EL NODO Rx
try:
    distance, path = g.dijkstra('0', str(len(nodos)-1))
    LATENCIA.append((len(nodos),latencia(path)))
    print(f"\nRuta más corta inicial de 0 a {len(nodos)-1}: {path}, Distancia: {distance}")
    print(f"LATENCIA : {latencia(path)}")

except ValueError as e:
    print(f"\nError al calcular ruta inicial: {e}")





############

for _ in range(10):
    agregar_nodo(nodos,area_x, area_y)

del G
del g

generar_conexiones(nodos, enlaces, tolerancia_conexion,conexione_maxima_nodo-1)

# objeto clase grafo y objeto clase de NetwoekX, esta ultima se encarga de visualizar el grafo

G = crear_grafo(nodos, enlaces)  # Grafo NetworkX para visualización
g = Graph(len(nodos))  # Grafo para Dijkstra

# Configurar grafo de Dijkstra
#NOTAR QUE SE AGREGAR EL LA ETIQUETA SEGUIDO DEL IDENTIFICADOR DEL GRAFO
for i in range(len(nodos)):
    g.add_vertex_data(i, str(i))

for nodo1, nodo2, peso in enlaces:
    g.add_edge(nodo1, nodo2, peso)



# VISULIZAR inicial
print("\n--- ESTADO INICIAL ---")
visualizar_red(G, area_x, area_y, "Estado al agregar nodo")

# Calcular ruta corta inicial ESTA DEBERIA CALCULARSE DESDE EL NODO Tx HASTA EL NODO Rx
try:
    distance, path = g.dijkstra('0', str(len(nodos)-1))
    LATENCIA.append((len(nodos),latencia(path)))
    print(f"\nRuta más corta inicial de 0 a {len(nodos)-1}: {path}, Distancia: {distance}")
    print(f"LATENCIA : {latencia(path)}")
except ValueError as e:
    print(f"\nError al calcular ruta inicial: {e}")


# Simular movimiento EN ESTE CASO SE SIMULAN 3 CAMBIOS DE POSICION
print("\n--- SIMULANDO MOVIMIENTO ---")
generar_movimiento(nodos, enlaces, 5, cantidad_nodos, area_x, area_y)

# DADO QUE HUBO UN MOVIMIENTO SE LIBERA LA MEMORIA de G y g, se vuelven a definir dado la lista nodos y enalces, ESTAS SE ACTUALIZAN
del G
del g
del distance
del path

#Se actualiza los grafos (ambos objetos) del movimiento, iniciando desde cero una nueva configuacion
G = crear_grafo(nodos, enlaces)
g = Graph(len(nodos))  # Reiniciar grafo de Dijkstra

for i in range(len(nodos)):
    g.add_vertex_data(i, str(i))

for nodo1, nodo2, peso in enlaces:
    g.add_edge(nodo1, nodo2, peso)

print("\n--- ESTADO FINAL ---")
visualizar_red(G, area_x, area_y, "Estado despues del movimiento")

# Calcular ruta sol cuando se deberia mandar un mensaje
try:
    distance, path = g.dijkstra('0',str(len(nodos)-1))
    print(f"\nRuta más corta final de 0 a {len(nodos)-1}: {path}, Distancia: {distance}")
    print(f"LATENCIA : {latencia(path)}")
except ValueError as e:
    print(f"\nError al calcular ruta final: {e}")

#SOLO SE CALCULA EL CAMINO OPTIMO UNA VEZ QUE SE DESEA MANDAR UN MENSAJE, ES EN ESTE MOMENTO QUE SE RECALCULAN LAS TABLAS DE ENRRUTAMIENTO

for _ in range(10):
    agregar_nodo(nodos,area_x, area_y)

generar_conexiones(nodos, enlaces, tolerancia_conexion,conexione_maxima_nodo-1)

# objeto clase grafo y objeto clase de NetwoekX, esta ultima se encarga de visualizar el grafo

G = crear_grafo(nodos, enlaces)  # Grafo NetworkX para visualización
g = Graph(len(nodos))  # Grafo para Dijkstra

# Configurar grafo de Dijkstra
#NOTAR QUE SE AGREGAR EL LA ETIQUETA SEGUIDO DEL IDENTIFICADOR DEL GRAFO
for i in range(len(nodos)):
    g.add_vertex_data(i, str(i))

for nodo1, nodo2, peso in enlaces:
    g.add_edge(nodo1, nodo2, peso)



# VISULIZAR inicial
print("\n--- ESTADO INICIAL ---")
visualizar_red(G, area_x, area_y, "Estado al agregar nodo")

# Calcular ruta corta inicial ESTA DEBERIA CALCULARSE DESDE EL NODO Tx HASTA EL NODO Rx
try:
    distance, path = g.dijkstra('0', str(len(nodos)-1))
    LATENCIA.append((len(nodos),latencia(path)))
    print(f"\nRuta más corta inicial de 0 a {len(nodos)-1}: {path}, Distancia: {distance}")
    print(f"LATENCIA : {latencia(path)}")
except ValueError as e:
    print(f"\nError al calcular ruta inicial: {e}")

n_nodos = [d[0] for d in LATENCIA]
latencias = [d[1] for d in LATENCIA]

plt.figure(figsize=(8, 5))
plt.plot(n_nodos, latencias, marker='o', linestyle='-', color='b', label='Latencia vs Nodos')

plt.title("Latencia en función del número de nodos", fontsize=14)
plt.xlabel("Número de nodos", fontsize=12)
plt.ylabel("Latencia (ms)", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()

plt.show()
