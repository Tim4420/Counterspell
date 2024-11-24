import pygame
import random
import sys

# Functions
def resize_images(images, scale_factor):
    return [pygame.transform.scale(img, (int(img.get_width() * scale_factor), int(img.get_height() * scale_factor))) for img in images]

def generate_random_items(item_images, num_items, floor_height, world_width):
    items = []
    for i in range(2):
        img = random.choice(item_images)
        x = random.randint(0, world_width - img.get_width())
        y = floor_height - img.get_height()
        items.append({"image": img, "x": x, "y": y})
    return items

def check_item_pickup(player_rect, items, pickup_range):
    for item in items[:]:  # Copy the list to safely modify it
        item_rect = pygame.Rect(item["x"], item["y"], item["image"].get_width(), item["image"].get_height())
        if player_rect.colliderect(item_rect.inflate(pickup_range, pickup_range)):
            return item
    return None

def drop_item(collected_item, floor_height):
    # Drop the item back to the floor
    collected_item["y"] = floor_height - collected_item["image"].get_height()
    return collected_item

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 1200, 700
FLOOR_HEIGHT = HEIGHT - 300
FPS = 30
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("60 Seconds Of Self")
clock = pygame.time.Clock()

# Load images
bg = pygame.image.load("Background.png")
standing_img = pygame.image.load("character/Standing.png")
walking_left_imgs = [pygame.image.load(f"character/WalkingLeft{i}.png") for i in range(1, 7)]
walking_right_imgs = [pygame.image.load(f"character/WalkingRight{i}.png") for i in range(1, 7)]
item_images = [
    pygame.image.load("item/Red Coach.png"),
    pygame.image.load("item/Blue Coach.png"),
    pygame.image.load("item/Yellow Coach.png"),
    pygame.image.load("item/Coffee Machine.png"),
    pygame.image.load("item/Coffee.png"),
    pygame.image.load("item/Coke.png"),
    pygame.image.load("item/Tall Plant.png"),
    pygame.image.load("item/Short Plant.png")
]
window,broken = pygame.image.load("Window.png"), pygame.image.load("Window_Cracked.png")

# Resize images
scale_factor = 7
standing_img = pygame.transform.scale(standing_img,(int(standing_img.get_width() * scale_factor), int(standing_img.get_height() * scale_factor)))
item_images[0],item_images[1], item_images[2] = pygame.transform.scale(item_images[0],(int(item_images[0].get_width() * 1.1), int(item_images[0].get_height() * 1.1))), pygame.transform.scale(item_images[1],(int(item_images[1].get_width() * 1.1), int(item_images[1].get_height() * 1.1))), pygame.transform.scale(item_images[2],(int(item_images[2].get_width() * 1.1), int(item_images[2].get_height() * 1.1)))
item_images[3] = pygame.transform.scale(item_images[3],(int(item_images[3].get_width() * 0.5), int(item_images[3].get_height() * 0.5)))
item_images[4], item_images[5] = pygame.transform.scale(item_images[4],(int(item_images[4].get_width() * 0.4), int(item_images[4].get_height() * 0.4))), pygame.transform.scale(item_images[5],(int(item_images[5].get_width() * 0.5), int(item_images[5].get_height() * 0.5)))
item_images[6], item_images[7] = pygame.transform.scale(item_images[6],(int(item_images[6].get_width() * 0.5), int(item_images[6].get_height() * 0.5))), pygame.transform.scale(item_images[7],(int(item_images[7].get_width() * 0.5), int(item_images[7].get_height() * 0.5)))


walking_left_imgs, walking_right_imgs = resize_images(walking_left_imgs, scale_factor), resize_images(walking_right_imgs, scale_factor)
item_images = resize_images(item_images, scale_factor)
bg = pygame.transform.scale(bg, (3000, HEIGHT))  # Scale to world width
window = pygame.transform.scale(window, (int(window.get_width() * 15), int(window.get_height() * 15)))  # Scale if needed
broken = pygame.transform.scale(broken, (int(broken.get_width() * 10), int(broken.get_height() * 10)))  # Scale if needed


# World attributes
WORLD_WIDTH = 3000

# Character attributes
x, y = WIDTH // 2, FLOOR_HEIGHT
velocity = 15
jumping = False
y_velocity = 0

pygame.mixer.init()
pygame.mixer.music.load('28. Hadopelagic Pressure.mp3')


