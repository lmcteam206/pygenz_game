import pygame


class InputManager:
    def __init__(self):
        pygame.joystick.init()

        # Connect and store all joysticks
        self.joysticks = [
            pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())
        ]

        # Action bindings can now target specific joysticks by ID
        self.bindings = {
            "move_up": [pygame.K_w, pygame.K_UP, ("joy_axis", 0, 1, -1)],
            "move_down": [pygame.K_s, pygame.K_DOWN, ("joy_axis", 0, 1, 1)],
            "move_left": [pygame.K_a, pygame.K_LEFT, ("joy_axis", 0, 0, -1)],
            "move_right": [pygame.K_d, pygame.K_RIGHT, ("joy_axis", 0, 0, 1)],
            "jump": [pygame.K_SPACE, ("mouse", 1), ("joy_button", 0, 0)],
            "dash": [pygame.K_LSHIFT, ("joy_button", 0, 1)],
            "attack": [pygame.K_j, ("mouse", 1), ("joy_button", 0, 2)],
            "interact": [pygame.K_e, ("joy_button", 0, 3)],
            "use_item": [pygame.K_f, ("mouse", 3)],
            "pause": [pygame.K_ESCAPE, ("joy_button", 0, 7)],
            "inventory": [pygame.K_i],
            "map": [pygame.K_m],
            "menu_up": [pygame.K_UP],
            "menu_down": [pygame.K_DOWN],
            "menu_select": [pygame.K_RETURN, ("mouse", 1)],
            "super_move": [[pygame.K_LEFT, pygame.K_LCTRL]],
        }

        # Input state
        self._keys_down = set()
        self._keys_pressed = set()
        self._mouse_buttons_down = set()
        self._mouse_buttons_pressed = set()
        self._joy_buttons_down = {}  # {joy_id: set()}
        self._joy_buttons_pressed = {}

        # Init button state for each joystick
        for joy in self.joysticks:
            self._joy_buttons_down[joy.get_id()] = set()
            self._joy_buttons_pressed[joy.get_id()] = set()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            self._keys_down.add(event.key)
            self._keys_pressed.add(event.key)
        elif event.type == pygame.KEYUP:
            self._keys_down.discard(event.key)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            self._mouse_buttons_down.add(event.button)
            self._mouse_buttons_pressed.add(event.button)
        elif event.type == pygame.MOUSEBUTTONUP:
            self._mouse_buttons_down.discard(event.button)

        elif event.type == pygame.JOYBUTTONDOWN:
            jid = event.joy
            self._joy_buttons_down[jid].add(event.button)
            self._joy_buttons_pressed[jid].add(event.button)
        elif event.type == pygame.JOYBUTTONUP:
            jid = event.joy
            self._joy_buttons_down[jid].discard(event.button)

    def update(self):
        self._keys_pressed.clear()
        self._mouse_buttons_pressed.clear()
        for jid in self._joy_buttons_pressed:
            self._joy_buttons_pressed[jid].clear()

    def is_action_pressed(self, action):
        for binding in self.bindings.get(action, []):
            if self._check_pressed(binding):
                return True
        return False

    def just_pressed(self, action):
        for binding in self.bindings.get(action, []):
            if self._check_just_pressed(binding):
                return True
        return False

    def _check_pressed(self, binding):
        if isinstance(binding, int):  # Keyboard key
            return binding in self._keys_down
        elif isinstance(binding, tuple):
            kind = binding[0]
            if kind == "mouse":
                return binding[1] in self._mouse_buttons_down
            elif kind == "joy_button":
                # Format: ("joy_button", joy_id, button_index)
                joy_id, btn = binding[1], binding[2]
                return btn in self._joy_buttons_down.get(joy_id, set())
            elif kind == "joy_axis":
                # Format: ("joy_axis", joy_id, axis_index, direction)
                joy_id, axis, direction = binding[1], binding[2], binding[3]
                if joy_id >= len(self.joysticks):
                    return False
                val = self.joysticks[joy_id].get_axis(axis)
                return val < -0.5 if direction < 0 else val > 0.5
        elif isinstance(binding, list):  # Combo binding
            return all(self._check_pressed(part) for part in binding)
        return False

    def _check_just_pressed(self, binding):
        if isinstance(binding, int):  # Keyboard key
            return binding in self._keys_pressed
        elif isinstance(binding, tuple):
            kind = binding[0]
            if kind == "mouse":
                return binding[1] in self._mouse_buttons_pressed
            elif kind == "joy_button":
                joy_id, btn = binding[1], binding[2]
                return btn in self._joy_buttons_pressed.get(joy_id, set())
        elif isinstance(binding, list):  # Combo binding
            return self._check_just_pressed(binding[-1]) and all(
                self._check_pressed(part) for part in binding[:-1]
            )
        return False

    def rebind(self, action, new_bindings):
        if not isinstance(new_bindings, list):
            new_bindings = [new_bindings]
        self.bindings[action] = new_bindings
