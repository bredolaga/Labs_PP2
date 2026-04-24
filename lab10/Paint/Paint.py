import pygame

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 50, 50)
GREEN = (50, 200, 50)
BLUE = (50, 100, 220)

screen.fill(WHITE)

# modes
mode = "draw"   # draw / rect / circle / erase
color = BLACK

drawing = False
start_pos = None

while True:
    clock.tick(60)

    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # keyboard (mode + color)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                mode = "rect"
            if event.key == pygame.K_w:
                mode = "circle"
            if event.key == pygame.K_e:
                mode = "erase"
            if event.key == pygame.K_r:
                mode = "draw"
            if event.key == pygame.K_t:
                screen.fill(WHITE)

            if event.key == pygame.K_1:
                color = BLACK
            if event.key == pygame.K_2:
                color = RED
            if event.key == pygame.K_3:
                color = GREEN
            if event.key == pygame.K_4:
                color = BLUE

        # mouse down
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos

        # mouse up
        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = event.pos

            # draw rectangle
            if mode == "rect":
                rect = pygame.Rect(start_pos, (
                    end_pos[0] - start_pos[0],
                    end_pos[1] - start_pos[1]
                ))
                pygame.draw.rect(screen, color, rect, 2)

            # draw circle
            if mode == "circle":
                dx = end_pos[0] - start_pos[0]
                dy = end_pos[1] - start_pos[1]
                radius = int((dx*dx + dy*dy) ** 0.5)

                pygame.draw.circle(screen, color, start_pos, radius, 2)

    # draw / erase while moving mouse
    if drawing:
        pos = pygame.mouse.get_pos()

        if mode == "draw":
            pygame.draw.circle(screen, color, pos, 4)

        if mode == "erase":
            pygame.draw.circle(screen, WHITE, pos, 10)

    pygame.display.update()
