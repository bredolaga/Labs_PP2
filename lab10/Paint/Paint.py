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

# Current drawing mode.
# r - free drawing, e - eraser, q - rectangle, w - circle,
# a - square, s - right triangle, d - equilateral triangle, f - rhombus.
mode = "draw"
color = BLACK

drawing = False
start_pos = None


def make_rect(start, end):
    # Rect with positive width and height
    x1, y1 = start
    x2, y2 = end
    return pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))


def draw_square(surface, clr, start, end):
    # Square side
    x1, y1 = start
    x2, y2 = end
    side = min(abs(x2 - x1), abs(y2 - y1))

    if x2 < x1:
        side = -side
    if y2 < y1:
        rect = pygame.Rect(x1, y1 - abs(side), side, abs(side))
    else:
        rect = pygame.Rect(x1, y1, side, side)

    pygame.draw.rect(surface, clr, rect, 2)


def draw_right_triangle(surface, clr, start, end):
    # Right triangle is built inside the rectangle between start and end points
    x1, y1 = start
    x2, y2 = end
    points = [(x1, y1), (x1, y2), (x2, y2)]
    pygame.draw.polygon(surface, clr, points, 2)


def draw_equilateral_triangle(surface, clr, start, end):
    # Equilateral triangle: all sides are approximately equal
    x1, y1 = start
    x2, y2 = end
    side = abs(x2 - x1)
    height = int(side * (3 ** 0.5) / 2)

    if x2 < x1:
        left = x1 - side
        right = x1
    else:
        left = x1
        right = x1 + side

    if y2 < y1:
        top = y1 - height
        bottom = y1
    else:
        top = y1
        bottom = y1 + height

    points = [(left, bottom), (right, bottom), ((left + right) // 2, top)]
    pygame.draw.polygon(surface, clr, points, 2)


def draw_rhombus(surface, clr, start, end):
    # Rhombus is drawn by four points: top right bottom left
    rect = make_rect(start, end)
    cx = rect.centerx
    cy = rect.centery
    points = [
        (cx, rect.top),
        (rect.right, cy),
        (cx, rect.bottom),
        (rect.left, cy),
    ]
    pygame.draw.polygon(surface, clr, points, 2)


while True:
    clock.tick(60)

    # Events.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        #inputs
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                mode = "rect"
            if event.key == pygame.K_w:
                mode = "circle"
            if event.key == pygame.K_e:
                mode = "erase"
            if event.key == pygame.K_r:
                mode = "draw"
            if event.key == pygame.K_a:
                mode = "square"
            if event.key == pygame.K_s:
                mode = "right_triangle"
            if event.key == pygame.K_d:
                mode = "equilateral_triangle"
            if event.key == pygame.K_f:
                mode = "rhombus"
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

        # drowing
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos

        # shape
        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = event.pos

            if mode == "rect":
                pygame.draw.rect(screen, color, make_rect(start_pos, end_pos), 2)

            if mode == "circle":
                dx = end_pos[0] - start_pos[0]
                dy = end_pos[1] - start_pos[1]
                radius = int((dx * dx + dy * dy) ** 0.5)
                pygame.draw.circle(screen, color, start_pos, radius, 2)

            if mode == "square":
                draw_square(screen, color, start_pos, end_pos)

            if mode == "right_triangle":
                draw_right_triangle(screen, color, start_pos, end_pos)

            if mode == "equilateral_triangle":
                draw_equilateral_triangle(screen, color, start_pos, end_pos)

            if mode == "rhombus":
                draw_rhombus(screen, color, start_pos, end_pos)

    if drawing:
        pos = pygame.mouse.get_pos()

        if mode == "draw":
            pygame.draw.circle(screen, color, pos, 4)

        if mode == "erase":
            pygame.draw.circle(screen, WHITE, pos, 10)

    pygame.display.update()
