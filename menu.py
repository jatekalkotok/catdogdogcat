import pygame
from os import path
from menupoint import MenuPoint


class Menu:

    def __init__(self, resolution):
        print("starting up")
        pygame.init()
        self.screen = pygame.display.set_mode(resolution)

        self.running = True

        self.title = "catdogdogcat"
        self.text_color = (0, 0, 0)
        self.menu_color = (0, 0, 255)
        self.menu_item_texts = ["Single Player", "Multi Player", "Settings", "Quit"]
        self.menu_items = []
        self.selected_menu_item = 0

        self.font_title = pygame.font.SysFont('Comic Sans MS', 100)
        self.font_menu = pygame.font.SysFont('Comic Sans MS', 30)

        self.background_image = \
            pygame.image.load(path.join("assets", "background.png")).convert()

        logo = pygame.image.load(path.join("assets", "logo32x32.png"))
        pygame.display.set_icon(logo)
        pygame.display.set_caption(self.title)

    def main(self):
        while self.running:
            self.events()
            # self.loop()
            self.render()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("caught safe quit")
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            keys = pygame.key.get_pressed()
            if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self.selected_menu_item < len(self.menu_item_texts) - 1:
                self.selected_menu_item += 1
            if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.selected_menu_item > 0:
                self.selected_menu_item -= 1

    # def loop(self):

    def render(self):
        self.screen.blit(self.background_image, (0, 0))

        title_text = self.font_title.render(self.title, False, self.text_color)
        self.screen.blit(title_text, (self.screen.get_size()[0] / 2 - title_text.get_width() / 2,
                                      self.screen.get_size()[1] / 3))

        for i in range(len(self.menu_item_texts)):
            string = self.menu_item_texts[i]
            text = self.font_menu.render(string, False, self.text_color)
            menu_point = MenuPoint(text, self.screen.get_size()[
                                 0] / 2 - text.get_width() / 2,
                             self.screen.get_size()[1] / 2 + i * (
                                         text.get_height() + 10))
            self.menu_items.append(menu_point)

        current = self.menu_items[self.selected_menu_item]
        pygame.draw.line(self.screen,
                         self.menu_color,
                         (current.x - 10, current.y + current.menu.get_height() / 2),
                         (current.x + current.menu.get_width() + 10, current.y + current.menu.get_height() / 2),
                         self.menu_items[0].menu.get_height() + 5)

        for menu_point in self.menu_items:
            self.screen.blit(menu_point.menu, (menu_point.x, menu_point.y))

        pygame.display.update()


if __name__ == "__main__":
    main = Menu((800, 600))
    main.main()
