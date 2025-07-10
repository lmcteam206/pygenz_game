import pygame
from engine.assest_manger import ResourceManager, resource_path

# === Load Encrypted Assets ===
resources = ResourceManager(
    asset_path=resource_path("assets.dat"),
    encrypted=True,
    key=b"secret_key"  # Must match the one used in encrypt_assets.py
)

class MenuScene:
    def __init__(self):
        self.played = False
        self.bg = resources.get_image("bg.png")

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN and not self.played:
            self.played = True
        print("Handling events")

    def update(self, keys, dt):
        print("Updating with keys", keys)

    def draw(self, screen):
        screen.blit(self.bg, (0, 0))  # actually draw something
