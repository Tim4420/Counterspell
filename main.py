import pygame

pygame.init()
screen = pygame.display.set_mode((1200, 700))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise SystemExit
