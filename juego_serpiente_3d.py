import pygame
import random
import sys
import os
from math import sin, cos

pygame.init()
pygame.mixer.init()

# Enhanced settings for 3D
ANCHO = 800
ALTO = 600
PROFUNDIDAD = 400
FOV = 60
TAMANO_BLOQUE = 20
VELOCIDAD = 15

# Colors with metallic effect
NEGRO = (15, 15, 20)
BLANCO = (255, 255, 255)
ROJO = (220, 50, 50)
VERDE_METALICO = (100, 200, 100)
DORADO = (212, 175, 55)

# Initialize 3D display
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('🐍 3D Snake 🐍')
reloj = pygame.time.Clock()

# Load and scale background image
try:
    fondo = pygame.image.load('assets/background.jpg')
    fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
except:
    # Create a gradient background if image not found
    fondo = pygame.Surface((ANCHO, ALTO))
    for y in range(ALTO):
        # Ensure color values are within valid range (0-255)
        r = min(255, int(0))
        g = min(255, int(50 + y/4))
        b = min(255, int(100 + y/3))
        color = (r, g, b)
        pygame.draw.line(fondo, color, (0, y), (ANCHO, y))

class Serpiente3D:
    def __init__(self):
        self.posicion = [ANCHO//2, ALTO//2, 0]
        self.cuerpo = [[ANCHO//2, ALTO//2, 0]]
        self.direccion = [1, 0, 0]
        self.ultima_direccion = self.direccion  # Previene giros de 180 grados
        
    # Al inicio del archivo, después de pygame.mixer.init()
    try:
        sonido_comer = pygame.mixer.Sound('sounds/eat.wav')
        sonido_colision = pygame.mixer.Sound('sounds/collision.wav')
        sonido_movimiento = pygame.mixer.Sound('sounds/move.wav')
    except:
        # Crear sonidos básicos si no se encuentran los archivos
        sonido_comer = pygame.mixer.Sound.play(pygame.mixer.Sound(bytes([128]*88200)))
        sonido_colision = pygame.mixer.Sound.play(pygame.mixer.Sound(bytes([64]*44100)))
        sonido_movimiento = pygame.mixer.Sound.play(pygame.mixer.Sound(bytes([32]*22050)))
    
    # En la parte donde la serpiente come
    if (abs(serpiente.posicion[0] - comida[0]) < TAMANO_BLOQUE and 
        abs(serpiente.posicion[1] - comida[1]) < TAMANO_BLOQUE):
        sonido_comer.play()  # Añadir sonido
        comida = [random.randrange(TAMANO_BLOQUE, ANCHO-TAMANO_BLOQUE),
                 random.randrange(TAMANO_BLOQUE, ALTO-TAMANO_BLOQUE),
                 0]
        puntuacion += 10
    
    # En la parte donde detecta colisión
    if serpiente.colision():
        sonido_colision.play()  # Añadir sonido
        game_over = True
    
    # En la parte donde se mueve la serpiente
    def mover(self):
        sonido_movimiento.play()  # Añadir sonido
        self.ultima_direccion = self.direccion.copy()
        self.posicion = [
            self.posicion[0] + self.direccion[0] * TAMANO_BLOQUE,
            self.posicion[1] + self.direccion[1] * TAMANO_BLOQUE,
            self.posicion[2] + self.direccion[2] * TAMANO_BLOQUE
        ]
        self.cuerpo.insert(0, list(self.posicion))
    def dibujar(self, superficie):
        tiempo = pygame.time.get_ticks() / 1000
        for i, pos in enumerate(self.cuerpo):
            # 3D effect with shadow and highlight
            z_effect = (sin(tiempo + i * 0.1) + 1) * 5
            size = max(5, TAMANO_BLOQUE - pos[2] / 20)
            
            x = pos[0] + cos(tiempo + i * 0.2) * 2
            y = pos[1] + z_effect
            
            # Metallic gradient effect
            color_base = (
                100 + int(sin(tiempo + i * 0.1) * 50),
                200 + int(sin(tiempo + i * 0.2) * 50),
                100 + int(sin(tiempo + i * 0.3) * 50)
            )
            
            # Draw 3D segment
            pygame.draw.ellipse(superficie, color_base, 
                              (x - size/2, y - size/2, size, size))
            
            # Highlight
            pygame.draw.ellipse(superficie, BLANCO, 
                              (x - size/4, y - size/4, size/4, size/4))
    def colision(self):
        # Check wall collision
        if (self.posicion[0] >= ANCHO or self.posicion[0] < 0 or
            self.posicion[1] >= ALTO or self.posicion[1] < 0):
            return True
        # Check self collision
        for segmento in self.cuerpo[1:]:
            if self.posicion[0] == segmento[0] and self.posicion[1] == segmento[1]:
                return True
        return False
def dibujar_comida_3d(pos, tiempo):
    # Floating effect
    y_offset = sin(tiempo * 2) * 5
    size = TAMANO_BLOQUE + sin(tiempo * 3) * 2
    
    # Draw glowing orb
    color = (255, int(128 + sin(tiempo * 5) * 127), 50)
    pygame.draw.circle(pantalla, color, 
                      (int(pos[0]), int(pos[1] + y_offset)), int(size))
    
    # Inner glow
    pygame.draw.circle(pantalla, BLANCO,
                      (int(pos[0]), int(pos[1] + y_offset)), int(size/3))
def main():
    running = True
    high_score = 0  # Añadimos high score
    
    while running:
        serpiente = Serpiente3D()
        comida = [random.randrange(TAMANO_BLOQUE, ANCHO-TAMANO_BLOQUE),
                  random.randrange(TAMANO_BLOQUE, ALTO-TAMANO_BLOQUE),
                  0]
        game_over = False
        puntuacion = 0
        ultima_actualizacion = pygame.time.get_ticks()
        
        while not game_over:
            tiempo_actual = pygame.time.get_ticks()
            tiempo = tiempo_actual / 1000  # Añadimos esta línea para definir 'tiempo'
            delta_tiempo = tiempo_actual - ultima_actualizacion
            
            if delta_tiempo >= 1000 / VELOCIDAD:  # Control de FPS consistente
                ultima_actualizacion = tiempo_actual
                serpiente.mover()
                
                if serpiente.colision():
                    game_over = True
                    high_score = max(high_score, puntuacion)
                    continue
            # Event handling
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    running = False
                    game_over = True
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_UP and serpiente.direccion != [0, 1, 0]:
                        serpiente.direccion = [0, -1, 0]
                    elif evento.key == pygame.K_DOWN and serpiente.direccion != [0, -1, 0]:
                        serpiente.direccion = [0, 1, 0]
                    elif evento.key == pygame.K_LEFT and serpiente.direccion != [1, 0, 0]:
                        serpiente.direccion = [-1, 0, 0]
                    elif evento.key == pygame.K_RIGHT and serpiente.direccion != [-1, 0, 0]:
                        serpiente.direccion = [1, 0, 0]
            # Game logic
            serpiente.mover()
            
            if (abs(serpiente.posicion[0] - comida[0]) < TAMANO_BLOQUE and 
                abs(serpiente.posicion[1] - comida[1]) < TAMANO_BLOQUE):
                comida = [random.randrange(TAMANO_BLOQUE, ANCHO-TAMANO_BLOQUE),
                         random.randrange(TAMANO_BLOQUE, ALTO-TAMANO_BLOQUE),
                         0]
                puntuacion += 10
            else:
                serpiente.cuerpo.pop()
                
            if serpiente.colision():
                game_over = True
            # Render
            pantalla.blit(fondo, (0, 0))
            
            luz_superficie = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            radio_luz = abs(sin(tiempo)) * 200 + 300
            pygame.draw.circle(luz_superficie, (255, 255, 255, 30),
                             (ANCHO//2, ALTO//2), radio_luz)
            pantalla.blit(luz_superficie, (0, 0))
            
            dibujar_comida_3d(comida, tiempo)
            serpiente.dibujar(pantalla)
            
            fuente = pygame.font.Font(None, 48)
            texto = fuente.render(f'Score: {puntuacion}', True, DORADO)
            sombra = fuente.render(f'Score: {puntuacion}', True, NEGRO)
            pantalla.blit(sombra, (12, 12))
            pantalla.blit(texto, (10, 10))
            # Actualizar puntuación máxima
            texto_high_score = fuente.render(f'High Score: {high_score}', True, DORADO)
            pantalla.blit(texto_high_score, (ANCHO - 200, 10))
            pygame.display.flip()
            reloj.tick(VELOCIDAD)
        # Game Over screen
        if running:  # Only show if not quitting
            pantalla.fill(NEGRO)
            fuente_grande = pygame.font.Font(None, 72)
            texto_game_over = fuente_grande.render('Game Over!', True, ROJO)
            texto_rect = texto_game_over.get_rect(center=(ANCHO//2, ALTO//2))
            pantalla.blit(texto_game_over, texto_rect)
            
            texto_puntuacion = fuente.render(f'Final Score: {puntuacion}', True, BLANCO)
            texto_puntuacion_rect = texto_puntuacion.get_rect(center=(ANCHO//2, ALTO//2 + 50))
            pantalla.blit(texto_puntuacion, texto_puntuacion_rect)
            
            texto_reiniciar = fuente.render('Press R to Restart', True, VERDE_METALICO)
            texto_reiniciar_rect = texto_reiniciar.get_rect(center=(ANCHO//2, ALTO//2 + 100))
            pantalla.blit(texto_reiniciar, texto_reiniciar_rect)
            
            pygame.display.flip()
            
            # Wait for restart or quit
            waiting = True
            while waiting and running:
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        running = False
                        waiting = False
                    elif evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_r:
                            waiting = False
                reloj.tick(VELOCIDAD)
    pygame.quit()
    sys.exit()
if __name__ == "__main__":
    main()