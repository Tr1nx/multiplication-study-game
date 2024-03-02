import pygame

pygame.init()
screen = pygame.display.set_mode((500, 500))
background = pygame.image.load("background.jpg")
bg = pygame.transform.scale(background, (500, 500))

height = 500
n = 0
time = pygame.time.Clock()

fly = True
while fly:
    time.tick(40)
    screen.fill((0, 0, 0))
    screen.blit(bg, (0, n))
    screen.blit(bg, (0, -height+n))

    if n == height:
        screen.blit(bg, (0, -height+n))
        n = 0
    n += 1

    pygame.display.update()