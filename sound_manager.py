import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()  # Initialize the mixer
        self.sounds = {}  # Dictionary to store sounds by name

    def load_sound(self, sound_name, file_path):
        """Loads a sound into the sound manager."""
        self.sounds[sound_name] = pygame.mixer.Sound(file_path)

    def play_sound(self, sound_name):
        """Plays the given sound by its name."""
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
        else:
            print(f"Sound '{sound_name}' not found!")

    def stop_all_sounds(self):
        """Stop all currently playing sounds."""
        pygame.mixer.stop()

    def load_music(self, file_path):
        """Loads a music track."""
        pygame.mixer.music.load(file_path)

    def play_music(self, loops=-1, start=0.0):
        """Plays background music."""
        pygame.mixer.music.play(loops, start)

    def stop_music(self):
        """Stops the background music."""
        pygame.mixer.music.stop()
