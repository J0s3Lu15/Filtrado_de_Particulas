# Filtrado de Partículas
Este repositorio contiene un programa en Python que implementa el filtrado de partículas para realizar la localización del PacMan y el Fantasma en un entorno con landmarks predefinidos.

## Configuración del Entorno
El entorno se configura con landmarks representados por sus coordenadas [x, y]. La dimensión del mundo se establece en 100.0 unidades.

## Clase Robot Genérica
El programa proporciona una implementación genérica de un robot que puede ser tanto el PacMan como el Fantasma. Esta clase contiene métodos para establecer la posición y la orientación del robot, así como la función para aplicar ruido a los movimientos del robot.

## Clase PacMan
La clase PacMan hereda de la clase robot genérica y tiene características específicas. El PacMan puede sensar su ubicación usando los landmarks y también puede calcular la probabilidad de una medición.

## Clase Fantasma
La clase Fantasma también hereda de la clase robot genérica. El Fantasma puede sensar la distancia entre él mismo y el PacMan, y calcular la probabilidad de una medición.

## Visualización del Entorno y Partículas
El programa incluye una función para visualizar el entorno y la distribución de partículas del PacMan y el Fantasma. La visualización muestra la posición y orientación del PacMan y el Fantasma, así como la distribución de las partículas representada por puntos en el gráfico.

## Ejecución del Programa
Para ejecutar el programa:
```bash
python filtrado_particulas.py
```
Al ejecutar el programa, se inicializa el PacMan y el Fantasma, y se definen los parámetros de ruido para los movimientos y las mediciones. Luego, se realizan una serie de movimientos y mediciones simulados para el PacMan y el Fantasma. Durante cada iteración, se realiza el paso de previsión, seguido del paso de actualización (pesado y remuestreo) para las partículas de ambos robots.

## Contactos:
Si te gusta mi trabajo o estás buscando consultoría para tus proyectos, Pentesting, servicios de RED TEAM - BLUE TEAM, implementación de normas de seguridad e ISOs, controles IDS - IPS, gestión de SIEM, implementación de topologías de red seguras, entrenamiento e implementación de modelos de IA, desarrollo de sistemas, Apps Móviles, Diseño Gráfico, Marketing Digital y todo lo relacionado con la tecnología, no dudes en contactarme al +591 75764248 y con gusto trabajare contigo.
