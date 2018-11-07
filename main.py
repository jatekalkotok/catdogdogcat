import pygame
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

        # time in seconds when a new obstacle needs to be added to the game
        self.obstacle_tick_time = 0

        logo = pygame.image.load(path.join("assets", "logo32x32.png"))
        pygame.display.set_icon(logo)
        pygame.display.set_caption("catdogdogcat")

        self.clock = pygame.time.Clock()

        # TODO: make this also a class
        self.dog = pygame.image.load(path.join("assets", "dog.png"))
        [self.dog_x, self.dog_y] = self.dog.get_size()

        self.cat = pygame.image.load(path.join("assets", "cat.png"))
        [self.cat_x, self.cat_y] = self.cat.get_size()

        self.obstacles = []

        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill((255, 255, 255))
        self.background = self.background.convert()

        [self.screen_x, self.screen_y] = self.screen.get_size()

        self.dogX = self.screen_x / 4 * 3 - self.dog_x / 2
        self.dogY = self.screen_y - self.dog_y

        self.catX = self.screen_x / 4 - self.cat_x / 2
        self.catY = self.screen_y - self.cat_y

        self.step = self.screen_x / self.dog_x / 2

    def main(self):
        while self.running:
            self.events()
            self.loop()
            self.render()

    def events(self):
        # TODO: lots of the stuff in here should probably be moved out
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("caught safe quit")
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_LEFT:
                    self.dogX = 0 if self.dogX <= 0 else self.dogX - self.step
                if event.key == pygame.K_a:
                    self.catX = 0 if self.catX <= 0 else self.catX - self.step
                if event.key == pygame.K_RIGHT:
                    if self.dogX >= self.screen_x - self.dog_x:
                        self.dogX = self.screen_x - self.dog_x
                    else:
                        self.dogX += self.step
                if event.key == pygame.K_d:
                    if self.catX >= self.screen_x - self.cat_x:
                        self.catX = self.screen_x - self.cat_x
                    else:
                        self.catX += self.step

    def loop(self):
        # step useless FPS clock
        milliseconds = self.clock.tick(self.FPS)
        self.playtime += milliseconds / 1000.0
        self.text = "FPS: {0:.2f}  Playtime: {1:.2f}".format(
                self.clock.get_fps(),
                self.playtime)


        # resize line connecting cat and dog
        self.point1 = self.dogX + self.dog_x / 2, self.dogY + self.dog_y / 2
        self.point2 = self.catX + self.cat_x / 2, self.catY + self.cat_y / 2

        # generate new animal food
        if int(self.playtime) == self.obstacle_tick_time:
            # Next obstacle will be added 1-2 sec later
            self.obstacle_tick_time += randint(1, 2)
            self.obstacles.append(Obstacle(
                bool(randint(0, 1)),
                bool(randint(0, 1)),
                (randint(10, self.screen_x - 10), 10)))

        # animal food falls down
        for o in self.obstacles: o.drop(self.gravity)

    def render(self):
        self.screen.blit(self.background, (0, 0))

        for o in self.obstacles:
            self.screen.blit(o.image, o.pos)

        pygame.draw.line(self.screen,
            (255, 0, 255), self.point1, self.point2, 10)
        self.screen.blit(self.dog, (self.dogX, self.dogY))
        self.screen.blit(self.cat, (self.catX, self.catY))

        pygame.display.set_caption(self.text)
        pygame.display.update()


if __name__ == "__main__":
    main = Main((800, 600))
    main.main()
