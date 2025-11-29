
import pygame
import numpy as np
import random
import time
import pandas as pd
import matplotlib.pyplot as plt  # type: ignore


# PARÁMETROS DEL ENTORNO
GRID_SIZE = 25
CELL_SIZE = 25
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE

START = (3, 2)
GOAL = (GRID_SIZE-1, GRID_SIZE-4)
ACCIONES = ['avanzar', 'izquierda', 'derecha']

# OBSTÁCULOS
obstaculos = [
    (0,0),(0,1),(0,2),(0,10),(0,11),(0,12),(0,13),(0,14),(0,15),(0,16),(0,17),
    (0,18),(0,19),(0,20),(0,21),(0,22),(0,23),(0,24),
    (0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(11,0),
    (12,0),(13,0),(14,0),(15,0),(16,0),(17,0),(18,0),(19,0),(20,0),(21,0),(22,0),
    (23,0),(24,0),(24,1),(24,2),
    (24,1),(24,2),(24,10),(24,11),(24,12),(24,13),(24,14),(24,15),(24,16),(24,17),
    (24,18),(24,19),(24,23),(24,24),
    (0,24),(1,24),(2,24),(5,24),(6,24),(7,24),(8,24),(9,24),(10,24),(11,24),(16,24),(17,24),(18,24),
    (19,24),(20,24),(21,24),(22,24),(23,24),
    (0,13),(1,13),(2,13),(3,13),(4,13),(5,13),(6,13),(7,13),(8,13),(9,13), (13,13), (14,13),
    (6,14),(6,18),(6,19),(6,20),(6,21),(6,22),(6,23),
    (14,0),(14,1),(14,2),(14,3),(14,4),(14,5),(14,6),(14,7),(14,8),(14,9),(14,10),(14,11),(14,12),(14,13),
    (18,13),(19,13),(20,13),(21,13),(22,13),(23,13),
    (1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8),(1,9),(1,10),(2,1),(2,2),(2,3),(2,4),(2,5),(2,6),(2,7),(2,8),(2,9),(2,10),
    (3,3),(3,4),(3,5),(3,6),(3,7),(3,8),
    (4,3),(4,4),(4,5),(4,6),(4,7),(4,8),
    (5,3),(5,4),(5,5),(5,6),(5,7),(5,8),
    (6,3),(6,4),(6,5),(6,6),(6,7),(6,8),
    (7,3),(7,4),(7,5),(7,6),(7,7),(7,8),
    (8,3),(8,4),(8,5),(8,6),(8,7),(8,8),
    (9,3),(9,4),(9,5),(9,6),(9,7),(9,8),
    (12,2),(12,3),(12,4),(12,5),(12,6),(12,7),(12,8),
    (13,2),(13,3),(13,4),(13,5),(13,6),(13,7),(13,8),
    (21,1),(21,2),(21,3),(21,4),
    (20,1),(20,2),(20,3),(20,4),
    (19,1),(19,2),(19,3),(19,4),
    (18,1),(18,2),(18,3),(18,4),
    (17,1),(17,2),(17,3),(17,4),
    (16,1),(16,2),(16,3),(16,4),
    (15,1),(15,2),(15,3),(15,4),
    (22,1),(22,2),(22,3),(22,4),
    (23,1),(23,2),(23,3),(23,4),
    (1,21),(1,22),(2,21),(2,22),
    (3,19),(3,20),(3,18),(4,19),(4,20),(4,18),(5,19),(5,20),(5,18),
    (7,18),(7,19),(7,20),(7,21),(7,22),(7,23),
    (8,18),(8,19),(8,20),(8,21),(8,22),(8,23),
    (9,18),(9,19),(9,20),(9,21),(9,22),(9,23),
    (12,19),(12,20),(13,17),(13,18),(13,19),(13,20),(13,21),
    (14,16),(14,17),(14,18),(14,19),(14,20),(14,21),(14,22),
    (15,16),(15,17),(15,18),(15,19),(15,20),(15,21),(15,22),
    (16,17),(16,18),(16,19),(16,20),(16,21),
    (17,17),(17,18),(17,19),(17,20),(17,21),
    (18,19),(18,20)
]

# PYGAME
pygame.init()
pantalla = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Agente RL Pygame")
clock = pygame.time.Clock()

# CARGAR IMÁGENES
img_robot = pygame.image.load(r"D:\IA\robot.png")
img_robot = pygame.transform.scale(img_robot, (CELL_SIZE, CELL_SIZE))
img_meta = pygame.image.load(r"D:\IA\meta.png")
img_meta = pygame.transform.scale(img_meta, (CELL_SIZE, CELL_SIZE))
img_obst = pygame.image.load(r"D:\IA\obstaculo.png")
img_obst = pygame.transform.scale(img_obst, (CELL_SIZE, CELL_SIZE))

# CARGAR FONDO DEL PLANO
try:
    fondo = pygame.image.load(r"D:\ia ia\Plano.jpg")   
    fondo = pygame.transform.scale(fondo, (WIDTH, HEIGHT))
    print("Fondo cargado correctamente.")
except Exception as e:
    print("ERROR cargando fondo:", e)
    fondo = None

# DIBUJAR ENTORNO
def dibujar_entorno(pos_agente):
    if fondo:
        pantalla.blit(fondo, (0, 0))   
    else:
        pantalla.fill((255, 255, 255)) 

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            x = j * CELL_SIZE
            y = i * CELL_SIZE
            if (i, j) == GOAL:
                pantalla.blit(img_meta, (x, y))
            elif (i, j) == pos_agente:
                pantalla.blit(img_robot, (x, y))
            #elif (i, j) in obstaculos:
           #     pantalla.blit(img_obst, (x, y)) 
            #else: pass
    pygame.display.update()

# MOVIMIENTO DEL AGENTE
def mover(pos, orient, accion):
    i, j = pos
    if accion == 'izquierda':
        orient = (orient - 1) % 4
        return pos, orient
    if accion == 'derecha':
        orient = (orient + 1) % 4
        return pos, orient
    if accion == 'avanzar':
        if orient == 0: nueva = (i-1, j)
        elif orient == 1: nueva = (i, j+1)
        elif orient == 2: nueva = (i+1, j)
        else: nueva = (i, j-1)
        if nueva in obstaculos or nueva[0]<0 or nueva[0]>=GRID_SIZE or nueva[1]<0 or nueva[1]>=GRID_SIZE:
            return pos, orient
        return nueva, orient
    return pos, orient

# RECOMPENSA
def obtener_recompensa(pos):
    if pos == GOAL: return 10
    if pos in obstaculos: return -5
    return -0.1

# TABLA Q
epsilon = 0.9
alpha = 0.6
gamma = 0.9
Q = {}

def obtener_Q(estado, accion):
    return Q.get((estado, accion), 0.0)

def elegir_accion(estado, epsilon_local):
    if random.uniform(0,1) < epsilon_local:
        return random.choice(ACCIONES)
    valores = {a: obtener_Q(estado,a) for a in ACCIONES}
    return max(valores, key=valores.get)

def actualizar_Q(estado, accion, recompensa, sig_estado):
    mejor_accion_sig = max([obtener_Q(sig_estado, a) for a in ACCIONES])
    actual = obtener_Q(estado, accion)
    Q[(estado, accion)] = actual + alpha * (recompensa + gamma*mejor_accion_sig - actual)

# ENTRENAMIENTO
EPISODIOS = 5000
PASOS_MAX = 200
recompensas_medias = []
acciones_optimas = []

for ep in range(EPISODIOS):
    pos = START
    orient = 1
    total_recompensa = 0
    for paso in range(PASOS_MAX):
        estado = (pos, orient)
        accion = elegir_accion(estado, epsilon)
        nueva_pos, nueva_orient = mover(pos, orient, accion)
        recompensa = obtener_recompensa(nueva_pos)
        total_recompensa += recompensa
        sig_estado = (nueva_pos, nueva_orient)
        actualizar_Q(estado, accion, recompensa, sig_estado)
        #print(f"Episodio {ep+1}: Última posición {pos}, Última acción {accion}, Recompensa total {total_recompensa}")
        pos, orient = nueva_pos, nueva_orient
        if pos == GOAL:
            break
    recompensas_medias.append(total_recompensa)
    acciones_optimas.append(int(accion == 'avanzar'))
    epsilon = max(0.05, epsilon*0.995)

# SIMULACIÓN EXPLOTACIÓN
epsilon = 0
pos = START
orient = 1
running = True
ejecutando = False  

while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_i: 
                ejecutando = True
            if e.key == pygame.K_p:
                ejecutando = False
    if ejecutando:
        estado = (pos, orient)
        accion = elegir_accion(estado, epsilon)
        pos, orient = mover(pos, orient, accion)
    dibujar_entorno(pos)
    clock.tick(5)
    if pos == GOAL:
        print("¡Meta alcanzada!")
        time.sleep(2)
        running = False

# MOSTRAR TABLA Q
pd.set_option('display.max_colwidth', None)
tabla_Q = pd.DataFrame([
    {'estado': list(e), 'valor': round(v, 2)}
    for (e, a), v in Q.items()
])
tabla_ordenada = tabla_Q.sort_values(by='valor', ascending=False)
print(tabla_ordenada)

# PRECISIÓN DEL MÉTODO E-GREEDY

precision_total = sum(acciones_optimas) / len(acciones_optimas)
print("Precisión del agente (ε-greedy):", round(precision_total * 100, 2), "%")

# PYGAME
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()


#grafica

plt.figure(figsize=(7,6))
plt.plot(acciones_optimas, marker='o', linestyle='-', markersize=3, linewidth=1)
plt.title('Precisión del agente por episodio (ε-greedy)', fontsize=16, weight='bold')
plt.xlabel('Episodios', fontsize=12)
plt.ylabel('1 = Acción óptima / 0 = No óptima', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()



