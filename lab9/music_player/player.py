import pygame
import os

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 40)
small_font = pygame.font.Font(None, 30)

music_folder = "music"
playlist = []

for file in os.listdir(music_folder):
    if file.endswith(".flac") or file.endswith(".wav"):
        playlist.append(file)

playlist.sort()

current_index = 0
is_playing = False

def load_track():
    if playlist:
        path = os.path.join(music_folder, playlist[current_index])
        pygame.mixer.music.load(path)

def play_track():
    global is_playing
    if playlist:
        load_track()
        pygame.mixer.music.play()
        is_playing = True

def stop_track():
    global is_playing
    pygame.mixer.music.stop()
    is_playing = False

def next_track():
    global current_index
    if playlist:
        current_index = (current_index + 1) % len(playlist)
        play_track()

def previous_track():
    global current_index
    if playlist:
        current_index = (current_index - 1) % len(playlist)
        play_track()

if playlist:
    load_track()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                play_track()
            elif event.key == pygame.K_s:
                stop_track()
            elif event.key == pygame.K_n:
                next_track()
            elif event.key == pygame.K_b:
                previous_track()
            elif event.key == pygame.K_q:
                running = False

    screen.fill((20, 20, 30))

    title = font.render("Music Player", True, (255, 255, 255))
    screen.blit(title, (30, 30))

    if playlist:
        track_text = small_font.render(f"Current track: {playlist[current_index]}", True, (200, 200, 200))
        screen.blit(track_text, (30, 100))

        status = "Playing" if is_playing else "Stopped"
        status_text = small_font.render(f"Status: {status}", True, (200, 200, 200))
        screen.blit(status_text, (30, 150))

        control_text = small_font.render("P - Play | S - Stop | N - Next | B - Previous | Q - Quit", True, (180, 180, 180))
        screen.blit(control_text, (30, 250))
    else:
        no_music = small_font.render("No music files found in music folder", True, (255, 100, 100))
        screen.blit(no_music, (30, 100))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
