# main.py
import pygame
from engine.personal_debug import P_Debug
from engine.input_manger import InputManager

debugger = P_Debug()

class MenuScene:
    def __init__(self):
        self.inputter = InputManager()

    def handle_events(self, event):
        self.inputter.handle_event(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            print("ESC pressed!")

    def update(self, keys, dt):
        self.inputter.update()
        if self.inputter.is_action_pressed("jump"):
            debugger.add_to_slot(1, "space pressed")

    def draw(self, screen):
        screen.fill((0, 0, 0))

