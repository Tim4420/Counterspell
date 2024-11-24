import pygame
import random

# Functions
def resize_images(images, scale_factor):
    return [pygame.transform.scale(img, (int(img.get_width() * scale_factor), int(img.get_height() * scale_factor))) for img in images]

def generate_random_items(item_images, num_items, floor_height, world_width):
    """Generate random items on the floor."""
    items = []
    for i in range(num_items):
        img = random.choice(item_images)
        x = random.randint(0, world_width - img.get_width())
        y = floor_height - img.get_height()
        items.append({"image": img, "x": x, "y": y})
    return items

def check_item_pickup(player_rect, items, pickup_range):
    """Check if player is within range to pick up items."""
    for item in items[:]:  # Copy the list to safely modify it
        item_rect = pygame.Rect(item["x"], item["y"], item["image"].get_width(), item["image"].get_height())
        if player_rect.colliderect(item_rect.inflate(pickup_range, pickup_range)):
            return item
    return None

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 1200, 700
FLOOR_HEIGHT = HEIGHT - 300
FPS = 30
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Camera and Items")
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

# World attributes
WORLD_WIDTH = 3000

# Character attributes
x, y = WIDTH // 2, FLOOR_HEIGHT
velocity = 15
jumping = False
y_velocity = 0

# Animation variables
left = False
right = False
frame = 0  # For cycling through frames
animation_delay = 100  # Delay in milliseconds
last_update_time = pygame.time.get_ticks()

# Camera attributes
camera_x = 0

# Generate random items
items = generate_random_items(item_images, num_items=10, floor_height=FLOOR_HEIGHT, world_width=WORLD_WIDTH)

# Collected item
collected_item = None

# Game loop
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get key states
    keys = pygame.key.get_pressed()
    print(collected_item)

    # Horizontal movement logic
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:  # Move left
        x -= velocity
        left, right = True, False
    elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:  # Move right
        x += velocity
        left, right = False, True
    else:
        left, right = False, False

    # Keep character within world boundaries
    x = max(0, min(x, WORLD_WIDTH - standing_img.get_width()))

    # Jumping logic
    if keys[pygame.K_w] and not jumping:  # Start jump
        jumping = True
        y_velocity = -15

    if jumping:
        y += y_velocity  # Apply vertical velocity
        y_velocity += 2  # Gravity
        if y >= FLOOR_HEIGHT:
            y = FLOOR_HEIGHT
            jumping = False

    # Update camera position
    camera_x = x - WIDTH // 2
    camera_x = max(0, min(camera_x, WORLD_WIDTH - WIDTH))  # Keep camera within bounds

    # Pickup items
    player_rect = pygame.Rect(x, y, standing_img.get_width(), standing_img.get_height())

    if keys[pygame.K_SPACE] and not collected_item:
        collected_item = check_item_pickup(player_rect, items, pickup_range=20)
        if collected_item:
            items.remove(collected_item)
    if keys[pygame.K_SPACE] and collected_item:
        print("asdf")
    # Draw background
    screen.blit(bg, (-camera_x, 0))

    # Draw items
    for item in items:
        screen.blit(item["image"], (item["x"] - camera_x, item["y"]))

    # Animation handling
    current_time = pygame.time.get_ticks()
    if current_time - last_update_time > animation_delay:
        frame = (frame + 1) % 6  # Loop through frames
        last_update_time = current_time

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

    # Update the display
    pygame.display.update()

pygame.quit()