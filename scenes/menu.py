import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from engine.data_manger import GameDB


# Load or create
db = GameDB("game.save", encrypt=False)

# Read something
print("Inventory:", db.get("Player", "inventory"))

# Change values
db.set("Player", "hp", 250)
db.set("World", "time", "sunrise")

# Save changes
db.save()
