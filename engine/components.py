import pygame
from engine.object_manger import Component,GameObject
from engine.global_resourses import resource_path, resources
import math

class Transform(Component):
    def __init__(self, game_object, x=0, y=0, rotation=0, scale_x=1, scale_y=1):
        super().__init__(game_object)
        self.x = x
        self.y = y
        self.rotation = rotation  # in degrees
        self.scale_x = scale_x
        self.scale_y = scale_y

        # For future child-parent hierarchy (optional)
        self.parent = None
        self.children = []

    # --- Position ---
    def set_position(self, x, y):
        self.x = x
        self.y = y

    def get_position(self):
        return (self.x, self.y)

    def translate(self, dx, dy):
        self.x += dx
        self.y += dy

    # --- Rotation ---
    def set_rotation(self, angle_deg):
        self.rotation = angle_deg

    def rotate(self, delta_angle):
        self.rotation += delta_angle

    # --- Scale ---
    def set_scale(self, sx, sy):
        self.scale_x = sx
        self.scale_y = sy

    def get_scale(self):
        return (self.scale_x, self.scale_y)

    # --- Direction Vector ---
    def get_forward_vector(self):
        """Returns a unit vector pointing in the direction of rotation."""
        radians = math.radians(self.rotation)
        return (math.cos(radians), math.sin(radians))

    # --- Matrix (for future OpenGL, camera, etc.) ---
    def get_matrix(self):
        """Returns a 3x3 transformation matrix (2D affine)."""
        radians = math.radians(self.rotation)
        cos_r = math.cos(radians)
        sin_r = math.sin(radians)

        # 2D Transform matrix: scale * rotate * translate
        return [
            [self.scale_x * cos_r, -self.scale_y * sin_r, self.x],
            [self.scale_x * sin_r,  self.scale_y * cos_r, self.y],
            [0,                    0,                    1]
        ]

    # --- Parent/Child Hierarchy (optional) ---
    def set_parent(self, parent_transform):
        if self.parent:
            self.parent.children.remove(self)
        self.parent = parent_transform
        parent_transform.children.append(self)

    def get_world_position(self):
        """Returns global position if parented."""
        if self.parent:
            px, py = self.parent.get_world_position()
            return (self.x + px, self.y + py)
        return (self.x, self.y)


class Renderer(Component):
    def __init__(self, game_object, image_path, scale_image=True, layer=0):
        super().__init__(game_object)
        self.image_path = image_path
        self.original_image = resources.get_image(image_path)
        self.image = self.original_image.copy()

        self.layer = layer
        self.scale_image = scale_image

    def draw(self, screen):
        transform = self.game_object.get_component(Transform)
        if not transform:
            return

        # Apply rotation
        rotated_image = pygame.transform.rotate(self.original_image, -transform.rotation)

        # Apply scaling
        if self.scale_image:
            size = (
                int(rotated_image.get_width() * transform.scale_x),
                int(rotated_image.get_height() * transform.scale_y)
            )
            rotated_image = pygame.transform.scale(rotated_image, size)

        # Position adjustment (centered)
        rect = rotated_image.get_rect(center=(transform.x, transform.y))

        screen.blit(rotated_image, rect.topleft)