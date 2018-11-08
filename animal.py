import pygame
from os import path

class Animal:
    """Never in my life did I think I would really make an animal class."""

    def __init__(self, screen):
        self.cat = Head("cat", screen)
        self.dog = Head("dog", screen)

class Head:
    """One head of the animal."""

    def __init__(self, animal_type, screen):
        if animal_type not in ["dog", "cat"]:
            raise ValueError("Animal Head must be one of 'dog' or 'cat'")
        self.animal_type = animal_type
        self.image = pygame.image.load(
                path.join("assets", animal_type + ".png"))
        self.pos = self._start_pos(screen)
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
        print(self.animal_type + " move left")
        x = self.pos[0]
        x = 0 if x <= 0 else x - self._step
        self.pos = (x, self.pos[1])
        self._recenter()

    def right(self, screen):
        """Step right but not off the screen"""
        print(self.animal_type + " move right")
        x = self.pos[0]
        screen_max = screen.get_size()[0]
        x = screen_max if x >= screen_max else x + self._step
        self.pos = (x, self.pos[1])
        self._recenter()
