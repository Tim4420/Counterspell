'''import pygame

pygame.init()
screen = pygame.display.set_mode((1200, 700))

while True:
    for event in pygame.event.get():
        if event.type == pygame.quit():
            raise SystemExit'''
import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 1200, 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Self-Destruct Challenge")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

player_size = 50
player_x, player_y = WIDTH // 2, HEIGHT // 2
player_speed = 7

spike_width, spike_height = 100, 20
spike_x, spike_y = random.randint(0, WIDTH - spike_width), random.randint(0, HEIGHT - spike_height)

button_width, button_height = 60, 30
button_x, button_y = random.randint(0, WIDTH - button_width), random.randint(0, HEIGHT - button_height)
button_pressed = False

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

    if (spike_x < player_x < spike_x + spike_width or spike_x < player_x + player_size < spike_x + spike_width) and \
       (spike_y < player_y < spike_y + spike_height or spike_y < player_y + player_size < spike_y + spike_height):
        game_over = True

    if (button_x < player_x < button_x + button_width or button_x < player_x + player_size < button_x + button_width) and \
       (button_y < player_y < button_y + button_height or button_y < player_y + player_size < button_y + button_height):
        button_pressed = True

    if button_pressed:
        spike_x, spike_y = random.randint(0, WIDTH - spike_width), random.randint(0, HEIGHT - spike_height)
        button_pressed = False

    timer -= 1
    if timer <= 0:
        running = False

    pygame.draw.rect(screen, BLACK, (player_x, player_y, player_size, player_size))
    pygame.draw.rect(screen, RED, (spike_x, spike_y, spike_width, spike_height))
    pygame.draw.rect(screen, GREEN, (button_x, button_y, button_width, button_height))

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
