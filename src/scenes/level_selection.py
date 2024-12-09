import pygame

class LevelSelection:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 74)
        self.small_font = pygame.font.SysFont(None, 36)
        self.running = True
        self.next_scene = None
        self.solved_levels = set()  # Conjunto para almacenar los niveles solucionados

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.next_scene = "quit"
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.next_scene = "start_level_1"
            elif event.key == pygame.K_2:
                self.next_scene = "start_level_2"
            elif event.key == pygame.K_3:
                self.next_scene = "start_level_3"

    def run(self):
        self.screen.fill((30, 30, 30))  # Fondo oscuro
        title = self.font.render("Selecciona un Nivel", True, (255, 255, 255))
        self.screen.blit(title, (150, 50))

        # Dibujar botones de niveles
        self.create_level_button("1. Nivel 1", 200, 200, "start_level_1")
        self.create_level_button("2. Nivel 2", 200, 300, "start_level_2")
        self.create_level_button("3. Nivel 3", 200, 400, "start_level_3")

        if self.next_scene:
            temp_scene = self.next_scene
            self.next_scene = None  # Reset after reading
            return temp_scene

        return None

    def create_level_button(self, text, x, y, level_key):
        button_rect = pygame.Rect(x - 10, y - 10, 300, 50)
        shadow_rect = button_rect.copy()
        shadow_rect.topleft = (button_rect.x + 5, button_rect.y + 5)
        
        # Dibujar sombra
        pygame.draw.rect(self.screen, (0, 0, 0), shadow_rect, border_radius=10)
        
        # Dibujar botón
        pygame.draw.rect(self.screen, (70, 130, 180), button_rect, border_radius=10)
        pygame.draw.rect(self.screen, (255, 255, 255), button_rect.inflate(-4, -4), border_radius=10)
        
        # Dibujar texto del nivel
        level_text = self.small_font.render(text, True, (0, 0, 0))
        self.screen.blit(level_text, (x + 10, y + 10))
        
        # Dibujar marca de nivel completado
        if level_key in self.solved_levels:
            solved_text = self.small_font.render("Completado", True, (0, 255, 0))
            self.screen.blit(solved_text, (x + 200, y + 10))

    def add_solved_level(self, level_key):
        self.solved_levels.add(level_key)