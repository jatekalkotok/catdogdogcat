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

        # Things for game difficulty
        self.gravity = 1
        self.gravity_tick = 0.5
        self.difficulty = 1
        self.difficulty_frequency_sec = 10
        self.difficulty_tick_time = 10

        self.clock = pygame.time.Clock()

        # time in seconds when a new obstacle needs to be added to the game
        self.obstacle_tick_time = 0
        self.obstacles = pygame.sprite.Group()

        # player score
        self.points = 0
        self.MIN_SCORE = -9

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
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.animal.dog.left()
            self.animal.update_body()
        if keys[pygame.K_a]:
            self.animal.cat.left()
            self.animal.update_body()
        if keys[pygame.K_RIGHT]:
            self.animal.dog.right()
            self.animal.update_body()
        if keys[pygame.K_d]:
            self.animal.cat.right()
            self.animal.update_body()

    def loop(self):
        # step useless FPS clock
        milliseconds = self.clock.tick(self.FPS)
        self.playtime += milliseconds / 1000.0

        if self.animal.dog.move_ticker > 0:
            self.animal.dog.move_ticker -= 1
        if self.animal.cat.move_ticker > 0:
            self.animal.cat.move_ticker -= 1

        # generate new animal food
        if int(self.playtime) == self.obstacle_tick_time:
            # Next obstacle will be added 1-2 sec later
            self.obstacle_tick_time += randint(1, 2)
            self.obstacles.add(Obstacle(
                bool(randint(0, 1)),
                bool(randint(0, 1)),
                (randint(10, self.screen.get_size()[0] - 10), 10)))

        # animal food falls down
        self.obstacles.update(self.gravity)

        # food off the screen is removed
        # TODO: instead of _off_ the screen, trigger when _hits_ the screen and
        # have a dramatic impact animation so the player feels it is bad
        for o in self.obstacles:
            if o.rect.y > self.screen.get_rect().height:
                self.obstacles.remove(o)
                self.points -= 1

        if int(self.playtime) == self.difficulty_tick_time:
            self.difficulty_tick_time += self.difficulty_frequency_sec
            self.gravity += self.gravity_tick
            self.difficulty += 1

        self.text = "Food: {0:d}  Points: {1:d}  Playtime: {2:.2f}  Difficulty: {3:d}".format(
            len(self.obstacles),
            self.points,
            self.playtime,
            self.difficulty)

        if self.points < self.MIN_SCORE:
            print("GAME OVER")
            self.running = False

    def render(self):
        self.screen.blit(self.background_image, (0, 0))
        self.obstacles.draw(self.screen)

        pygame.draw.line(self.screen,
                         self.animal.body.color,
                         self.animal.body.sides[0],
                         self.animal.body.sides[1],
                         self.animal.body.thickness)
        self.screen.blit(self.animal.dog.image, self.animal.dog.rect)
        self.screen.blit(self.animal.cat.image, self.animal.cat.rect)

        pygame.display.set_caption(self.text)
        pygame.display.update()


if __name__ == "__main__":
    main = Main((800, 600))
    main.main()