# Animation variables
left = False
right = False
frame = 0  # For cycling through frames
animation_delay = 100  # Delay in milliseconds
last_update_time = pygame.time.get_ticks()
pygame.font.init()
font = pygame.font.Font("Minecraft.ttf", 40)
countdown_time = 60  # 60 seconds
start_ticks = pygame.time.get_ticks()

# Camera attributes
camera_x = 0

# Generate random items
items = generate_random_items(item_images, num_items=10, floor_height=FLOOR_HEIGHT, world_width=WORLD_WIDTH)

# Collected item
collected_item = None

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)

# Game loop
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get key states
    keys = pygame.key.get_pressed()

    # Horizontal movement logic
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:  # Move left
        x -= velocity
        left, right = True, False
    elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:  # Move right
        x += velocity
        left, right = False, True
    else:
        left, right = False, False
    if keys[pygame.K_w] or keys[pygame.K_UP]:  # Move up
        y -= velocity
    elif keys[pygame.K_s] or keys[pygame.K_RIGHT]:  # Move down
        y += velocity

    # Keep character within world boundaries
    x = max(0, min(x, WORLD_WIDTH - standing_img.get_width()))
    y = max(0, min(y, HEIGHT - standing_img.get_height()))  # Prevent going out of frame vertically

    # Update camera position
    camera_x = x - WIDTH // 2
    camera_x = max(0, min(camera_x, WORLD_WIDTH - WIDTH))  # Keep camera within bounds

    # Pickup items
    player_rect = pygame.Rect(x, y, standing_img.get_width(), standing_img.get_height())
    if keys[pygame.K_SPACE]:
        if collected_item == None:
            collected_item = check_item_pickup(player_rect, items, pickup_range=20)
            if collected_item:
                items.remove(collected_item)
        else:
            # Drop the held item back to its original position on the floor        
                collected_item = drop_item(collected_item, FLOOR_HEIGHT)

    # Draw background
    screen.blit(bg, (-camera_x, 0))
    screen.blit(window, (-140-camera_x, -40))
    screen.blit(window, (-140 - camera_x, 200))
    screen.blit(window, (-140 - camera_x, 450))

    # Draw items
    for item in items:
        screen.blit(item["image"], (item["x"] - camera_x, item["y"]))

  # Calculate the remaining time
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000  # Convert to seconds
    remaining_time = max(0, countdown_time - elapsed_time)  # Prevent negative values


    # Format time as MM:SS
    minutes = int(remaining_time // 60)
    seconds = int(remaining_time % 60)
    timer_text = f"{minutes:02}:{seconds:02}"
    timer_surface = font.render(timer_text, True, (RED if seconds <= 10 else BLACK))
    screen.blit(timer_surface, (WIDTH // 2 - 50, 10))
    # Animation handling
    current_time = pygame.time.get_ticks()
    if current_time - last_update_time > animation_delay:
        frame = (frame + 1) % 6  # Loop through frames
        last_update_time = current_time

    if seconds >= 10 and not pygame.mixer.music.get_busy():
        pygame.mixer.music.play(1)


    # Draw the character
    if left:
        screen.blit(walking_left_imgs[frame], (x - camera_x, y))
    elif right:
        screen.blit(walking_right_imgs[frame], (x - camera_x, y))
    else:
        screen.blit(standing_img, (x - camera_x, y))

    # Draw collected item above the player
    if collected_item:
        item_image = collected_item["image"]
        item_x = x - camera_x + (standing_img.get_width() - item_image.get_width()) // 2  # Center above player
        item_y = y - item_image.get_height() + 150 
        screen.blit(item_image, (item_x, item_y))
    else:
        for item in items:
            screen.blit(item["image"], (item["x"] - camera_x, item["y"]))
    print(collected_item)


    if seconds <= 0:
        death_sound = pygame.mixer.music.load('super-mario-death-sound-sound-effect.mp3')

        screen.fill(BLACK)
        pygame.mixer.music.play(1)
        end1 = font.render("YOU DID NOT DIE, YOU LOST", True, (255, 0, 0))
        pygame.time.wait(5000)
        print("bruh")
        screen.blit(end1, (WIDTH // 2 - 50, 10))
        pygame.quit()

    # Update the display
    pygame.display.update()

    

pygame.quit()