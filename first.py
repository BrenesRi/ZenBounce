import sys
import pygame
import random
import math

# Inicializa Pygame
pygame.init()
resX, resY = 108 * 4, 192 * 4  # Establece el tamaño actual
screen = pygame.display.set_mode((resX, resY))

# Posición y radio del círculo principal
circle_pos = (resX // 2, resY // 2)
circle_radius = resX / 2.1
circle_width = int((resX / 2.2) / 40)

# Color inicial del círculo principal
main_circle_color = (255, 255, 255)  # Blanco

# Configuración de la bola más pequeña
ball_radius = 18
ball_pos = [resX // 2, resY // 2]
ball_vel = [5, 5]

# VALORES MODIFICABLES
gravity = 0.38
bounce_damping = 1.05
max_speed = 15

# Configuración de estrellas
num_stars = 300  # Número de estrellas
stars = []
for _ in range(num_stars):
    while True:
        x = random.randint(0, resX)
        y = random.randint(0, resY)
        distance_from_center = math.sqrt((x - circle_pos[0]) ** 2 + (y - circle_pos[1]) ** 2)
        if distance_from_center >= circle_radius:  # Asegurarse de que no esté dentro del círculo
            brightness = random.random()  # Brillo aleatorio para cada estrella
            stars.append((x, y, brightness))
            break

# Rastro de la bola
trail = []
trail_length = 10  # Longitud del rastro

# Función para obtener un color basado en el tiempo
def get_ball_color():
    time = pygame.time.get_ticks() * 0.001  # Obtiene el tiempo en segundos
    r = int((math.sin(time + 0) + 1) / 2 * 255)  # Componente rojo
    g = int((math.sin(time + 2) + 1) / 2 * 255)  # Componente verde
    b = int((math.sin(time + 4) + 1) / 2 * 255)  # Componente azul
    return (r, g, b)

# Bucle principal del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Dibuja el fondo negro
    screen.fill((0, 0, 0))

    # Dibuja las estrellas con animación de entrada y salida
    for i, (x, y, brightness) in enumerate(stars):
        # Brillo variable con animación de entrada y salida
        brightness = (math.sin(pygame.time.get_ticks() * 0.001 + i) + 1) / 2  # Parpadeo suave
        brightness = min(max(0, brightness), 1)  # Asegúrate de que esté entre 0 y 1
        star_size = int(3 * brightness)  # Tamaño basado en el brillo (más grandes)

        if star_size > 0:  # Solo dibujar si el tamaño es mayor que 0
            color = (255, 255 * brightness, 255)  # Color blanco con brillo variable
            pygame.draw.circle(screen, color, (x, y), star_size)

    # Obtener el color actual de la bola
    ball_color = get_ball_color()
    
    # Lógica de rebote 
    ball_vel[1] += gravity
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    distance_from_center = math.sqrt((ball_pos[0] - circle_pos[0]) ** 2 + (ball_pos[1] - circle_pos[1]) ** 2)
    
    if distance_from_center + ball_radius > circle_radius:
        normal_x = (ball_pos[0] - circle_pos[0]) / distance_from_center
        normal_y = (ball_pos[1] - circle_pos[1]) / distance_from_center
        dot_product = ball_vel[0] * normal_x + ball_vel[1] * normal_y
        ball_vel[0] -= 2 * dot_product * normal_x * bounce_damping
        ball_vel[1] -= 2 * dot_product * normal_y * bounce_damping
        ball_vel[0] = max(-max_speed, min(max_speed, ball_vel[0]))
        ball_vel[1] = max(-max_speed, min(max_speed, ball_vel[1]))
        ball_pos[0] = circle_pos[0] + (circle_radius - ball_radius) * normal_x
        ball_pos[1] = circle_pos[1] + (circle_radius - ball_radius) * normal_y
        
        # Cambiar el color del círculo principal al color de la bola en colisión
        main_circle_color = ball_color

    # Dibuja el círculo principal con el color actualizado
    pygame.draw.circle(screen, main_circle_color, circle_pos, circle_radius, circle_width)
    # Dibuja el fondo gris oscuro dentro del círculo
    pygame.draw.circle(screen, (20, 20, 20), circle_pos, circle_radius - circle_width)  # Resta el ancho del círculo
    
    # Agrega la posición actual de la bola al rastro
    trail.append((int(ball_pos[0]), int(ball_pos[1])))
    if len(trail) > trail_length:
        trail.pop(0)  # Mantiene la longitud del rastro

    # Dibuja el rastro de la bola
    for i, (x, y) in enumerate(trail):
        alpha = int(255 * (1 - (i / trail_length)))  # Reduce la opacidad del rastro
        
        # Calcula el color para cada posición del rastro basado en el tiempo
        r = int((math.sin(pygame.time.get_ticks() * 0.001 + i) + 1) / 2 * 255)
        g = int((math.sin(pygame.time.get_ticks() * 0.001 + i + 2) + 1) / 2 * 255)
        b = int((math.sin(pygame.time.get_ticks() * 0.001 + i + 4) + 1) / 2 * 255)
        color_trail = (r, g, b)

        # Dibuja la bola del rastro con borde blanco
        pygame.draw.circle(screen, (255, 255, 255), (x, y), ball_radius + 3)  # Borde blanco
        pygame.draw.circle(screen, color_trail, (x, y), ball_radius)  # Bola del rastro con color variable

    # Dibuja la bola con color variable y borde blanco
    pygame.draw.circle(screen, (255, 255, 255), (int(ball_pos[0]), int(ball_pos[1])), ball_radius + 3)  # Borde blanco
    pygame.draw.circle(screen, ball_color, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)  # Bola con color variable

    pygame.display.flip()
    pygame.time.delay(20)
