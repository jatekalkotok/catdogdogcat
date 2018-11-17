import pygame
from os import path

_assets = {}
for x in ["milk", "broccoli", "bone", "fish"]:
    _assets[x] = pygame.image.load(path.join("assets", x + ".png"))


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, for_dog, for_cat, pos=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.image = self._whatami(for_dog, for_cat)
        self.rect = self.image.get_rect()
        [self.rect.x, self.rect.y] = pos

    def update(self, gravity):
        self._drop(gravity)

    def _whatami(self, for_dog, for_cat):
        if for_dog and for_cat:
            return _assets["milk"]
        elif not for_dog and not for_cat:
            return _assets["broccoli"]
        elif for_dog:
            return _assets["bone"]
        else:
            return _assets["fish"]

    def _drop(self, gravity):
        self.rect.move_ip(0, gravity)
