import pygame

class Victory:
    def __init__(self, screen):
        self.screen = screen

    def run(self):
        self.screen.fill((0, 255, 0))
        font = pygame.font.Font(None, 74)
        text = font.render("¡Victoria!", True, (255, 255, 255))
        self.screen.blit(text, (250, 200))
        pygame.display.flip()
        pygame.time.wait(3000)
