import pygame
from os import path

_assets = {}
for x in ["milk", "broccoli", "bone", "fish"]:
    _assets[x] = pygame.image.load(path.join("assets", x + ".png"))

class Obstacle:
    for_dog = None
    for_cat = None
    pos = (0, 0)

    def __init__(self, for_dog, for_cat, pos):
        self.for_dog = for_dog
        self.for_cat = for_cat
        self.pos = pos

    def drop(self, gravity):
        self.pos = (self.pos[0], self.pos[1] + gravity)

    def get_asset(self):
        if self.for_dog and self.for_cat:
            return _assets["milk"]
        elif not self.for_dog and not self.for_cat:
            return _assets["broccoli"]
        elif self.for_dog:
            return _assets["bone"]
        else:
            return _assets["fish"]
