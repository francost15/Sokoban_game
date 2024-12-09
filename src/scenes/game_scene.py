import sys
import os
import pygame
import time

# Agregar la ruta superior para importar módulos correctamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from solvers.astar_solver import AStarSolver
from components.player import Player
from components.map import Map
from config import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, BACKGROUND_COLOR

class GameScene:
    def __init__(self, screen, level_paths, current_level_index, total_levels):
        self.screen = screen
        self.level_paths = level_paths
        self.current_level_index = current_level_index
        self.total_levels = total_levels  # Total de niveles en el juego
        self.level_file = self.level_paths[self.current_level_index]
        
        # Cargar el nivel actual
        self.map_layout = self.load_level(self.level_file)
        self.initial_map_layout = [row.copy() for row in self.map_layout]
        self.map = Map(self.map_layout)
        self.player = Player(self.get_player_start_position())
        self.move_history = []
        self.moves = 0
        self.won = False
        self.start_time = time.time()  # Tiempo de inicio del nivel

        # Variables para controlar el tiempo de espera al completar el nivel
        self.level_completed_time = None  # Tiempo en que se completó el nivel
        self.wait_time_after_win = 10  # Segundos a esperar antes de avanzar al siguiente nivel

        # Cargar imágenes y fuentes
        self.steps_image = pygame.image.load("src/assets/images/pasos.png").convert_alpha()
        self.steps_image = pygame.transform.scale(self.steps_image, (60, 60))  # Ajustar tamaño
        self.clock_image = pygame.image.load("src/assets/images/reloj.png").convert_alpha()
        self.clock_image = pygame.transform.scale(self.clock_image, (50, 60))  # Ajustar tamaño
        self.solve_image = pygame.image.load("src/assets/images/resolver.png").convert_alpha()
        self.solve_image = pygame.transform.scale(self.solve_image, (80, 60))  # Ajustar tamaño
        self.sound_image = pygame.image.load("src/assets/images/sonido.png").convert_alpha()
        self.sound_image = pygame.transform.scale(self.sound_image, (80, 60))  # Ajustar tamaño
        self.undo_image = pygame.image.load("src/assets/images/regresar.png").convert_alpha()
        self.undo_image = pygame.transform.scale(self.undo_image, (80, 60))  # Ajustar tamaño
        self.restart_image = pygame.image.load("src/assets/images/reiniciar.png").convert_alpha()
        self.restart_image = pygame.transform.scale(self.restart_image, (80, 60))  # Ajustar tamaño

        # Fuentes y colores
        self.font = pygame.font.SysFont("Arial", 24)
        self.large_font = pygame.font.SysFont("Arial", 74)
        self.ui_color = (255, 255, 255)

        # Botones (usar dimensiones de las imágenes)
        self.undo_button = pygame.Rect(SCREEN_WIDTH - 100, 10, self.undo_image.get_width(), self.undo_image.get_height())
        self.restart_button = pygame.Rect(SCREEN_WIDTH - 200, 10, self.restart_image.get_width(), self.restart_image.get_height())
        self.sound_button = pygame.Rect(SCREEN_WIDTH - 300, 10, self.sound_image.get_width(), self.sound_image.get_height())
        self.solve_button = pygame.Rect(SCREEN_WIDTH - 400, 10, self.solve_image.get_width(), self.solve_image.get_height())
        
        # Sonidos
        self.move_sound = pygame.mixer.Sound("src/assets/sounds/drag.mp3")
        self.push_sound = pygame.mixer.Sound("src/assets/sounds/drag.mp3")
        self.win_sound = pygame.mixer.Sound("src/assets/sounds/victory.mp3")
        self.click_sound = pygame.mixer.Sound("src/assets/sounds/drag.mp3")
        self.background_music = "src/assets/sounds/background.mp3"
        pygame.mixer.music.load(self.background_music)
        pygame.mixer.music.play(-1)
        
        # Variables para el solucionador A*
        self.is_solving = False
        self.solution_step = 0
        self.solution_path = []
        self.move_delay = 500  # Milisegundos entre movimientos
        self.last_move_time = pygame.time.get_ticks()
        
        # Control de sonido
        self.sound_enabled = True

    def load_level(self, filename):
        """Cargar el mapa desde un archivo."""
        with open(filename, 'r') as f:
            return [list(line.rstrip('\n')) for line in f]

    def get_player_start_position(self):
        """Encontrar la posición inicial del jugador en el mapa."""
        for y, row in enumerate(self.map_layout):
            for x, tile in enumerate(row):
                if tile == '@':
                    return (x, y)
        return (1, 1)  # Posición por defecto si no se encuentra

    def restart_level(self):
        """Restablecer el nivel al estado inicial."""
        self.map_layout = [row.copy() for row in self.initial_map_layout]
        self.map = Map(self.map_layout)
        self.player.rect.topleft = (self.get_player_start_position()[0] * TILE_SIZE, 
                                     self.get_player_start_position()[1] * TILE_SIZE)
        self.move_history.clear()
        self.moves = 0
        self.won = False
        self.is_solving = False
        self.solution_step = 0
        self.solution_path = []
        self.start_time = time.time()  # Resetear tiempo de inicio
        if self.sound_enabled:
            self.click_sound.play()

    def draw_buttons(self):
        """Dibuja los botones en la pantalla con animación de resaltado."""
        mouse_pos = pygame.mouse.get_pos()

        for button, image in [(self.undo_button, self.undo_image),
                              (self.restart_button, self.restart_image),
                              (self.sound_button, self.sound_image),
                              (self.solve_button, self.solve_image)]:
            self.screen.blit(image, (button.x, button.y))

    def solve_level(self):
        """Resuelve el nivel usando A*."""
        solver = AStarSolver(self.map_layout, (self.player.rect.x // TILE_SIZE, self.player.rect.y // TILE_SIZE))
        self.solution_path = solver.solve()
        if self.solution_path:
            self.is_solving = True
            self.solution_step = 0
            self.last_move_time = pygame.time.get_ticks()
            if self.sound_enabled:
                self.click_sound.play()

    def display_status(self):
        """Muestra información del juego."""
        elapsed_time = int(time.time() - self.start_time)
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60

        moves_text = self.font.render(f": {self.moves}", True, self.ui_color)
        time_text = self.font.render(f"{minutes:02}:{seconds:02}", True, self.ui_color)

        # Dibujar la imagen de pasos y el contador de movimientos
        self.screen.blit(self.steps_image, (SCREEN_WIDTH - self.steps_image.get_width() - 55, 130))
        self.screen.blit(moves_text, (SCREEN_WIDTH - moves_text.get_width() - 40, 150))

        # Dibujar la imagen del reloj y el tiempo
        self.screen.blit(self.clock_image, (SCREEN_WIDTH - self.clock_image.get_width() - 55, 190))
        self.screen.blit(time_text, (SCREEN_WIDTH - time_text.get_width() - 10, 210))

    def check_win(self):
        """Verifica si el jugador ha ganado."""
        for row in self.map_layout:
            if '$' in row:
                return False
        return True

    def handle_event(self, event):
        """Maneja los eventos del juego."""
        if not self.won and not self.is_solving:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.move(-1, 0, "left")
                elif event.key == pygame.K_RIGHT:
                    self.move(1, 0, "right")
                elif event.key == pygame.K_UP:
                    self.move(0, -1, "up")
                elif event.key == pygame.K_DOWN:
                    self.move(0, 1, "down")
                elif event.key == pygame.K_u:
                    self.undo_move()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botón izquierdo del mouse
                    if self.undo_button.collidepoint(event.pos):
                        self.undo_move()
                        if self.sound_enabled:
                            self.click_sound.play()
                    elif self.restart_button.collidepoint(event.pos):
                        self.restart_level()
                    elif self.sound_button.collidepoint(event.pos):
                        self.toggle_sound()
                        if self.sound_enabled:
                            self.click_sound.play()
                    elif self.solve_button.collidepoint(event.pos):
                        self.solve_level()
        else:
            # Si el nivel está completado, no hacemos nada aquí
            pass

    def move(self, dx, dy, direction):
        """Mueve al jugador y las cajas si es necesario."""
        # Guardar estado antes de mover
        self.move_history.append((self.player.rect.topleft, [row.copy() for row in self.map_layout]))

        # Calcular nueva posición del jugador
        new_x = (self.player.rect.x + dx * TILE_SIZE) // TILE_SIZE
        new_y = (self.player.rect.y + dy * TILE_SIZE) // TILE_SIZE

        # Verificar si la nueva posición está libre o es un objetivo
        if self.map_layout[new_y][new_x] == ' ' or self.map_layout[new_y][new_x] == '.':
            self.player.move(dx, dy, direction)
            self.moves += 1
            if self.sound_enabled:
                self.move_sound.play()

        elif self.map_layout[new_y][new_x] in ('$','*'):  # Si hay una caja
            next_x = new_x + dx
            next_y = new_y + dy
            if self.map_layout[next_y][next_x] in (' ', '.'):
                # Mover caja
                if self.map_layout[next_y][next_x] == '.':
                    self.map_layout[next_y][next_x] = '*'
                else:
                    self.map_layout[next_y][next_x] = '$'
                if self.map_layout[new_y][new_x] == '*':
                    self.map_layout[new_y][new_x] = '.'
                else:
                    self.map_layout[new_y][new_x] = ' '
                self.player.move(dx, dy, direction)
                if self.sound_enabled:
                    self.push_sound.play()
                self.moves += 1

    def undo_move(self):
        """Deshace el último movimiento."""
        if self.move_history:
            last_position, last_map = self.move_history.pop()
            self.player.rect.topleft = last_position
            self.map_layout = last_map
            self.moves -= 1
            self.map = Map(self.map_layout)  # Actualizar mapa

    def toggle_sound(self):
        """Activa o desactiva el sonido."""
        self.sound_enabled = not self.sound_enabled
        if self.sound_enabled:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()

    def run(self):
        """Actualiza y dibuja el estado del juego, y retorna señales para cambiar de escena si es necesario."""
        # Actualizar el estado del juego
        next_scene = self.update()

        # Retornar cualquier señal para cambiar de escena
        return next_scene

    def update(self):
        """Actualiza la visualización y acciones del juego."""
        # Dibujar fondo negro
        self.screen.fill((0, 0, 0))

        # Dibujar mapa
        self.map.draw(self.screen)

        # Movimiento lento si está resolviendo
        if self.is_solving:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_move_time > self.move_delay:
                if self.solution_step < len(self.solution_path):
                    dx, dy = self.solution_path[self.solution_step]
                    if dx == -1:
                        direction = "left"
                    elif dx == 1:
                        direction = "right"
                    elif dy == -1:
                        direction = "up"
                    elif dy == 1:
                        direction = "down"
                    else:
                        direction = "down"
                    self.move(dx, dy, direction)
                    self.solution_step += 1
                    self.last_move_time = current_time
                else:
                    self.is_solving = False  # Terminó de resolver

        # Verificar condición de victoria
        if self.check_win():
            if not self.won:
                if self.sound_enabled:
                    pygame.mixer.music.stop()
                    self.win_sound.play()
                self.won = True
                self.player.start_celebration()
                self.level_completed_time = time.time()  # Registrar tiempo de finalización
            else:
                self.player.update()  # Actualizar animación de celebración
            # Mostrar mensaje de "¡Nivel Completado!"
            self.show_completed_message()
            # Verificar si han pasado 10 segundos desde que se completó el nivel
            if time.time() - self.level_completed_time >= self.wait_time_after_win:
                return "next_level"
        else:
            self.player.update()  # Actualizar animación del jugador

        # Dibujar jugador y estado
        self.player.draw(self.screen)
        self.display_status()
        self.draw_buttons()

        return None

    def show_completed_message(self):
        """Muestra un mensaje de completado en la pantalla."""
        text = self.large_font.render("¡Nivel Completado!", True, (255, 215, 0))
        # Dibujar el texto centrado en la pantalla
        self.screen.blit(text, (
            SCREEN_WIDTH // 2 - text.get_width() // 2, 
            SCREEN_HEIGHT // 2 - text.get_height() // 2 - 50
        ))