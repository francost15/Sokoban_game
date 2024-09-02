import pygame
import sys
from map import draw_map
from player import Player
from settings import WIDTH, HEIGHT, BLACK, WHITE, FPS, GRASS_IMAGE  # Importar las constantes de settings.py

class Game:
    def __init__(self, screen, level_file):
        self.screen = screen
        self.player = Player()
        self.map_layout = self.load_level(level_file)
        self.move_history = []
        self.undo_button = pygame.Rect(WIDTH - 100, 10, 80, 30)  # Botón de deshacer en la esquina superior derecha
        self.grass_image = pygame.image.load(GRASS_IMAGE)  # Cargar la imagen de césped
        self.grass_image = pygame.transform.scale(self.grass_image, (WIDTH, HEIGHT))  # Escalar la imagen al tamaño de la ventana

    def load_level(self, filename):
        with open(filename, 'r') as f:
            return [list(line.strip()) for line in f]

    def draw_undo_button(self):
        pygame.draw.rect(self.screen, BLACK, self.undo_button)
        font = pygame.font.SysFont(None, 24)
        text = font.render('Regresar', True, WHITE)
        self.screen.blit(text, (self.undo_button.x + 10, self.undo_button.y + 5))

    def update(self):
        self.screen.blit(self.grass_image, (0, 0))  # Dibujar la imagen de césped escalada
        draw_map(self.map_layout, self.screen)
        self.player.draw(self.screen)
        self.draw_undo_button()

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
                dx, dy = 0, 0
                if event.key == pygame.K_LEFT:
                    dx, dy = -1, 0
                elif event.key == pygame.K_RIGHT:
                    dx, dy = 1, 0
                elif event.key == pygame.K_UP:
                    dx, dy = 0, -1
                elif event.key == pygame.K_DOWN:
                    dx, dy = 0, 1
                self.move(dx, dy)
            elif event.key == pygame.K_u:  # Deshacer último movimiento
                self.undo_move()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.undo_button.collidepoint(event.pos):
                self.undo_move()

    def move(self, dx, dy):
        # Guardar estado actual para el deshacer
        self.move_history.append((self.player.x, self.player.y, [row[:] for row in self.map_layout]))
        
        new_x = self.player.x + dx
        new_y = self.player.y + dy

        # Comprobando si el jugador puede moverse
        if self.map_layout[new_y][new_x] not in ['#', '$', '*']:  # No se puede mover a una pared o caja sin moverla
            self.player.move(dx, dy, self.map_layout)
        elif self.map_layout[new_y][new_x] in ['$', '*']:  # Si hay una caja en la dirección de movimiento
            box_new_x = new_x + dx
            box_new_y = new_y + dy
            if self.map_layout[box_new_y][box_new_x] in [' ', '.']:  # La caja puede ser movida
                # Actualizar la posición del jugador
                self.player.move(dx, dy, self.map_layout)
                # Mover la caja
                if self.map_layout[new_y][new_x] == '$':
                    self.map_layout[new_y][new_x] = ' '  # Eliminar la caja de la posición actual
                else:
                    self.map_layout[new_y][new_x] = '.'  # Si la caja estaba en un agujero, restaurar el agujero
                # Poner la caja en la nueva posición
                if self.map_layout[box_new_y][box_new_x] == '.':
                    self.map_layout[box_new_y][box_new_x] = '*'  # Caja en el agujero
                else:
                    self.map_layout[box_new_y][box_new_x] = '$'  # Caja normal

    def undo_move(self):
        if self.move_history:
            self.player.x, self.player.y, self.map_layout = self.move_history.pop()

    def run(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.handle_events(event)

            self.update()
            pygame.display.flip()
            clock.tick(FPS)