import pygame
from os import path


class Animal:
    """Never in my life did I think I would really make an animal class."""

    def __init__(self, screen):
        self.cat = Head("cat", screen)
        self.dog = Head("dog", screen)
        self.body = Body(screen, self.cat.image.get_size()[0]
                         + self.dog.image.get_size()[0])
        self.update_body()

    def update_body(self):
        self.body.calculate_body(self.dog.rect.center, self.cat.rect.center)


class Body:
    """ Body between the heads """

    sides = ((0, 0), (0, 0))
    color = (0, 0, 255)
    thickness_multiplier = 10

    @property
    def thickness(self):
        distance = abs(self.sides[0][0] - self.sides[1][0])
        if distance <= self.heads_size / 2:
            distance = self.heads_size / 2
        return int(self.screen.get_size()[0] / distance
                   * self.thickness_multiplier)

    def __init__(self, screen, heads_size):
        self.screen = screen
        self.heads_size = heads_size

    def calculate_body(self, start, end):
        self.sides = (start, end)


class Head(pygame.sprite.Sprite):
    """One head of the animal."""

    MOVE_TICK_TIME = 2

    def __init__(self, animal_type, screen):
        pygame.sprite.Sprite.__init__(self)
        if animal_type not in ["dog", "cat"]:
            raise ValueError("Animal Head must be one of 'dog' or 'cat'")
        self.screen = screen
        self.animal_type = animal_type
        self.image = pygame.image.load(
            path.join("assets", animal_type + ".png"))
        self.rect = self.image.get_rect()
        self._start_pos()
        self.move_ticker = 0
        self._step = screen.get_size()[0] / self.image.get_size()[0] / 2

    def _start_pos(self):
        """Calculate starting position for animal head"""
        # shortcuts
        [[s_w, s_h], [i_w, i_h]] = [ self.screen.get_size(), self.image.get_size() ]

        # what name do you give a multiplier for positioning based on what side
        # of the screen a thing is on?
        side_multiplier = 1 if self.animal_type is "cat" else 3

        self.rect.x = s_w / 4 * side_multiplier - i_w / 2
        self.rect.y = s_h - i_h

    def left(self):
        """Step left but not into negative"""
        if self.move_ticker > 0: return
        if self.rect.x > 0: self.rect.move_ip(-self._step, 0)
        self.move_ticker = self.MOVE_TICK_TIME

    def right(self):
        """Step right but not off the screen"""
        if self.move_ticker > 0: return
        if self.rect.x < self.screen.get_rect().width - self.rect.width:
            self.rect.move_ip(self._step, 0)
        self.move_ticker = self.MOVE_TICK_TIME
