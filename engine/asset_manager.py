import struct
import io
import pygame
from engine.utils import resource_path


class SimpleAssetManager:
    def __init__(self, pack_file, key: bytes = b"\x42", encrypted=False):
        self.encrypted = encrypted
        self.key = key
        self.assets = {}
        self.image_cache = {}
        self._load_pack(resource_path(pack_file))

    def _load_pack(self, path):
        with open(path, "rb") as f:
            count = struct.unpack("<I", f.read(4))[0]
            entries = []
            for _ in range(count):
                name_len = struct.unpack("<H", f.read(2))[0]
                name = f.read(name_len).decode("utf-8")
                offset, size = struct.unpack("<II", f.read(8))
                entries.append((name, offset, size))
            blob = f.read()

        for name, offset, size in entries:
            raw = blob[offset : offset + size]
            if self.encrypted:
                raw = self._xor(raw)
            self.assets[name] = raw

    def get_raw(self, name):
        raw = self.assets.get(name)
        if raw is None:
            raise FileNotFoundError(f"Asset '{name}' not found in pack file.")
        return raw

    def get_image(self, name: str) -> pygame.Surface:
        if name in self.image_cache:
            return self.image_cache[name]

        raw = self.get_raw(name)
        surface = pygame.image.load(io.BytesIO(raw))

        try:
            surface = surface.convert_alpha()
        except pygame.error:
            # Display not initialized, skip conversion
            pass

        self.image_cache[name] = surface
        return surface

    def get_sound(self, name):
        raw = self.get_raw(name)
        return pygame.mixer.Sound(io.BytesIO(raw))

    def get_font(self, name, size):
        raw = self.get_raw(name)
        return pygame.font.Font(io.BytesIO(raw), size)

    def _xor(self, data: bytes) -> bytes:
        return bytes(b ^ self.key[i % len(self.key)] for i, b in enumerate(data))

    def list_assets(self):
        """
        Returns a list of all asset names in the pack file.
        """
        return list(self.assets.keys())
