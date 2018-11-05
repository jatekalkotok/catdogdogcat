import pygame

def main():
    pygame.init()
    logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("minimal program")

    screen = pygame.display.set_mode((800,600))
    image = pygame.image.load("dog.png")
    [dog_x, dog_y] = image.get_size()

    background = pygame.Surface(screen.get_size())
    background.fill((255,0,0))
    background = background.convert()
    screen.blit(background, (0,0))

    clock = pygame.time.Clock()

    print("start")
    running = True
    FPS = 30
    playtime = 0.0

    [screen_x, screen_y] = screen.get_size()
    step = 10

    x = screen_x/2 - dog_x/2
    y = screen_y - dog_y

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
                    x = 0 if x <= 0 else x-step
                if event.key == pygame.K_RIGHT:
                    x = screen_x - dog_x if x >= screen_x - dog_x else x+step

        # refreshing shit
        text = "FPS: {0:.2f}  Playtime: {1:.2f}".format(clock.get_fps(), playtime)

        screen.blit(background, (0, 0))
        screen.blit(image, (x, y))

        pygame.display.set_caption(text)
        pygame.display.update()

if __name__ == "__main__":
    main()
