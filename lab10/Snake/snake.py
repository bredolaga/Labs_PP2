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
WHITE = (255, 255, 255)
GRAY = (80, 80, 80)

snake = [[300, 300]]
dx = CELL
dy = 0

score = 0
level = 1
speed = 8

def make_food():
    while True:
        x = random.randrange(CELL, WIDTH - CELL, CELL)
        y = random.randrange(CELL, HEIGHT - CELL, CELL)

        if [x, y] not in snake:
            return [x, y]

food = make_food()

running = True

while running:
    clock.tick(speed)

    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # keyboard control
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

    # create new head
    head = snake[0]
    new_head = [head[0] + dx, head[1] + dy]

    # wall collision
    if new_head[0] <= 0 or new_head[0] >= WIDTH - CELL:
        running = False

    if new_head[1] <= 0 or new_head[1] >= HEIGHT - CELL:
        running = False

    # snake collision
    if new_head in snake:
        running = False

    # move snake
    snake.insert(0, new_head)

    # food collision
    if new_head == food:
        score += 1

        # every 3 foods level increases
        if score % 3 == 0:
            level += 1
            speed += 2

        food = make_food()
    else:
        snake.pop()

    # draw background
    screen.fill(BLACK)

    # draw wall
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, CELL))
    pygame.draw.rect(screen, GRAY, (0, HEIGHT - CELL, WIDTH, CELL))
    pygame.draw.rect(screen, GRAY, (0, 0, CELL, HEIGHT))
    pygame.draw.rect(screen, GRAY, (WIDTH - CELL, 0, CELL, HEIGHT))

    # draw food
    pygame.draw.rect(screen, RED, (food[0], food[1], CELL, CELL))

    # draw snake
    for part in snake:
        pygame.draw.rect(screen, GREEN, (part[0], part[1], CELL, CELL))

    # draw score and level
    text = font.render("Score: " + str(score) + "  Level: " + str(level), True, WHITE)
    screen.blit(text, (30, 25))

    pygame.display.update()

pygame.quit()
