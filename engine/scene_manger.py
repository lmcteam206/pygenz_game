class Scene_Manger:
    def __init__(self, scenes_dict=None):
        if scenes_dict is None:
            scenes_dict = {}
        self.scenes = scenes_dict  # Now a dictionary: {"menu": MenuScene(), ...}
        self.current_scene = None

        if scenes_dict:
            # Set the first scene as default
            first_key = next(iter(scenes_dict))
            self.set_current_scene(first_key)

    def set_current_scene(self, name):
        if name in self.scenes:
            self.current_scene = self.scenes[name]
        else:
            raise ValueError(f"Scene '{name}' not found in manager.")

    def get_current_scene(self):
        return self.current_scene

    def handle_scenes_events(self, event):
        if self.current_scene:
            self.current_scene.handle_events(event)

    def update_scenes(self, keys,dt):
        if self.current_scene:
            self.current_scene.update(keys=keys,dt=dt)

    def draw_scenes(self, screen):
        if self.current_scene:
            self.current_scene.draw(screen)

    def restart_current_scene(self):
        name = self.current_scene
        scene_class = type(self.scenes[name])
        self.scenes[name] = scene_class()  # Recreate
        self.set_current_scene(name)
            
