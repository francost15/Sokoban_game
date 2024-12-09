import pygame
from scenes.main_menu import MainMenu
from scenes.game_scene import GameScene
from scenes.level_selection import LevelSelection
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR

def show_final_screen(screen):
    """Muestra una pantalla de finalización cuando se completan todos los niveles."""
    font = pygame.font.SysFont(None, 74)
    text = font.render("¡Has completado todos los niveles!", True, (255, 255, 255))
    screen.fill((0, 0, 0))  # Fondo negro
    screen.blit(text, (
        SCREEN_WIDTH // 2 - text.get_width() // 2,
        SCREEN_HEIGHT // 2 - text.get_height() // 2
    ))
    pygame.display.flip()

    # Mantener el letrero en pantalla hasta que el jugador decida salir
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False  # Salir del bucle y cerrar la ventana
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False  # Salir del bucle si se presiona una tecla o clic del mouse

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Sokoban - UVP")

    # Fondo suave para mejorar la experiencia visual
    background_color = BACKGROUND_COLOR

    # Lista de niveles en orden
    level_paths = [
        # NIVEL I
        "src/levels/level1_1.txt",
        "src/levels/level1_2.txt",
        "src/levels/level1_3.txt",
        # NIVEL II
        "src/levels/level2_1.txt",
        "src/levels/level2_2.txt",
        "src/levels/level2_3.txt",
        # NIVEL III
        "src/levels/level3_1.txt",
        "src/levels/level3_2.txt",
        "src/levels/level3_3.txt"
    ]
    current_level_index = 0
    total_levels = len(level_paths)  # Agregamos esta línea para obtener el total de niveles

    # Escenas
    main_menu = MainMenu(screen)
    level_selection = LevelSelection(screen)
    game_scene = None  # Inicializar
    current_scene = main_menu  # Empieza con el menú

    # Control de tiempo para limitar los FPS
    clock = pygame.time.Clock()
    FPS = 60

    running = True
    while running:
        clock.tick(FPS)  # Limitar a 60 FPS
        screen.fill(background_color)  # Fondo suave para mejorar la experiencia visual

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Manejar eventos en la escena actual
            next_scene_event = current_scene.handle_event(event)

            # Procesar transiciones si se retornó una escena desde handle_event
            if next_scene_event:
                if next_scene_event == "start_game":
                    current_level_index = 0
                    game_scene = GameScene(screen, level_paths, current_level_index, total_levels)
                    current_scene = game_scene
                elif next_scene_event == "level_selection":
                    current_scene = level_selection
                elif next_scene_event == "main_menu":
                    current_scene = main_menu
                elif next_scene_event == "quit":
                    running = False
                elif next_scene_event in ["start_level_1", "start_level_2", "start_level_3"]:
                    level_map = {
                        "start_level_1": 0,
                        "start_level_2": 3,
                        "start_level_3": 6
                    }
                    current_level_index = level_map[next_scene_event]
                    game_scene = GameScene(screen, level_paths, current_level_index, total_levels)
                    current_scene = game_scene

        # Actualizar y renderizar la escena actual
        next_scene = current_scene.run()

        # Procesar transiciones si se retornó una escena desde run
        if next_scene:
            if next_scene == "start_game":
                current_level_index = 0
                game_scene = GameScene(screen, level_paths, current_level_index, total_levels)
                current_scene = game_scene
            elif next_scene == "level_selection":
                current_scene = level_selection
            elif next_scene == "main_menu":
                current_scene = main_menu
            elif next_scene == "next_level":
                current_level_index += 1
                if current_level_index < total_levels:
                    # Verificar si se ha completado el último nivel de un conjunto
                    if current_level_index in [3, 6, 9]:  # Después de level1_3, level2_3, level3_3
                        # Marcar el conjunto de niveles como completado
                        if current_level_index == 3:
                            level_selection.add_solved_level("start_level_1")
                        elif current_level_index == 6:
                            level_selection.add_solved_level("start_level_2")
                        elif current_level_index == 9:
                            level_selection.add_solved_level("start_level_3")
                        current_scene = level_selection
                    else:
                        game_scene = GameScene(screen, level_paths, current_level_index, total_levels)
                        current_scene = game_scene
                    # Marcar el nivel anterior como solucionado
                    solved_level_key = f"start_level_{(current_level_index - 1) // 3 + 1}"
                    level_selection.add_solved_level(solved_level_key)
                else:
                    # Si no hay más niveles, mostrar una pantalla de finalización y salir
                    show_final_screen(screen)
                    running = False
            elif next_scene in ["start_level_1", "start_level_2", "start_level_3"]:
                level_map = {
                    "start_level_1": 0,
                    "start_level_2": 3,
                    "start_level_3": 6
                }
                current_level_index = level_map[next_scene]
                game_scene = GameScene(screen, level_paths, current_level_index, total_levels)
                current_scene = game_scene
            elif next_scene == "quit":
                running = False

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()