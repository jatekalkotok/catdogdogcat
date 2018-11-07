import pygame
from os import path

_assets = {}
for x in ["milk", "broccoli", "bone", "fish"]:
    _assets[x] = pygame.image.load(path.join("assets", x + ".png"))

class Obstacle:
    def __init__(self, for_dog, for_cat, pos = (0, 0)):
        self.image = self._whatami(for_dog, for_cat)
        self.pos = pos

    def _whatami(self, for_dog, for_cat):
        if for_dog and for_cat:
            return _assets["milk"]
        elif not for_dog and not for_cat:
            return _assets["broccoli"]
        elif for_dog:
            return _assets["bone"]
        else:
            return _assets["fish"]

    def drop(self, gravity):
        self.pos = (self.pos[0], self.pos[1] + gravity)
