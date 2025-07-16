
class Component:
    def __init__(self, game_object):
        self.game_object = game_object

    def start(self):
        pass

    def update(self, dt):
        pass

    def draw(self, screen):
        pass


class GameObject:
    def __init__(self, name="GameObject"):
        self.name = name
        self.components = []

    def add_component(self, component_cls, *args, **kwargs):
        comp = component_cls(self, *args, **kwargs)
        self.components.append(comp)
        return comp

    def get_component(self, component_cls):
        for comp in self.components:
            if isinstance(comp, component_cls):
                return comp
        return None

    def start(self):
        for comp in self.components:
            comp.start()

    def update(self, dt):
        for comp in self.components:
            comp.update(dt)

    def draw(self, screen):
        for comp in self.components:
            if hasattr(comp, "draw"):
                comp.draw(screen)
