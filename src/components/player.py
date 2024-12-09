import pygame
from config import TILE_SIZE  # Importar el tamaño de los tiles

class Player(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.images = {
            "left": pygame.image.load("src/assets/pantera/izquierda.png").convert_alpha(),
            "right": pygame.image.load("src/assets/pantera/derecha.png").convert_alpha(),
            "up": pygame.image.load("src/assets/pantera/atras.png").convert_alpha(),
            "down": pygame.image.load("src/assets/pantera/frontal.png").convert_alpha(),
            "celebration": [
                pygame.image.load("src/assets/pantera/derecha.png").convert_alpha(),
                pygame.image.load("src/assets/pantera/frontal.png").convert_alpha(),
                pygame.image.load("src/assets/pantera/izquierda.png").convert_alpha(),
                # Agrega más imágenes si es necesario
            ]
        }
        self.direction = "down"
        # Escalar las imágenes al tamaño de TILE_SIZE, excepto las de celebración
        self.images = {key: pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE)) if key != "celebration" else img for key, img in self.images.items()}
        self.celebration_images = [pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE)) for img in self.images["celebration"]]
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect(topleft=(position[0] * TILE_SIZE, position[1] * TILE_SIZE))
        self.is_celebrating = False
        self.celebration_index = 0
        self.celebration_timer = 0

    def move(self, dx, dy, direction):
        self.rect.x += dx * TILE_SIZE
        self.rect.y += dy * TILE_SIZE
        # Actualizar la dirección y la imagen
        self.direction = direction
        self.image = self.images[self.direction]

    def start_celebration(self):
        """Inicia la animación de celebración."""
        self.is_celebrating = True
        self.celebration_index = 0
        self.celebration_timer = pygame.time.get_ticks()

    def update(self):
        """Actualiza el estado del jugador, incluyendo la animación de celebración."""
        if self.is_celebrating:
            current_time = pygame.time.get_ticks()
            if current_time - self.celebration_timer > 200:  # Cambiar de imagen cada 200 ms
                self.celebration_timer = current_time
                self.celebration_index = (self.celebration_index + 1) % len(self.celebration_images)
                self.image = self.celebration_images[self.celebration_index]

    def draw(self, screen):
        """Dibuja el jugador en la pantalla."""
        screen.blit(self.image, self.rect.topleft)