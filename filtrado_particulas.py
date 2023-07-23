import math
import random
import numpy as np
import matplotlib.pyplot as plt

# Configuración del mundo
landmarks  = [[20.0, 20.0], [80.0, 80.0], [20.0, 80.0], [80.0, 20.0]]
world_size = 100.0

# Implementación genérica del robot
class Robot:
    def __init__(self):
        # Inicialización del robot con ubicación y orientación aleatorias
        self.x = random.random() * world_size
        self.y = random.random() * world_size
        self.orientation = random.random() * 2.0 * math.pi
        
        self.forward_noise = 0.0
        self.turn_noise    = 0.0
        self.sense_noise   = 0.0
    
    def set(self, new_x, new_y, new_orientation):
        if new_x < 0 or new_x >= world_size:
            raise ValueError('Coordenada X fuera de límites')
        if new_y < 0 or new_y >= world_size:
            raise ValueError('Coordenada Y fuera de límites')
        if new_orientation < 0 or new_orientation >= 2 * math.pi:
            raise ValueError('La orientación debe estar en el rango [0..2pi]')
        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation)

    def set_noise(self, new_f_noise, new_t_noise, new_s_noise):
        self.forward_noise = float(new_f_noise);
        self.turn_noise    = float(new_t_noise);
        self.sense_noise   = float(new_s_noise);
    
    # Aplicar movimiento con ruido al robot
    def nueva_posicion(self, girar, avanzar):
        if avanzar < 0:
            raise ValueError('El robot no puede retroceder')
        
        # Girar, y agregar aleatoriedad al comando de giro
        orientacion = self.orientation + float(girar) + random.gauss(0.0, self.turn_noise)
        orientacion %= 2 * math.pi
        
        # Avanzar, y agregar aleatoriedad al comando de movimiento
        distancia = float(avanzar) + random.gauss(0.0, self.forward_noise)
        x = self.x + (math.cos(orientacion) * distancia)
        y = self.y + (math.sin(orientacion) * distancia)
        x %= world_size    # Truncar cíclicamente
        y %= world_size

        return x, y, orientacion
    
    # Modelo de ruido utilizando distribuciones Gaussianas
    def Gaussiana(self, mu, sigma, x):
        # Calcula la probabilidad de x para una Gaussiana unidimensional con media mu y varianza sigma
        return math.exp(- ((mu - x) ** 2) / (sigma ** 2) / 2.0) / math.sqrt(2.0 * math.pi * (sigma ** 2))
    
# Clase PacMan
class PacMan(Robot):
    # El PacMan puede sensar su ubicación usando los landmarks
    def sensar(self):
        Z = []
        for i in range(len(landmarks)):
            distancia = math.sqrt((self.x - landmarks[i][0]) ** 2 + (self.y - landmarks[i][1]) ** 2)
            distancia += random.gauss(0.0, self.sense_noise)
            Z.append(distancia)
        return Z

    # Calcula la probabilidad de una medición
    def probabilidad_medicion(self, medicion):
        probabilidad = 1.0
        for i in range(len(landmarks)):
            distancia = math.sqrt((self.x - landmarks[i][0]) ** 2 + (self.y - landmarks[i][1]) ** 2)
            probabilidad *= self.Gaussiana(distancia, self.sense_noise, medicion[i])
        return probabilidad

    def mover(self, girar, avanzar):
        x, y, orientacion = self.nueva_posicion(girar, avanzar)
        resultado = PacMan()
        resultado.set(x, y, orientacion)
        resultado.set_noise(self.forward_noise, self.turn_noise, self.sense_noise)
        return resultado

