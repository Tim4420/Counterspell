'''import pygame

pygame.init()
screen = pygame.display.set_mode((1200, 700))

while True:
    for event in pygame.event.get():
        if event.type == pygame.quit():
            raise SystemExit'''
import pygame
import sys
import os

pygame.init()

WIDTH, HEIGHT = 1200, 700
WHITE = (254, 254, 254)
BLACK = (25, 25, 25)
RED = (255, 25, 25)
BLACK = (23, 23, 23)
GREEN = (25, 255, 25)
ALPHA = (0, 255, 0)

FPS = 30

class employee(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for i in range(1,7):
            img = pygame.image.load(os.path.join('images', 'hero' + str(i) + '.png')).convert()
            img.convert_alpha()  # optimise alpha
            img.set_colorkey(ALPHA)  # set alpha
            self.images.append(img)
            self.image = self.images[0]
            self.rect = self.image.get_rect()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PLACEHOLDER")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

player_size = 50
player_x, player_y = WIDTH // 2, HEIGHT // 2
player_speed = 7


timer = 60 * 30
game_over = False

running = True
while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < HEIGHT - player_size:
        player_y += player_speed

    timer -= 1
    if timer <= 0:
        running = False

    timer_text = font.render(f"Time Left: {timer // 30}s", True, BLACK)
    screen.blit(timer_text, (10, 10))

    pygame.display.flip()
    clock.tick(30)

if game_over:
    screen.fill(WHITE)
    end_text = font.render("You Did It! Game Over.", True, RED)
    screen.blit(end_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
    pygame.display.flip()
    pygame.time.wait(3000)

pygame.quit()
sys.exit()
