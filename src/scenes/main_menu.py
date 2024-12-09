import pygame

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 74)
        self.small_font = pygame.font.SysFont(None, 36)
        self.running = True
        self.next_scene = None

        # Cargar la imagen de fondo
        self.background_image = pygame.image.load("src/assets/images/menusokoban.jpg")
        self.background_image = pygame.transform.scale(self.background_image, (self.screen.get_width(), self.screen.get_height()))


        # Cargar la imagen del botón de "Play"
        self.play_button_image = pygame.image.load("src/assets/images/play.png")
        self.play_button_image = pygame.transform.scale(self.play_button_image, (300, 150))
        self.play_button_rect = self.play_button_image.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 100))

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.next_scene = "level_selection"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_button_rect.collidepoint(event.pos):
                self.next_scene = "level_selection"

    def run(self):
        self.screen.blit(self.background_image, (0, 0))

        # Dibujar el botón de "Play"
        self.screen.blit(self.play_button_image, self.play_button_rect.topleft)

        return self.next_scene