import pygame
import random
import sys
import os

pygame.init()
pygame.mixer.init()

# Enhanced colors with neon effect
NEGRO = (15, 15, 20)
BLANCO = (255, 255, 255)
ROJO = (255, 50, 50)
VERDE_NEON = (57, 255, 20)
GRIS = (30, 30, 35)
PURPURA = (147, 0, 211)

# Game settings
ANCHO = 800
ALTO = 600
TAMANO_BLOQUE = 20
VELOCIDAD = 15

# Create window with a title
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('🐍 Neon Snake 🐍')
reloj = pygame.time.Clock()

# Sound effects
pygame.mixer.init()
try:
    # Create simple beep sounds
    def create_eating_sound():
        sound = pygame.mixer.Sound(buffer=bytes([127]*44100))  # 1 second beep
        sound.set_volume(0.2)
        return sound

    def create_collision_sound():
        sound = pygame.mixer.Sound(buffer=bytes([80]*88200))  # 2 second lower beep
        sound.set_volume(0.3)
        return sound

    SONIDO_COMER = create_eating_sound()
    SONIDO_COLISION = create_collision_sound()
except:
    class DummySound:
        def play(self): pass
    SONIDO_COMER = DummySound()
    SONIDO_COLISION = DummySound()
class Serpiente:
    def __init__(self):
        self.posicion = [ANCHO//2, ALTO//2]
        self.cuerpo = [[ANCHO//2, ALTO//2]]
        self.direccion = [1, 0]
        self.color_base = VERDE_NEON
        
    def mover(self):
        self.posicion[0] += self.direccion[0] * TAMANO_BLOQUE
        self.posicion[1] += self.direccion[1] * TAMANO_BLOQUE
        self.cuerpo.insert(0, list(self.posicion))
        
    def colision(self):
        if (self.posicion[0] >= ANCHO or self.posicion[0] < 0 or
            self.posicion[1] >= ALTO or self.posicion[1] < 0):
            return True
        for segmento in self.cuerpo[1:]:
            if self.posicion == segmento:
                return True
        return False

def generar_comida():
    x = random.randrange(0, ANCHO, TAMANO_BLOQUE)
    y = random.randrange(0, ALTO, TAMANO_BLOQUE)
    return [x, y]

def dibujar_grid():
    for x in range(0, ANCHO, TAMANO_BLOQUE):
        alpha = abs(int(pygame.time.get_ticks() / 20) % 255 - 127) + 128
        color_linea = (GRIS[0], GRIS[1], min(alpha, GRIS[2]))
        pygame.draw.line(pantalla, color_linea, (x, 0), (x, ALTO))
    for y in range(0, ALTO, TAMANO_BLOQUE):
        pygame.draw.line(pantalla, color_linea, (0, y), (ANCHO, y))

def dibujar_serpiente(cuerpo):
    tiempo = pygame.time.get_ticks()
    for i, pos in enumerate(cuerpo):
        # Pulsing neon effect
        brillo = abs(int(tiempo / 10) % 50 - 25) + 230
        color = (
            57,  # R
            min(255, brillo),  # G
            20 + min(100, i * 2)  # B
        )
        
        # Draw snake segment with glow effect
        pygame.draw.rect(pantalla, color, [pos[0], pos[1], TAMANO_BLOQUE-1, TAMANO_BLOQUE-1])
        pygame.draw.rect(pantalla, (color[0]//4, color[1]//4, color[2]//4), 
                        [pos[0]-1, pos[1]-1, TAMANO_BLOQUE+1, TAMANO_BLOQUE+1], 1)
        
        # Eyes for head
        if i == 0:
            eye_size = 4
            eye_offset = 4
            # Glowing eyes
            pygame.draw.circle(pantalla, BLANCO, (pos[0] + eye_offset, pos[1] + eye_offset), eye_size+1)
            pygame.draw.circle(pantalla, BLANCO, (pos[0] + TAMANO_BLOQUE - eye_offset, pos[1] + eye_offset), eye_size+1)
            pygame.draw.circle(pantalla, NEGRO, (pos[0] + eye_offset, pos[1] + eye_offset), eye_size)
            pygame.draw.circle(pantalla, NEGRO, (pos[0] + TAMANO_BLOQUE - eye_offset, pos[1] + eye_offset), eye_size)

def dibujar_comida(pos, tiempo):
    # Pulsing food effect
    radio = TAMANO_BLOQUE//2 + abs(int(tiempo/100) % 4 - 2)
    brillo = abs(int(tiempo / 10) % 50 - 25) + 230
    color_comida = (min(255, brillo), 50, 50)
    
    centro = (pos[0] + TAMANO_BLOQUE//2, pos[1] + TAMANO_BLOQUE//2)
    pygame.draw.circle(pantalla, color_comida, centro, radio)
    pygame.draw.circle(pantalla, (color_comida[0]//3, color_comida[1]//3, color_comida[2]//3), 
                      centro, radio+2, 2)

def main():
    serpiente = Serpiente()
    comida = generar_comida()
    game_over = False
    puntuacion = 0
    
    while not game_over:
        tiempo = pygame.time.get_ticks()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP and serpiente.direccion != [0, 1]:
                    serpiente.direccion = [0, -1]
                elif evento.key == pygame.K_DOWN and serpiente.direccion != [0, -1]:
                    serpiente.direccion = [0, 1]
                elif evento.key == pygame.K_LEFT and serpiente.direccion != [1, 0]:
                    serpiente.direccion = [-1, 0]
                elif evento.key == pygame.K_RIGHT and serpiente.direccion != [-1, 0]:
                    serpiente.direccion = [1, 0]
        
        serpiente.mover()
        
        if serpiente.posicion == comida:
            SONIDO_COMER.play()
            comida = generar_comida()
            puntuacion += 10
        else:
            serpiente.cuerpo.pop()
            
        if serpiente.colision():
            SONIDO_COLISION.play()
            game_over = True
            
        pantalla.fill(NEGRO)
        dibujar_grid()
        dibujar_comida(comida, tiempo)
        dibujar_serpiente(serpiente.cuerpo)
        
        # Draw scores with glow effect
        fuente = pygame.font.Font(None, 36)
        texto_score = fuente.render(f'Score: {puntuacion}', True, VERDE_NEON)
        sombra_score = fuente.render(f'Score: {puntuacion}', True, (VERDE_NEON[0]//4, VERDE_NEON[1]//4, VERDE_NEON[2]//4))
        pantalla.blit(sombra_score, (12, 12))
        pantalla.blit(texto_score, (10, 10))
            
        pygame.display.update()
        reloj.tick(VELOCIDAD)
    
    # Game Over screen with fade effect
    alpha_surface = pygame.Surface((ANCHO, ALTO))
    alpha_surface.fill((0, 0, 0))
    for alpha in range(0, 128, 2):
        alpha_surface.set_alpha(alpha)
        pantalla.blit(alpha_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(5)

    fuente_grande = pygame.font.Font(None, 72)
    texto_game_over = fuente_grande.render('Game Over!', True, ROJO)
    texto_rect = texto_game_over.get_rect(center=(ANCHO//2, ALTO//2))
    pantalla.blit(texto_game_over, texto_rect)
    
    texto_puntuacion = fuente.render(f'Final Score: {puntuacion}', True, BLANCO)
    texto_puntuacion_rect = texto_puntuacion.get_rect(center=(ANCHO//2, ALTO//2 + 50))
    pantalla.blit(texto_puntuacion, texto_puntuacion_rect)
    
    pygame.display.update()
    pygame.time.wait(2000)
    pygame.quit()

if __name__ == "__main__":
    main()