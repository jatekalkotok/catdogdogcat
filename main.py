import pygame
from Circle import Circle
from random import randint

circle_list = []

def main():
    pygame.init()
    logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("minimal program")

    screen = pygame.display.set_mode((800, 600))
    dog = pygame.image.load("dog.png")
    cat = pygame.image.load("cat.png")

    [dog_x, dog_y] = dog.get_size()
    [cat_x, cat_y] = cat.get_size()

    background = pygame.Surface(screen.get_size())
    background.fill((255, 255, 255))
    background = background.convert()
    screen.blit(background, (0, 0))

    clock = pygame.time.Clock()

    print("start")
    running = True
    FPS = 30
    playtime = 0.0

    [screen_x, screen_y] = screen.get_size()
    step = 10

    dogX = screen_x / 4 * 3 - dog_x / 2
    dogY = screen_y - dog_y

    catX = screen_x / 4 - cat_x / 2
    catY = screen_y - cat_y

    while running:
        milliseconds = clock.tick(FPS)
        playtime += milliseconds / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("caught safe quit")
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_LEFT:
                    dogX = 0 if dogX <= 0 else dogX - step
                if event.key == pygame.K_a:
                    catX = 0 if catX <= 0 else catX - step
                if event.key == pygame.K_RIGHT:
                    dogX = screen_x - dog_x if dogX >= screen_x - dog_x \
                        else dogX + step
                if event.key == pygame.K_d:
                    catX = screen_x - cat_x if catX >= screen_x - cat_x \
                        else catX + step

        # refreshing shit
        text = "FPS: {0:.2f}  Playtime: {1:.2f}".format(clock.get_fps(),
                                                        playtime)

        screen.blit(background, (0, 0))
        screen.blit(dog, (dogX, dogY))
        screen.blit(cat, (catX, catY))

        point1 = dogX + dog_x / 2, dogY + dog_y / 2
        point2 = catX + cat_x / 2, catY + cat_y / 2
        pygame.draw.line(screen, (255, 0, 255), point1, point2, 10)

        # if int(playtime) % 2 == 0:
        circle_list.append(Circle((randint(0, 150), randint(0, 150), randint(0, 150)), (randint(10, screen_x - 10), 10)))
        for circle in circle_list:
            pygame.draw.circle(screen, circle.color, circle.pos, circle.radius, circle.width)

        pygame.display.set_caption(text)
        pygame.display.update()


if __name__ == "__main__":
    main()

