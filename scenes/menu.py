import pygame
from engine.data_manger import GameDB

class Scene:
    def __init__(self):
        self.db = GameDB("game.save", encrypt=False)

        # Initialize only if it's a fresh file
        if self.db.get("Player", "inventory") is None:
            self.db.set("Player", "inventory", ["sword", "potion"])
            self.db.set("Player", "hp", 100)
            self.db.save()

        self.font = pygame.font.SysFont("consolas", 24)
        self.message = "Press S to save, A to add item, D to damage player"

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                self.db.save()
                self.message = "Saved!"

            elif event.key == pygame.K_a:
                inv = self.db.get("Player", "inventory", [])
                inv.append("item_" + str(len(inv) + 1))
                self.db.set("Player", "inventory", inv)
                self.message = f"Added item_{len(inv)}"

            elif event.key == pygame.K_d:
                hp = self.db.get("Player", "hp", 100)
                hp = max(hp - 10, 0)
                self.db.set("Player", "hp", hp)
                self.message = "Took damage!"

    def update(self, keys, dt):
        pass  # Add animation logic if needed

    def draw(self, screen):
        screen.fill((25, 25, 30))
        y = 40

        inventory = self.db.get("Player", "inventory", [])
        hp = self.db.get("Player", "hp", 0)

        screen.blit(self.font.render("Inventory:", True, (255, 255, 255)), (20, y))
        y += 30
        for item in inventory:
            screen.blit(self.font.render(f"- {item}", True, (180, 220, 255)), (40, y))
            y += 25

        screen.blit(self.font.render(f"HP: {hp}", True, (255, 150, 150)), (20, y + 20))
        screen.blit(self.font.render(self.message, True, (100, 255, 100)), (20, y + 60))
