# map.py

import pygame
from settings import *

def draw_map(game_map, screen):
    wall_image = pygame.image.load(f'{ASSET_PATH}wall.gif').convert_alpha()
    crate_image = pygame.image.load(f'{ASSET_PATH}crate.gif').convert_alpha()
    hole_image = pygame.image.load(f'{ASSET_PATH}hole.gif').convert_alpha()
    crate_in_hole_image = pygame.image.load(f'{ASSET_PATH}crate-in-hole.gif').convert_alpha()

    for y, row in enumerate(game_map):
        for x, char in enumerate(row):
            pos = (x * TILE_SIZE, y * TILE_SIZE)
            if char == '#':
                screen.blit(wall_image, pos)
            elif char == '$':
                screen.blit(crate_image, pos)
            elif char == '.':
                screen.blit(hole_image, pos)
            elif char == '*':
                screen.blit(crate_in_hole_image, pos)
