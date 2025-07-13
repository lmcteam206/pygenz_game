import pygame
from engine.global_resourses import resources

class MenuScene:
    def __init__(self):
        self.played = False
        self.bg = resources.get_image("bg.png")
        print("Assets in pack:")
        for asset_name in resources.list_assets():
            print("-", asset_name)

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN and not self.played:
            self.played = True
        

    def update(self, keys, dt):
        if keys[pygame.K_SPACE]:
            print('hello')

    def draw(self, screen):
        screen.blit(self.bg, (0, 0))  # actually draw something
