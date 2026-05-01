import pygame
import random

# Load and scale image
def load_image(path, height):
    img = pygame.image.load(path).convert_alpha()

    w = img.get_width()
    h = img.get_height()

    new_h = height
    new_w = int(w * new_h / h)

    img = pygame.transform.smoothscale(img, (new_w, new_h))

    return img, new_w, new_h


# Create new random coin
def make_coin():
    coin_types = [
        {"value": 1, "size": 24, "color": (240, 210, 30), "weight": 70},
        {"value": 2, "size": 28, "color": (230, 230, 230), "weight": 25},
        {"value": 5, "size": 34, "color": (255, 170, 40), "weight": 5},
    ]

    coin_type = random.choices(coin_types, weights=[c["weight"] for c in coin_types])[0]
    size = coin_type["size"]

    return {
        "x": random.randint(road_x + 10, road_x + road_w - size - 10),
        "y": random.randint(-500, -100),
        "size": size,
        "value": coin_type["value"],
        "color": coin_type["color"],
    }


pygame.init()

#some presets like colors and charepter speed ans size
WIDTH = 400
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 26)

WHITE = (255, 255, 255)
GRAY = (45, 45, 45)
GREEN = (40, 150, 40)

road_x = 50
road_w = 300

player_img, player_w, player_h = load_image("player.png", 80)
obstacle_img, obstacle_w, obstacle_h = load_image("obstacle.png", 80)

player_x = WIDTH // 2 - player_w // 2
player_y = HEIGHT - player_h - 20
player_speed = 6

obstacle_x = random.randint(road_x + 10, road_x + road_w - obstacle_w - 10)
obstacle_y = -obstacle_h
obstacle_speed = 5

coin = make_coin()
coin_speed = 5
coins = 0

# Enemy becomes faster after every N collected coins
N = 5
last_speed_level = 0

line_y = 0
running = True

while running:
    clock.tick(60)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Keyboard input
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player_x > road_x + 5:
        player_x -= player_speed

    if keys[pygame.K_RIGHT] and player_x < road_x + road_w - player_w - 5:
        player_x += player_speed

    # Move road lines 
    line_y += obstacle_speed
    if line_y >= 80:
        line_y = 0

    # Move enemy
    obstacle_y += obstacle_speed
    if obstacle_y > HEIGHT:
        obstacle_y = -obstacle_h
        obstacle_x = random.randint(road_x + 10, road_x + road_w - obstacle_w - 10)

    # Move coin
    coin["y"] += coin_speed
    if coin["y"] > HEIGHT:
        coin = make_coin()

    # Hitboxes
    player_rect = pygame.Rect(
        int(player_x + player_w * 0.25),
        int(player_y + player_h * 0.10),
        int(player_w * 0.50),
        int(player_h * 0.80)
    )

    obstacle_rect = pygame.Rect(
        int(obstacle_x + obstacle_w * 0.25),
        int(obstacle_y + obstacle_h * 0.10),
        int(obstacle_w * 0.50),
        int(obstacle_h * 0.80)
    )

    coin_rect = pygame.Rect(coin["x"], coin["y"], coin["size"], coin["size"])

    # Lose if player hits enemy
    if player_rect.colliderect(obstacle_rect):
        running = False

    # Collect coin
    if player_rect.colliderect(coin_rect):
        coins += coin["value"]
        coin = make_coin()

        # Increase enemy speed 
        speed_level = coins // N
        if speed_level > last_speed_level:
            obstacle_speed += 1
            last_speed_level = speed_level

    # Draw all 
    screen.fill(GREEN)

    pygame.draw.rect(screen, GRAY, (road_x, 0, road_w, HEIGHT))
    pygame.draw.rect(screen, WHITE, (road_x, 0, 5, HEIGHT))
    pygame.draw.rect(screen, WHITE, (road_x + road_w - 5, 0, 5, HEIGHT))

    for y in range(-80, HEIGHT, 80):
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 4, y + line_y, 8, 45))

    screen.blit(player_img, (player_x, player_y))
    screen.blit(obstacle_img, (obstacle_x, obstacle_y))

    pygame.draw.ellipse(screen, coin["color"], coin_rect)
    pygame.draw.ellipse(screen, WHITE, (coin["x"] + 6, coin["y"] + 5, 6, 6))

    text = font.render("Coins: " + str(coins) + "  Speed: " + str(obstacle_speed), True, WHITE)
    screen.blit(text, (15, 15))

    pygame.display.update()

pygame.quit()