# Clase Fantasma
class Fantasma(Robot):
    # El PacMan ("mypacman") puede sensar su distancia al Fantasma
    def sensar(self, mypacman):
        Z = math.sqrt((self.x - mypacman.x) ** 2 + (self.y - mypacman.y) ** 2) + random.gauss(0.0, self.sense_noise)
        return Z

    # Calcula la probabilidad de una medición
    def probabilidad_medicion(self, medicion, mypacman):
        distancia = math.sqrt((self.x - mypacman.x) ** 2 + (self.y - mypacman.y) ** 2)
        probabilidad = self.Gaussiana(distancia, self.sense_noise, medicion)
        return probabilidad

    def mover(self, girar, avanzar):
        x, y, orientacion = self.nueva_posicion(girar, avanzar)
        resultado = Fantasma()
        resultado.set(x, y, orientacion)
        resultado.set_noise(self.forward_noise, self.turn_noise, self.sense_noise)
        return resultado

# Visualización del mundo con la distribución de partículas
def mostrar_creenca(mypacman, particulas_pacman, myfantasma, particulas_fantasma):
    plt.rcParams["figure.figsize"] = (5,5)

    for p in particulas_pacman:
        plt.plot(p.x, p.y, marker=(3, 0, 180.0*p.orientation/math.pi), markerfacecolor='red', markersize=10, markeredgewidth=0.0, alpha=.3, linestyle='None')

    plt.plot(mypacman.x, mypacman.y, marker=(3, 0, 180.0*mypacman.orientation/math.pi), markerfacecolor='black', markersize=20, markeredgewidth=0.0, linestyle='None')

    for p in particulas_fantasma:
        plt.plot(p.x, p.y, marker=(5, 0, 180.0*p.orientation/math.pi), markerfacecolor='green', markersize=10, markeredgewidth=0.0, alpha=.3, linestyle='None')

    plt.plot(myfantasma.x, myfantasma.y, marker=(5, 0, 180.0*myfantasma.orientation/math.pi), markerfacecolor='black', markersize=20, markeredgewidth=0.0, linestyle='None')

    for x, y in landmarks:
          plt.plot(x, y, marker='o', markersize=20, markeredgewidth=2.0, markerfacecolor='None', markeredgecolor='blue')

    plt.xlim([0,100])
    plt.ylim([0,100])

    plt.show()

# Medir la proximidad entre la ubicación real y la distribución de partículas
def evaluar(real, particulas):
    suma = 0.0;
    for i in range(len(particulas)):
        dx = (particulas[i].x - real.x + (world_size/2.0)) % world_size - (world_size/2.0)
        dy = (particulas[i].y - real.y + (world_size/2.0)) % world_size - (world_size/2.0)
        error = math.sqrt(dx * dx + dy * dy)
        suma += error
    return suma / float(len(particulas))

# Inicialización del PacMan y el Fantasma
ruido_avance = 3.0 
ruido_giro = 0.05
ruido_sensores = 3.0

mypacman = PacMan()
mypacman.set_noise(ruido_avance, ruido_giro, ruido_sensores)

myfantasma = Fantasma()
myfantasma.set_noise(ruido_avance, ruido_giro, ruido_sensores)

# Distribución de partículas
N = 1000 # número de partículas
T = 10   # número de movimientos

# Inicializar partículas aleatorias para el PacMan y el Fantasma
particulas_pacman = []
particulas_fantasma = []
for i in range(N):
    x = PacMan()
    x.set_noise(ruido_avance, ruido_giro, ruido_sensores)
    particulas_pacman.append(x)
    x = Fantasma()
    x.set_noise(ruido_avance, ruido_giro, ruido_sensores)
    particulas_fantasma.append(x)

mostrar_creenca(mypacman, particulas_pacman, myfantasma, particulas_fantasma)

print("Distancia promedio del PacMan:", evaluar(mypacman, particulas_pacman))
print("Distancia promedio del Fantasma:", evaluar(myfantasma, particulas_fantasma))

