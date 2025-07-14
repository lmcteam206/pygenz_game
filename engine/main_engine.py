
import os
import sys
import pygame
from engine.scene_manger import Scene_Manger



def silent_pygame_init():
    # Save original stdout
    original_stdout = sys.stdout
    sys.stdout = open(os.devnull, "w")  # Redirect stdout to null (no output)

    try:
        pygame.init()
    finally:
        sys.stdout.close()  # Close redirected stdout
        sys.stdout = original_stdout  # Restore original stdout



class GameEngine:
    def __init__(
        self, game_name="none", window_size=(100, 800), defualt_bgcolor=(255, 255, 255)
    ):
        
        
        silent_pygame_init()
        self.game_name = game_name
        self.window_size = window_size
        self.defult_bgcolor = defualt_bgcolor
        self.running = True
        self.scenes = {}

    def init(self, scenes):
        pygame.display.set_caption(self.game_name)
        self.screen = pygame.display.set_mode(self.window_size)
        self.clock = pygame.time.Clock()
        self.Smanger = Scene_Manger(scenes)

    def add_scene(self, name, scene):
        self.scenes[name] = scene

    def add_scenes(self, scenes_dict):
        self.scenes.update(scenes_dict)

    def change_scene(self, name):
        self.Smanger.set_current_scene(name)

    def Set_Window_Name(self, name):
        self.game_name = name
        pygame.display.set_caption(self.game_name)

    def Set_Window_Size(self, size):
        self.screen = pygame.display.set_mode(size)


    def Run_Engine(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            keys = pygame.key.get_pressed()
            self.screen.fill(self.defult_bgcolor)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.Smanger.handle_scenes_events(event)

            self.Smanger.update_scenes(keys, dt)
            self.Smanger.draw_scenes(self.screen)

            pygame.display.flip()
