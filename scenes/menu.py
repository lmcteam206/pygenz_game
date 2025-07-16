# main.py
import pygame
from engine.personal_debug import P_Debug
from engine.input_manger import InputManager
from engine.components import GameObject, Transform, Renderer

debugger = P_Debug()

class MenuScene:
    def __init__(self):
        self.player = GameObject("Player")
        self.transform = self.player.add_component(Transform, x=100, y=200, rotation=45)
        self.player.add_component(Renderer, image_path="bg.png")
        self.inputter = InputManager()

    def handle_events(self, event):
        self.inputter.handle_event(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.transform.translate(10, -5)
            self.transform.rotate(15)

    def update(self, keys, dt):
        self.inputter.update()
        if self.inputter.is_action_pressed("jump"):
            debugger.add_to_slot(1,f"pos : {self.transform.get_position()} , forward : {self.transform.get_forward_vector()}")

    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.player.draw(screen)

