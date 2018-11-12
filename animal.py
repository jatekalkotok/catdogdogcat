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
        self.body.calculate_body(self.dog.center, self.cat.center)


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


class Head:
    """One head of the animal."""

    MOVE_TICK_TIME = 2

    def __init__(self, animal_type, screen):
        if animal_type not in ["dog", "cat"]:
            raise ValueError("Animal Head must be one of 'dog' or 'cat'")
        self.animal_type = animal_type
        self.image = pygame.image.load(
            path.join("assets", animal_type + ".png"))
        self.pos = self._start_pos(screen)
        self.move_ticker = 0
        self._step = screen.get_size()[0] / self.image.get_size()[0] / 2
        self._center = self.image.get_rect().center
        self._recenter()

    def _start_pos(self, screen):
        """Calculate starting position for animal head
        :returns: array of coordinates
        """
        # shortcuts
        [[s_x, s_y], [i_x, i_y]] = [screen.get_size(), self.image.get_size()]

        # what name do you give a multiplier for positioning based on what side
        # of the screen a thing is on?
        side_multiplier = 1 if self.animal_type is "cat" else 3

        return [
            s_x / 4 * side_multiplier - i_x / 2,
            s_y - i_y
        ]

    def _recenter(self):
        """Reposition centre point based on position and image centre"""
        self.center = (
            self.pos[0] + self._center[0],
            self.pos[1] + self._center[1])

    def left(self):
        """Step left but not into negative"""
        if self.move_ticker > 0: return
        print(self.animal_type + " move left")
        x = self.pos[0]
        x = 0 if x <= 0 else x - self._step
        self.pos = (x, self.pos[1])
        self._recenter()
        self.move_ticker = self.MOVE_TICK_TIME

    def right(self, screen):
        if self.move_ticker > 0: return
        """Step right but not off the screen"""
        print(self.animal_type + " move right")
        x = self.pos[0]
        max_x = screen.get_size()[0] - self.image.get_size()[0]
        x = max_x if x >= max_x else x + self._step
        self.pos = (x, self.pos[1])
        self._recenter()
        self.move_ticker = self.MOVE_TICK_TIME
