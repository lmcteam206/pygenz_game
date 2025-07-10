import pygame
from engine.assest_manger import ResourceManager, resource_path

# === Init pygame ===
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Encrypted Asset Scene")

# === Load Encrypted Assets ===
resources = ResourceManager(
    asset_path=resource_path("assets.dat"),
    encrypted=True,
    key=b"your-secret-key"  # Must match the one used in encrypt_assets.py
)

# === Load assets ===
bg = resources.get_image("backgrounds/menu.png")
font = resources.get_font("fonts/arcade.ttf", 36)
sound = resources.get_sound("sfx/jump.wav")

# === Scene class ===
class Scene:
    def __init__(self):
        self.message = font.render("Encrypted Assets Loaded!", True, (255, 255, 255))
        self.played = False

    def update(self, dt):
        pass

    def draw(self, surface):
        surface.blit(bg, (0, 0))
        surface.blit(self.message, (200, 250))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and not self.played:
            sound.play()
            self.played = True

# === Game loop ===
scene = Scene()
clock = pygame.time.Clock()
running = True

while running:
    dt = clock.tick(60) / 1000  # delta time in seconds
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        scene.handle_event(event)

    scene.update(dt)
    scene.draw(screen)
    pygame.display.flip()

pygame.quit()
