from engine.asset_packer import SimpleAssetPacker  # noqa: F401
from engine.main_engine import GameEngine 
from scenes.menu import MenuScene


game_engine = GameEngine("nigga", (1000, 800), (255, 255, 6))
scenes = {"menu": MenuScene()}
game_engine.init(scenes)
game_engine.Run_Engine()
