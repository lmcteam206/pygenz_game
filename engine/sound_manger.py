# sound_manager.py
# =================================
# A simple and reusable sound system for playing sound effects and music using Pygame.
# - Centralizes all audio control (play, volume, mute, etc.)
# - Prevents loading the same sound file multiple times
# - Supports music and SFX separately

import pygame
import os


class SoundManager:
    def __init__(self, sound_folder="assets/"):
        """
        Initialize the SoundManager.
        - sound_folder: where all your audio files (wav, mp3) are stored
        """
        pygame.mixer.init()
        self.sound_folder = sound_folder  # Base folder to load sounds/music from
        self.sounds = {}  # Dictionary to store sound effects by name
        self.music_volume = 1.0  # Volume for background music (0.0 to 1.0)
        self.sfx_volume = 1.0  # Volume for sound effects (0.0 to 1.0)
        self.muted = False  # Global mute toggle

    def load(self, name, filename):
        """
        Load a sound effect file into memory.
        - name: key used to reference this sound later (e.g. "jump")
        - filename: actual file in the folder (e.g. "jump.wav")
        """
        path = os.path.join(self.sound_folder, filename)
        self.sounds[name] = pygame.mixer.Sound(path)
        self.sounds[name].set_volume(self.sfx_volume)

    def play(self, name):
        """
        Play a loaded sound effect by its name.
        Will do nothing if muted or the sound isn't found.
        """
        if not self.muted and name in self.sounds:
            self.sounds[name].play()

    def play_music(self, filename, loop=True):
        """
        Play background music.
        - filename: audio file in the folder (e.g. "bg_music.mp3")
        - loop: whether to loop the music (default is True)
        """
        path = os.path.join(self.sound_folder, filename)
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(self.music_volume if not self.muted else 0)
        pygame.mixer.music.play(-1 if loop else 0)

    def stop_music(self):
        """
        Stop any currently playing background music.
        """
        pygame.mixer.music.stop()

    def set_volume(self, sfx=None, music=None):
        """
        Adjust the volume levels.
        - sfx: volume for sound effects (0.0 to 1.0)
        - music: volume for background music (0.0 to 1.0)
        """
        if sfx is not None:
            self.sfx_volume = sfx
            for sound in self.sounds.values():
                sound.set_volume(sfx if not self.muted else 0)

        if music is not None:
            self.music_volume = music
            pygame.mixer.music.set_volume(music if not self.muted else 0)

    def mute(self):
        """
        Mute all sounds and music.
        """
        self.muted = True
        pygame.mixer.music.set_volume(0)
        for sound in self.sounds.values():
            sound.set_volume(0)

    def unmute(self):
        """
        Unmute all sounds and restore previous volume levels.
        """
        self.muted = False
        pygame.mixer.music.set_volume(self.music_volume)
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume)
