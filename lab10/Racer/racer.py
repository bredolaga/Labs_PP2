import pygame
import random

# load image
def load_image(path, height):
    img = pygame.image.load(path).convert_alpha()

    w = img.get_width()
    h = img.get_height()

    new_h = height
    new_w = int(w * new_h / h)

    img = pygame.transform.smoothscale(img, (new_w, new_h))

    return img, new_w, new_h


pygame.init()

WIDTH = 400
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 26)

WHITE = (255, 255, 255)
GRAY = (45, 45, 45)
GREEN = (40, 150, 40)
YELLOW = (240, 210, 30)

road_x = 50
road_w = 300

# load assets
player_img, player_w, player_h = load_image("player.png", 80)
obstacle_img, obstacle_w, obstacle_h = load_image("obstacle.png", 80)

# initial state
player_x = WIDTH // 2 - player_w // 2
player_y = HEIGHT - player_h - 20
player_speed = 6

obstacle_x = random.randint(road_x + 10, road_x + road_w - obstacle_w - 10)
obstacle_y = -obstacle_h
obstacle_speed = 5

coin_size = 25
coin_x = random.randint(road_x + 10, road_x + road_w - coin_size - 10)
coin_y = random.randint(-500, -100)
coin_speed = 5

coins = 0
line_y = 0
running = True

while running:
    clock.tick(60)

    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # input
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player_x > road_x + 5:
        player_x -= player_speed

    if keys[pygame.K_RIGHT] and player_x < road_x + road_w - player_w - 5:
        player_x += player_speed

    # update
    line_y += obstacle_speed
    if line_y >= 80:
        line_y = 0

    obstacle_y += obstacle_speed
    if obstacle_y > HEIGHT:
        obstacle_y = -obstacle_h
        obstacle_x = random.randint(road_x + 10, road_x + road_w - obstacle_w - 10)

    coin_y += coin_speed
    if coin_y > HEIGHT:
        coin_y = random.randint(-500, -100)
        coin_x = random.randint(road_x + 10, road_x + road_w - coin_size - 10)

    # collision
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

    coin_rect = pygame.Rect(coin_x, coin_y, coin_size, coin_size)

    if player_rect.colliderect(obstacle_rect):
        running = False

    if player_rect.colliderect(coin_rect):
        coins += 1
        coin_y = random.randint(-500, -100)
        coin_x = random.randint(road_x + 10, road_x + road_w - coin_size - 10)

    # draw
    screen.fill(GREEN)

    pygame.draw.rect(screen, GRAY, (road_x, 0, road_w, HEIGHT))

    pygame.draw.rect(screen, WHITE, (road_x, 0, 5, HEIGHT))
    pygame.draw.rect(screen, WHITE, (road_x + road_w - 5, 0, 5, HEIGHT))

    for y in range(-80, HEIGHT, 80):
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 4, y + line_y, 8, 45))

    screen.blit(player_img, (player_x, player_y))
    screen.blit(obstacle_img, (obstacle_x, obstacle_y))

    pygame.draw.ellipse(screen, YELLOW, coin_rect)
    pygame.draw.ellipse(screen, WHITE, (coin_x + 6, coin_y + 5, 6, 6))

    text = font.render("Coins: " + str(coins), True, WHITE)
    screen.blit(text, (WIDTH - text.get_width() - 15, 15))

    pygame.display.update()

pygame.quit()
