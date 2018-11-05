class Circle:
    color = (0, 0, 0)
    pos = (0, 0)
    radius = 10
    width = 10

    def __init__(self, color, pos):
        self.color = color
        self.pos = pos

    def drop(self, gravity):
        self.pos = (self.pos[0], self.pos[1] + gravity)
