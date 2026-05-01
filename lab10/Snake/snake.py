import pygame
import random

pygame.init()

WIDTH = 600
HEIGHT = 600
CELL = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 26)

BLACK = (0, 0, 0)
GREEN = (40, 180, 40)
RED = (220, 40, 40)
YELLOW = (240, 210, 30)
BLUE = (50, 140, 240)
WHITE = (255, 255, 255)
GRAY = (80, 80, 80)

snake = [[300, 300]]
dx = CELL
dy = 0

score = 0
level = 1
speed = 8

# Food live time)
FOOD_LIFETIME = 5000


def make_food():
    # Different food types
    food_types = [
        {"value": 1, "color": RED, "weight": 70},
        {"value": 2, "color": YELLOW, "weight": 25},
        {"value": 3, "color": BLUE, "weight": 5},
    ]

    food_type = random.choices(food_types, weights=[f["weight"] for f in food_types])[0]

    # Choose a free cell that is not inside the snake
    while True:
        x = random.randrange(CELL, WIDTH - CELL, CELL)
        y = random.randrange(CELL, HEIGHT - CELL, CELL)

        if [x, y] not in snake:
            return {
                "pos": [x, y],
                "value": food_type["value"],
                "color": food_type["color"],
                "spawn_time": pygame.time.get_ticks(),
            }


food = make_food()
running = True

while running:
    clock.tick(speed)

    # Events.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Keyboard control
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and dx != CELL:
                dx = -CELL
                dy = 0

            if event.key == pygame.K_RIGHT and dx != -CELL:
                dx = CELL
                dy = 0

            if event.key == pygame.K_UP and dy != CELL:
                dx = 0
                dy = -CELL

            if event.key == pygame.K_DOWN and dy != -CELL:
                dx = 0
                dy = CELL

    # If food is too old replace it with new random food
    current_time = pygame.time.get_ticks()
    if current_time - food["spawn_time"] > FOOD_LIFETIME:
        food = make_food()

    # Create new head
    head = snake[0]
    new_head = [head[0] + dx, head[1] + dy]

    # Wall collision
    if new_head[0] <= 0 or new_head[0] >= WIDTH - CELL:
        running = False

    if new_head[1] <= 0 or new_head[1] >= HEIGHT - CELL:
        running = False

    # Snake collision
    if new_head in snake:
        running = False

    # Move snake
    snake.insert(0, new_head)

    # Food collision
    if new_head == food["pos"]:
        score += food["value"]

        # Every 3 points level increases
        if score // 3 + 1 > level:
            level = score // 3 + 1
            speed += 2

        food = make_food()
    else:
        snake.pop()

    # Draw all
    screen.fill(BLACK)

    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, CELL))
    pygame.draw.rect(screen, GRAY, (0, HEIGHT - CELL, WIDTH, CELL))
    pygame.draw.rect(screen, GRAY, (0, 0, CELL, HEIGHT))
    pygame.draw.rect(screen, GRAY, (WIDTH - CELL, 0, CELL, HEIGHT))

    pygame.draw.rect(screen, food["color"], (food["pos"][0], food["pos"][1], CELL, CELL))

    for part in snake:
        pygame.draw.rect(screen, GREEN, (part[0], part[1], CELL, CELL))

    #Timer
    time_left = max(0, (FOOD_LIFETIME - (pygame.time.get_ticks() - food["spawn_time"])) // 1000 + 1)
    text = font.render("Score: " + str(score) + "  Level: " + str(level) + "  Food: " + str(time_left), True, WHITE)
    screen.blit(text, (30, 25))

    pygame.display.update()

pygame.quit()
