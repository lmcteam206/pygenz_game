# resource_loader.py
import os
import io
import zipfile
import pygame
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from hashlib import sha256
import sys


class ResourceManager:
    def __init__(self, asset_path="assets", encrypted=False, key=None):
        self.image_cache = {}
        self.sound_cache = {}
        self.font_cache = {}

        self.zip = None
        if encrypted:
            if key is None:
                raise ValueError("Encryption key must not be None")
            key = sha256(key).digest()
            with open(asset_path, "rb") as f:
                data = f.read()
            iv = data[:16]
            cipher = AES.new(key, AES.MODE_CBC, iv)
            decrypted = unpad(cipher.decrypt(data[16:]), AES.block_size)
            self.zip = zipfile.ZipFile(io.BytesIO(decrypted), "r")
        elif asset_path.endswith(".zip"):
            self.zip = zipfile.ZipFile(asset_path, "r")
        else:
            self.asset_path = asset_path  # Raw folder

    def _load_file(self, path):
        path = path.replace("\\", "/")
        if self.zip:
            with self.zip.open(path) as f:
                return f.read()
        else:
            with open(os.path.join(self.asset_path, path), "rb") as f:
                return f.read()

    def get_image(self, path, convert_alpha=True):
        if path in self.image_cache:
            return self.image_cache[path]
        data = self._load_file(path)
        image = pygame.image.load(io.BytesIO(data)) if self.zip else pygame.image.load(os.path.join(self.asset_path, path))
        image = image.convert_alpha() if convert_alpha else image.convert()
        self.image_cache[path] = image
        return image

    def get_sound(self, path):
        if path in self.sound_cache:
            return self.sound_cache[path]
        data = self._load_file(path)
        sound = pygame.mixer.Sound(file=io.BytesIO(data)) if self.zip else pygame.mixer.Sound(os.path.join(self.asset_path, path))
        self.sound_cache[path] = sound
        return sound

    def get_font(self, path, size):
        key = f"{path}:{size}"
        if key in self.font_cache:
            return self.font_cache[key]
        data = self._load_file(path)
        font = pygame.font.Font(io.BytesIO(data), size) if self.zip else pygame.font.Font(os.path.join(self.asset_path, path), size)
        self.font_cache[key] = font
        return font

def resource_path(relative_path: str) -> str:
    """
    Get absolute path to resource, works for dev and PyInstaller builds.
    
    When using PyInstaller with --onefile, all files are unpacked to a
    temporary folder and stored in _MEIPASS. This function detects that.
    """
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)
