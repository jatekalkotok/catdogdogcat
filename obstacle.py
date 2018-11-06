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
            return "milk.png"
        elif not self.for_dog and not self.for_cat:
            return "broccoli.png"
        elif self.for_dog:
            return "bone.png"
        else:
            return "fish.png"