for giro in range(T):
    print('\nTurno #{}'.format(giro+1))

    # Movimiento real del PacMan
    # Girar 0.1 y avanzar 10 metros
    mypacman = mypacman.mover(0.2, 10.0)

    # Movimiento real del Fantasma (aleatorio)
    giro_fantasma = (random.random()-0.5)*(math.pi/2.0) # ángulo aleatorio en [-45,45]
    distancia_fantasma = random.random()*20.0           # distancia aleatoria en [0,20]
    myfantasma = myfantasma.mover(giro_fantasma, distancia_fantasma)

    # Avance del tiempo
    # Mover las partículas utilizando el mismo movimiento realizado por el robot
    particulas_pacman2 = []
    particulas_fantasma2 = []
    for i in range(N):
        particulas_pacman2.append(particulas_pacman[i].mover(0.2, 10.0))
        particulas_fantasma2.append(particulas_fantasma[i].mover(giro_fantasma, distancia_fantasma))
    particulas_pacman = particulas_pacman2
    particulas_fantasma = particulas_fantasma2

    mostrar_creenca(mypacman, particulas_pacman, myfantasma, particulas_fantasma)
    print("Distancia promedio del PacMan antes del remuestreo:", evaluar(mypacman, particulas_pacman))
    print("Distancia promedio del Fantasma antes del remuestreo:", evaluar(myfantasma, particulas_fantasma))

    # Observar
    ZP = mypacman.sensar()        # medición ruidosa de la distancia entre el PacMan y los landmarks
    ZG = myfantasma.sensar(mypacman) # medición ruidosa de la distancia entre el PacMan y el Fantasma

    w_pacman = []
    for particula in particulas_pacman:
        peso = particula.probabilidad_medicion(ZP) # Calcula la probabilidad de la medición para cada partícula del PacMan
        w_pacman.append(peso)
    
    # Ponderación de las partículas del Fantasma
    w_fantasma = []
    for i, particula in enumerate(particulas_fantasma):
        peso = particula.probabilidad_medicion(ZG, particulas_pacman[i])  # Utiliza particulas_pacman[i] en lugar de mypacman
        w_fantasma.append(peso)
    
    # Paso 2: Remuestreo de partículas
    # Remuestreo de las partículas del PacMan
    particulas_pacman2 = []
    indice_pacman = int(random.random() * N)  # Selecciona un índice aleatorio para iniciar el remuestreo
    beta_pacman = 0.0
    max_peso_pacman = max(w_pacman)
    for i in range(N):
        beta_pacman += random.random() * 2.0 * max_peso_pacman
        while beta_pacman > w_pacman[indice_pacman]:
            beta_pacman -= w_pacman[indice_pacman]
            indice_pacman = (indice_pacman + 1) % N
        particulas_pacman2.append(particulas_pacman[indice_pacman]) # Crea una nueva partícula a partir de la partícula seleccionada
    
    # Remuestreo de las partículas del Fantasma
    particulas_fantasma2 = []
    indice_fantasma = int(random.random() * N)  # Selecciona un índice aleatorio para iniciar el remuestreo
    beta_fantasma = 0.0
    max_peso_fantasma = max(w_fantasma)
    for i in range(N):
        beta_fantasma += random.random() * 2.0 * max_peso_fantasma
        while beta_fantasma > w_fantasma[indice_fantasma]:
            beta_fantasma -= w_fantasma[indice_fantasma]
            indice_fantasma = (indice_fantasma + 1) % N
        particulas_fantasma2.append(particulas_fantasma[indice_fantasma]) # Crea una nueva partícula a partir de la partícula seleccionada
    
    # Actualiza las listas de partículas del PacMan y del Fantasma con las partículas remuestreadas
    particulas_pacman = particulas_pacman2
    particulas_fantasma = particulas_fantasma2

    mostrar_creenca(mypacman, particulas_pacman, myfantasma, particulas_fantasma)
    print("Distancia promedio del PacMan después del remuestreo:", evaluar(mypacman, particulas_pacman))
    print("Distancia promedio del Fantasma después del remuestreo:", evaluar(myfantasma, particulas_fantasma))
