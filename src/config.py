# Configuración de pantalla
SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 800

# Tamaño del mapa (en tiles)
MAP_WIDTH = 25
MAP_HEIGHT = 18

# Tamaño de cada tile (calculado en función del tamaño de la pantalla y el tamaño del mapa)
TILE_SIZE = min(SCREEN_WIDTH // MAP_WIDTH, SCREEN_HEIGHT // MAP_HEIGHT)

# Color de fondo en formato RGB
BACKGROUND_COLOR = (255, 255, 255)  # Blanco