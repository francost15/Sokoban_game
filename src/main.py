import pygame
import sys
from settings import *
from game import Game
from button import Button

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Sokoban Game")
    clock = pygame.time.Clock()

    font = pygame.font.Font(None, FONT_SIZE)

    # Cargar la imagen de fondo
    background = pygame.image.load(BACKGROUND_IMAGE)

    # Level selection menu
    def start_game(level_file):
        game = Game(screen, level_file)
        game.run()

    def show_menu():
        buttons = []
        for i in range(1, 5):
            button = Button(
                x=WINDOW_WIDTH // 2 - 100,
                y=200 + i * 50,  # Ajustar la posición para dejar espacio para el título
                width=200,
                height=40,
                text=f"Level {i}",
                font=font,
                color=WHITE,
                hover_color=PURPLE,
                hover_text_color=WHITE,
                action=lambda lvl=i: start_game(f"{LEVEL_PATH}level{lvl}.txt")
            )
            buttons.append(button)

        # Renderizar el título
        title_font = pygame.font.Font(None, 48)  # Fuente más grande para el título
        title = title_font.render("Sokoban Game", True, WHITE)

        while True:
            screen.blit(background, (0, 0))  # Dibujar la imagen de fondo
            screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 100))  # Dibujar el título

            for button in buttons:
                button.draw(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                for button in buttons:
                    button.is_clicked(event)

            pygame.display.flip()
            clock.tick(FPS)

    show_menu()

if __name__ == "__main__":
    main()