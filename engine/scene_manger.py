# scene_manager.py
# ==============================
# Scene_Manger handles switching between different game scenes (like Menu, Game, Pause).
# Each scene is expected to implement: handle_events(), update(keys, dt), and draw(screen).

class Scene_Manger:
    def __init__(self, scenes_dict=None):
        if scenes_dict is None:
            scenes_dict = {}

        # Store scenes in a dictionary: { "menu": MenuScene(), "game": GameScene(), ... }
        self.scenes = scenes_dict
        self.current_scene = None

        if scenes_dict:
            # Automatically set the first scene in the dictionary as the starting scene
            first_key = next(iter(scenes_dict))
            self.set_current_scene(first_key)

    def set_current_scene(self, name):
        """
        Switch to a scene by its name.
        Example: manager.set_current_scene("game")
        """
        if name in self.scenes:
            self.current_scene = self.scenes[name]
        else:
            raise ValueError(f"Scene '{name}' not found in manager.")

    def get_current_scene(self):
        """
        Return the currently active scene object.
        """
        return self.current_scene

    def handle_scenes_events(self, event):
        """
        Forward a single event (like a KEYDOWN or MOUSEBUTTONDOWN) to the active scene.
        Called inside your main loop.
        """
        if self.current_scene:
            self.current_scene.handle_events(event)

    def update_scenes(self, keys, dt):
        """
        Call the update() method of the active scene.
        - keys: result of pygame.key.get_pressed()
        - dt: delta time in seconds (for time-based movement)
        """
        if self.current_scene:
            self.current_scene.update(keys=keys, dt=dt)

    def draw_scenes(self, screen):
        """
        Call the draw() method of the active scene to render everything to the screen.
        """
        if self.current_scene:
            self.current_scene.draw(screen)

    def restart_current_scene(self):
        """
        Restart the current scene by re-instantiating it from its original class.
        Useful for restarting levels or resetting game state.
        """
        name = self.current_scene
        scene_class = type(self.scenes[name])
        self.scenes[name] = scene_class()  # Create a new instance of the same class
        self.set_current_scene(name)
