import pygame
import datetime

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 50, 50)
GREEN = (50, 200, 50)
BLUE = (50, 100, 220)

# Canvas (stores final drawing)
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)

# Current drawing mode
mode = "draw"

# Current color and brush size
color = BLACK
brush_size = 2

# Drawing state
drawing = False
start_pos = None
prev_pos = None

# Text tool state
text_active = False
text_value = ""
text_pos = (0, 0)


def make_rect(start, end):
    # Rect with positive width and height
    x1, y1 = start
    x2, y2 = end
    return pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))


def draw_square(surface, clr, start, end, width):
    # Square with equal sides
    x1, y1 = start
    x2, y2 = end

    side = min(abs(x2 - x1), abs(y2 - y1))

    if x2 < x1:
        x = x1 - side
    else:
        x = x1

    if y2 < y1:
        y = y1 - side
    else:
        y = y1

    pygame.draw.rect(surface, clr, (x, y, side, side), width)


def draw_right_triangle(surface, clr, start, end, width):
    # Right triangle inside bounding rectangle
    x1, y1 = start
    x2, y2 = end

    points = [(x1, y1), (x1, y2), (x2, y2)]
    pygame.draw.polygon(surface, clr, points, width)


def draw_equilateral_triangle(surface, clr, start, end, width):
    # Equilateral triangle (approximate)
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
        bottom = y1
        top = y1 - height
    else:
        top = y1
        bottom = y1 + height

    points = [
        (left, bottom),
        (right, bottom),
        ((left + right) // 2, top)
    ]

    pygame.draw.polygon(surface, clr, points, width)


def draw_rhombus(surface, clr, start, end, width):
    # Rhombus using rectangle center
    rect = make_rect(start, end)

    cx = rect.centerx
    cy = rect.centery

    points = [
        (cx, rect.top),
        (rect.right, cy),
        (cx, rect.bottom),
        (rect.left, cy)
    ]

    pygame.draw.polygon(surface, clr, points, width)


def draw_shape(surface, shape_mode, clr, start, end, width):
    # Universal shape dispatcher
    if shape_mode == "line":
        pygame.draw.line(surface, clr, start, end, width)

    elif shape_mode == "rect":
        pygame.draw.rect(surface, clr, make_rect(start, end), width)

    elif shape_mode == "circle":
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        radius = int((dx * dx + dy * dy) ** 0.5)
        pygame.draw.circle(surface, clr, start, radius, width)

    elif shape_mode == "square":
        draw_square(surface, clr, start, end, width)

    elif shape_mode == "right_triangle":
        draw_right_triangle(surface, clr, start, end, width)

    elif shape_mode == "equilateral_triangle":
        draw_equilateral_triangle(surface, clr, start, end, width)

    elif shape_mode == "rhombus":
        draw_rhombus(surface, clr, start, end, width)


def flood_fill(surface, x, y, new_color):
    # Flood fill using stack (DFS)
    target_color = surface.get_at((x, y))
    if target_color == new_color:
        return

    stack = [(x, y)]

    while stack:
        px, py = stack.pop()

        if px < 0 or px >= WIDTH or py < 0 or py >= HEIGHT:
            continue

        if surface.get_at((px, py)) != target_color:
            continue

        surface.set_at((px, py), new_color)

        stack.append((px + 1, py))
        stack.append((px - 1, py))
        stack.append((px, py + 1))
        stack.append((px, py - 1))


# Main loop
running = True

while running:
    clock.tick(60)

    # Draw canvas
    screen.blit(canvas, (0, 0))

    # Preview shapes
    if drawing and start_pos:
        current_pos = pygame.mouse.get_pos()

        if mode in ["line", "rect", "circle", "square",
                    "right_triangle", "equilateral_triangle", "rhombus"]:
            draw_shape(screen, mode, color, start_pos, current_pos, brush_size)

    # Preview text
    if text_active:
        txt = font.render(text_value, True, color)
        screen.blit(txt, text_pos)

    pygame.display.update()

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Keyboard input
        if event.type == pygame.KEYDOWN:

            if text_active:
                if event.key == pygame.K_RETURN:
                    txt = font.render(text_value, True, color)
                    canvas.blit(txt, text_pos)
                    text_active = False
                    text_value = ""

                elif event.key == pygame.K_ESCAPE:
                    text_active = False
                    text_value = ""

                elif event.key == pygame.K_BACKSPACE:
                    text_value = text_value[:-1]

                else:
                    text_value += event.unicode

            else:
                # Mode switching
                if event.key == pygame.K_r: mode = "draw"
                if event.key == pygame.K_e: mode = "erase"
                if event.key == pygame.K_l: mode = "line"
                if event.key == pygame.K_q: mode = "rect"
                if event.key == pygame.K_w: mode = "circle"
                if event.key == pygame.K_a: mode = "square"
                if event.key == pygame.K_s: mode = "right_triangle"
                if event.key == pygame.K_d: mode = "equilateral_triangle"
                if event.key == pygame.K_f: mode = "rhombus"
                if event.key == pygame.K_g: mode = "fill"
                if event.key == pygame.K_x: mode = "text"

                # Clear canvas
                if event.key == pygame.K_t:
                    canvas.fill(WHITE)

                # Brush size
                if event.key == pygame.K_1: brush_size = 2
                if event.key == pygame.K_2: brush_size = 5
                if event.key == pygame.K_3: brush_size = 10

                # Colors
                if event.key == pygame.K_4: color = BLACK
                if event.key == pygame.K_5: color = RED
                if event.key == pygame.K_6: color = GREEN
                if event.key == pygame.K_7: color = BLUE

                # Save image
                if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    filename = datetime.datetime.now().strftime("paint_%Y%m%d_%H%M%S.png")
                    pygame.image.save(canvas, filename)

        # Mouse down
        if event.type == pygame.MOUSEBUTTONDOWN:

            if mode == "fill":
                flood_fill(canvas, event.pos[0], event.pos[1], color)

            elif mode == "text":
                text_active = True
                text_value = ""
                text_pos = event.pos

            else:
                drawing = True
                start_pos = event.pos
                prev_pos = event.pos

        # Mouse move
        if event.type == pygame.MOUSEMOTION and drawing:
            pos = event.pos

            if mode == "draw":
                pygame.draw.line(canvas, color, prev_pos, pos, brush_size)
                prev_pos = pos

            elif mode == "erase":
                pygame.draw.line(canvas, WHITE, prev_pos, pos, brush_size * 2)
                prev_pos = pos

        # Mouse up
        if event.type == pygame.MOUSEBUTTONUP and drawing:
            end_pos = event.pos

            if mode in ["line", "rect", "circle", "square",
                        "right_triangle", "equilateral_triangle", "rhombus"]:
                draw_shape(canvas, mode, color, start_pos, end_pos, brush_size)

            drawing = False
            start_pos = None
            prev_pos = None

pygame.quit()
