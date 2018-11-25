import pygame
import ptext
from os import path

_assets = {}
for x in ["milk", "broccoli", "bone", "fish"]:
    _assets[x] = pygame.image.load(path.join("assets", x + ".png"))


class Obstacle(pygame.sprite.Sprite):

    DESTROY_TICK_TIME = 10

    def __init__(self, for_dog, for_cat, pos=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.image = self._whatami(for_dog, for_cat)
        self.rect = self.image.get_rect()
        [self.rect.x, self.rect.y] = pos
        self.for_what = []
        if for_dog: self.for_what.append('dog')
        if for_cat: self.for_what.append('cat')
        self.gone = False
        self._destroy = False
        self._destroy_ticker = 0

    def update(self, gravity=0):
        self._drop(gravity)
        # tick destroy until you disappear
        if self._destroy:
            if self._destroy_ticker > 0:
                self._destroy_ticker -= 1
            else:
                self.gone = True

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

    def destroy(self, points):
        self._destroy = True
        self._destroy_ticker = self.DESTROY_TICK_TIME

        self.image = ptext.draw(points, (0, 0), surf=None,
            fontname='assets/GochiHand-Regular.ttf', fontsize=50, color="white",
            owidth=1.5, ocolor="black")[0]
