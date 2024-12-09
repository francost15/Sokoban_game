# src/utils/sound_manager.py
import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.background_music = pygame.mixer.Sound("assets/sounds/background.mp3")
        self.drag_sound = pygame.mixer.Sound("assets/sounds/drag.mp3")
        self.victory_sound = pygame.mixer.Sound("assets/sounds/victory.mp3")
        self.sound_enabled = True

    def play_background(self):
        if self.sound_enabled:
            self.background_music.play(loops=-1)

    def play_drag(self):
        if self.sound_enabled:
            self.drag_sound.play()

    def play_victory(self):
        if self.sound_enabled:
            self.victory_sound.play()

    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        if not self.sound_enabled:
            pygame.mixer.stop()
