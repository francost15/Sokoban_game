import pygame
from config import TILE_SIZE  # Importar el tamaño de los tiles desde config.py

class Map:
    def __init__(self, level_data):
        self.level_data = level_data
        # Cargar las imágenes de los tiles
        self.tiles = {
            "#": pygame.transform.scale(pygame.image.load("src/assets/images/wall.gif"), (TILE_SIZE, TILE_SIZE)),
            " ": pygame.transform.scale(pygame.image.load("src/assets/images/grass.jpg"), (TILE_SIZE, TILE_SIZE)),
            ".": pygame.transform.scale(pygame.image.load("src/assets/images/hole.png"), (TILE_SIZE, TILE_SIZE)),
            "$": pygame.transform.scale(pygame.image.load("src/assets/images/crate-in-hole.png"), (TILE_SIZE, TILE_SIZE)),
            "*": pygame.transform.scale(pygame.image.load("src/assets/images/crate.png"), (TILE_SIZE, TILE_SIZE)),
        }

    def draw(self, screen):
        for y, row in enumerate(self.level_data):
            for x, tile in enumerate(row):
                # Dibuja cada tipo de tile
                if tile in self.tiles:
                    screen.blit(self.tiles[tile], (x * TILE_SIZE, y * TILE_SIZE))
                elif tile == "P":  # Dibujar el camino de la solución en morado
                    pygame.draw.rect(screen, (128, 0, 128), (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                else:
                    # Tile desconocido, usar el piso por defecto
                    screen.blit(self.tiles[" "], (x * TILE_SIZE, y * TILE_SIZE))