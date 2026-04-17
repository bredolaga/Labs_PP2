import pygame
import datetime

pygame.init()

WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

center = (WIDTH // 2, HEIGHT // 2)

clockface = pygame.image.load("clock face.png").convert_alpha()
arrow = pygame.image.load("arrow.png").convert_alpha()

clockface = pygame.transform.scale(clockface, (600, 600))

hour_img = pygame.transform.scale(arrow, (200, 200))
minute_img = pygame.transform.scale(arrow, (250, 250))
second_img = pygame.transform.scale(arrow, (300, 300))


def draw(image, angle):
    rotated = pygame.transform.rotate(image, angle)
    rect = rotated.get_rect(center=center)
    screen.blit(rotated, rect)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    now = datetime.datetime.now()

    sec = now.second + now.microsecond / 1_000_000
    minute = now.minute + sec / 60
    hour = (now.hour % 12) + minute / 60

    sec_angle = -sec * 6
    min_angle = -minute * 6
    hour_angle = -hour * 30

    screen.fill((255, 255, 255))

    screen.blit(clockface, clockface.get_rect(center=center))

    draw(hour_img, hour_angle)
    draw(minute_img, min_angle)
    draw(second_img, sec_angle)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
