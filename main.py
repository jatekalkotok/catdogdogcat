import pygame
from animal import Animal
from obstacle import Obstacle
from random import randint
from os import path


class Main:
    """Thing to hold the whole game together. """

    def __init__(self, resolution):
        print("starting up")
        pygame.init()
        self.screen = pygame.display.set_mode(resolution)

        self.running = True
        self.FPS = 30
        self.playtime = 0.0
        self.gravity = 1

        self.clock = pygame.time.Clock()

        # time in seconds when a new obstacle needs to be added to the game
        self.obstacle_tick_time = 0
        self.obstacles = []

        self.move_ticker = 0

        logo = pygame.image.load(path.join("assets", "logo32x32.png"))
        pygame.display.set_icon(logo)
        pygame.display.set_caption("catdogdogcat")

        self.background_image = \
            pygame.image.load(path.join("assets", "background.png")).convert()

        self.animal = Animal(self.screen)

    def main(self):
        while self.running:
            self.events()
            self.loop()
            self.render()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("caught safe quit")
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: self.running = False
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: self.animal.dog.left()
        if keys[pygame.K_a]: self.animal.cat.left()
        if keys[pygame.K_RIGHT]: self.animal.dog.right(self.screen)
        if keys[pygame.K_d]: self.animal.cat.right(self.screen)

    def loop(self):
        # step useless FPS clock
        milliseconds = self.clock.tick(self.FPS)
        self.playtime += milliseconds / 1000.0
        self.text = "FPS: {0:.2f}  Playtime: {1:.2f}".format(
                self.clock.get_fps(),
                self.playtime)

        if self.animal.dog.move_ticker > 0:
            self.animal.dog.move_ticker -= 1
        if self.animal.cat.move_ticker > 0:
            self.animal.cat.move_ticker -= 1

        # generate new animal food
        if int(self.playtime) == self.obstacle_tick_time:
            # Next obstacle will be added 1-2 sec later
            self.obstacle_tick_time += randint(1, 2)
            self.obstacles.append(Obstacle(
                bool(randint(0, 1)),
                bool(randint(0, 1)),
                (randint(10, self.screen.get_size()[0] - 10), 10)))

        # animal food falls down
        for o in self.obstacles: o.drop(self.gravity)

    def render(self):
        self.screen.blit(self.background_image, (0, 0))

        for o in self.obstacles:
            self.screen.blit(o.image, o.pos)

        pygame.draw.line(self.screen, (255, 0, 255),
            self.animal.dog.center, self.animal.cat.center, 10)
        self.screen.blit(self.animal.dog.image, self.animal.dog.pos)
        self.screen.blit(self.animal.cat.image, self.animal.cat.pos)

        pygame.display.set_caption(self.text)
        pygame.display.update()


if __name__ == "__main__":
    main = Main((800, 600))
    main.main()
