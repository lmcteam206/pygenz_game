import pygame
import os

class SoundManager:
    def __init__(self, sound_folder="assets/"):
        pygame.mixer.init()
        self.sound_folder = sound_folder
        self.sounds = {}
        self.music_volume = 1.0
        self.sfx_volume = 1.0
        self.muted = False

    def load(self, name, filename):
        path = os.path.join(self.sound_folder, filename)
        self.sounds[name] = pygame.mixer.Sound(path)
        self.sounds[name].set_volume(self.sfx_volume)

    def play(self, name):
        if not self.muted and name in self.sounds:
            self.sounds[name].play()

    def play_music(self, filename, loop=True):
        path = os.path.join(self.sound_folder, filename)
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(self.music_volume if not self.muted else 0)
        pygame.mixer.music.play(-1 if loop else 0)

    def stop_music(self):
        pygame.mixer.music.stop()

    def set_volume(self, sfx=None, music=None):
        if sfx is not None:
            self.sfx_volume = sfx
            for sound in self.sounds.values():
                sound.set_volume(sfx if not self.muted else 0)
        if music is not None:
            self.music_volume = music
            pygame.mixer.music.set_volume(music if not self.muted else 0)

    def mute(self):
        self.muted = True
        pygame.mixer.music.set_volume(0)
        for sound in self.sounds.values():
            sound.set_volume(0)

    def unmute(self):
        self.muted = False
        pygame.mixer.music.set_volume(self.music_volume)
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume)
