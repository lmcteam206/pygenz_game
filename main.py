import pygame
from engine.scene_manger import Scene_Manger
from scenes.menu import MenuScene

pygame.init()
pygame.display.set_caption("Game")

screen = pygame.display.set_mode((1000, 800))
clock = pygame.time.Clock()

# ✅ Use a dictionary of named scenes
scenes = {
    "menu": MenuScene(),
}

Smanger = Scene_Manger(scenes)

running = True
while running:
    dt = clock.tick(60) / 1000.0  # ✅ delta time in seconds
    keys = pygame.key.get_pressed()
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        Smanger.handle_scenes_events(event)

    Smanger.update_scenes(keys,dt)
    Smanger.draw_scenes(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
