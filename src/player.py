# player.py

import pygame
from settings import TILE_SIZE, ASSET_PATH

class Player:
    def __init__(self):
        self.x = 1
        self.y = 1
        self.image = pygame.image.load(f'{ASSET_PATH}player.gif').convert_alpha()

    def draw(self, screen):
        screen.blit(self.image, (self.x * TILE_SIZE, self.y * TILE_SIZE))

    def move(self, dx, dy, map_layout):
        new_x = self.x + dx
        new_y = self.y + dy

        if map_layout[new_y][new_x] != '#':
            self.x = new_x
            self.y = new_y
