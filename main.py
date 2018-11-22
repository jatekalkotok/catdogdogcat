import pygame
from animal import Animal
from obstacle import Obstacle
from random import randint
from os import path
from menupoint import MenuPoint


class Main:
    """Thing to hold the whole game together. """

    def __init__(self, resolution):
        print("starting up")
        pygame.init()
        self.screen = pygame.display.set_mode(resolution)

        self.title = "catdogdogcat"

        self.running = True
        self.paused = False

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
        pygame.display.set_caption(self.title)

        self.background_image = \
            pygame.image.load(path.join("assets", "background.png")).convert()

        self.animal = Animal(self.screen)

        self.fonts = {
            'score': pygame.font.Font('assets/GochiHand-Regular.ttf', 50),
            'title': pygame.font.Font('assets/GochiHand-Regular.ttf', 100),
            'menu': pygame.font.Font('assets/GochiHand-Regular.ttf', 30)
        }

        # menu
        self.text_color = (0, 0, 0)
        self.menu_color = (0, 0, 255)
        self.menu_item_texts = ["Start", "Quit"]
        self.menu_items = []
        self.selected_menu_item = 0

    def main(self):
        while self.running:
            if not self.paused:
                self.game_events()
                self.loop_game()
                self.render_game()
            else:
                self.menu_events()
                if self.paused:
                    self.loop_menu()
                    self.render_menu()

    def game_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("caught safe quit")
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
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

    def loop_game(self):
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
                if len(o.for_what): self.points -= 1

        if int(self.playtime) == self.difficulty_tick_time:
            self.difficulty_tick_time += self.difficulty_frequency_sec
            self.gravity += self.gravity_tick
            self.difficulty += 1

        # food you catch earns points
        for a in [self.animal.dog, self.animal.cat]:
            caught = pygame.sprite.spritecollide( a, self.obstacles, True)
            self.points += len([c for c in caught if a.animal_type in c.for_what])
            miscatch = len([c for c in caught if a.animal_type not in c.for_what])
            self.points -= 2 * miscatch
            if miscatch > 0: a.freeze()

        # update heads state
        self.animal.dog.update()
        self.animal.cat.update()

        self.text = "Food: {0:d}  Points: {1:d}  Playtime: {2:.2f}  Difficulty: {3:d}".format(
            len(self.obstacles),
            self.points,
            self.playtime,
            self.difficulty)

        if self.points < self.MIN_SCORE:
            print("GAME OVER")
            self.running = False

    def render_game(self):
        self.screen.blit(self.background_image, (0, 0))
        self.obstacles.draw(self.screen)

        pygame.draw.line(self.screen,
                         self.animal.body.color,
                         self.animal.body.sides[0],
                         self.animal.body.sides[1],
                         self.animal.body.thickness)
        self.screen.blit(self.animal.dog.image, self.animal.dog.rect)
        self.screen.blit(self.animal.cat.image, self.animal.cat.rect)

        self.screen.blit(self.fonts['score'].render(
            "score: {:d}".format(self.points), False, (255, 255, 255)), (0, 0))

        pygame.display.set_caption(self.text)
        pygame.display.update()

    def loop_menu(self):
        self.clock.tick(self.FPS)

    def menu_events(self):
      for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("caught safe quit")
                self.running = False
            keys = pygame.key.get_pressed()
            if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self.selected_menu_item < len(self.menu_item_texts) - 1:
                self.selected_menu_item += 1
            if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.selected_menu_item > 0:
                self.selected_menu_item -= 1
            if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
                if self.selected_menu_item == 0:
                    self.menu_item_texts[0] = "Resume"
                    self.paused = False
                elif self.selected_menu_item == 1:
                    self.running = False

    def render_menu(self):
        self.screen.blit(self.background_image, (0, 0))

        title_text = self.fonts['title'].render(self.title, False, self.text_color)
        self.screen.blit(title_text, (self.screen.get_size()[0] / 2 - title_text.get_width() / 2,
                                      self.screen.get_size()[1] / 4))

        self.menu_items.clear()
        for i in range(len(self.menu_item_texts)):
            string = self.menu_item_texts[i]
            text = self.fonts['menu'].render(string, False, self.text_color)
            menu_point = MenuPoint(text, self.screen.get_size()[
                0] / 2 - text.get_width() / 2,
                                   self.screen.get_size()[1] / 2 + i * (
                                           text.get_height() + 10))
            self.menu_items.append(menu_point)

        current = self.menu_items[self.selected_menu_item]
        pygame.draw.line(self.screen,
                         self.menu_color,
                         (current.x - 10,
                          current.y + current.menu.get_height() / 2),
                         (current.x + current.menu.get_width() + 10,
                          current.y + current.menu.get_height() / 2),
                         self.menu_items[0].menu.get_height() + 5)

        for menu_point in self.menu_items:
            self.screen.blit(menu_point.menu, (menu_point.x, menu_point.y))

        pygame.display.update()


if __name__ == "__main__":
    main = Main((800, 600))

    # Renders the game first, then immediately pauses it
    main.game_events()
    main.loop_game()
    main.render_game()
    main.paused = True
    # ps.: I hack you

    main.main()
