from enum import Enum
import random
import pygame as pyg


class ENTITY(Enum):
    BALDO = "baldo"          # Winning
    WALDO = "failure"       # U R A FAILURE
    JAM = "nom"             # +10s
    MARMELADE = "nom nom"   # +15s


# --------------------------------------------------
# Base Entity
# --------------------------------------------------

class Entity:
    def __init__(self, x, y, base_texture, mask_texture=None, scale=2):
        self.x = x
        self.y = y
        self.scale = scale

        # Load images ONCE
        self.base_image = pyg.image.load(base_texture).convert_alpha()
        self.mask_image = (
            pyg.image.load(mask_texture).convert_alpha()
            if mask_texture else None
        )

        # Pre-scale images
        self.scaled_base = pyg.transform.scale_by(self.base_image, self.scale)
        self.scaled_mask = (
            pyg.transform.scale_by(self.mask_image, self.scale)
            if self.mask_image else None
        )

        # Rect exists immediately (important!)
        self.rect = self.scaled_base.get_rect(topleft=(self.x, self.y))

    def draw(self, surface):
        surface.blit(self.scaled_base, self.rect.topleft)
        if self.scaled_mask:
            surface.blit(self.scaled_mask, self.rect.topleft)

        # Debug hitbox (optional)
        # pyg.draw.rect(surface, (255, 0, 0), self.rect, 2)

    def on_click(self, event):
        if event.type == pyg.MOUSEBUTTONDOWN:
            return self.rect.collidepoint(event.pos)
        return False


# --------------------------------------------------
# Baldo (win condition)
# --------------------------------------------------

class Baldo(Entity):
    def __init__(self, x, y, base_texture="Assets/baldo_01.png"):
        super().__init__(x, y, base_texture)

    def on_click(self, event):
        if super().on_click(event):
            return ENTITY.BALDO
        return None


# --------------------------------------------------
# Waldo (decoy)
# --------------------------------------------------

class Waldo(Entity):
    def __init__(self, x, y, scale=2):
        base, mask = self._random_textures()
        super().__init__(x, y, base, mask, scale)

    def _random_textures(self):
        path = "Assets/"
        base = f"{path}base_{random.randint(1, 6)}.png"
        mask = f"{path}mask_{random.randint(1, 9)}.png"
        return base, mask

    def on_click(self, event):
        if super().on_click(event):
            return ENTITY.WALDO
        return None


# --------------------------------------------------
# Jar (bonus time)
# --------------------------------------------------

class Jar(Entity):
    def __init__(self, x, y, jar_type, scale=2):
        self.jar_type = jar_type

        texture = (
            "Assets/jam.png"
            if jar_type == ENTITY.JAM
            else "Assets/marmelade.png"
        )

        super().__init__(x, y, texture, scale=scale)

    def on_click(self, event):
        if super().on_click(event):
            return self.jar_type
        return None
