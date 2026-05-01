import pygame
import random
import json
import os

# Load and scale image
def load_image(path, height):
    img = pygame.image.load(path).convert_alpha()

    w = img.get_width()
    h = img.get_height()

    new_h = height
    new_w = int(w * new_h / h)

    img = pygame.transform.smoothscale(img, (new_w, new_h))

    return img, new_w, new_h


pygame.init()
pygame.mixer.init()


# Presets
WIDTH = 400
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer Extended")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)
small_font = pygame.font.SysFont("Arial", 18)

WHITE = (255, 255, 255)
GRAY = (45, 45, 45)
GREEN = (40, 150, 40)
BLACK = (0, 0, 0)
YELLOW = (240, 210, 30)
SILVER = (230, 230, 230)
ORANGE = (255, 170, 40)
RED = (220, 50, 50)
BLUE = (50, 120, 255)
PURPLE = (160, 80, 255)

road_x = 50
road_w = 300
lane_w = road_w // 3

player_img, player_w, player_h = load_image("player.png", 80)
obstacle_img, obstacle_w, obstacle_h = load_image("obstacle.png", 80)

settings_file = "settings.json"
leaderboard_file = "leaderboard.json"

SOUND_FILES = {
    "coin": "coin.wav",
    "power": "power.wav",
    "hit": "hit.wav",
    "game_over": "gameover.wav"
}


# Sound
def load_sounds():
    sounds = {}

    for name, filename in SOUND_FILES.items():
        if os.path.exists(filename):
            sounds[name] = pygame.mixer.Sound(filename)
        else:
            sounds[name] = None

    return sounds


sounds = load_sounds()


def play_sound(name):
    if settings["sound"] and sounds.get(name):
        sounds[name].play()


# Files
def load_settings():
    if os.path.exists(settings_file):
        with open(settings_file, "r") as file:
            return json.load(file)

    return {
        "difficulty": "normal",
        "car_color": "default",
        "sound": True
    }


def save_settings(settings):
    with open(settings_file, "w") as file:
        json.dump(settings, file, indent=4)


def load_leaderboard():
    if os.path.exists(leaderboard_file):
        with open(leaderboard_file, "r") as file:
            return json.load(file)

    return []


def save_score(name, score, distance):
    data = load_leaderboard()
    data.append({
        "name": name,
        "score": score,
        "distance": distance
    })

    data.sort(key=lambda x: x["score"], reverse=True)
    data = data[:10]

    with open(leaderboard_file, "w") as file:
        json.dump(data, file, indent=4)


# Random objects
def random_lane_x(width):
    lane = random.randint(0, 2)
    left = road_x + lane * lane_w
    return random.randint(left + 8, left + lane_w - width - 8)


def make_coin():
    coin_types = [
        {"value": 1, "size": 24, "color": YELLOW, "weight": 70},
        {"value": 2, "size": 28, "color": SILVER, "weight": 25},
        {"value": 5, "size": 34, "color": ORANGE, "weight": 5},
    ]

    coin_type = random.choices(coin_types, weights=[c["weight"] for c in coin_types])[0]
    size = coin_type["size"]

    return {
        "x": random_lane_x(size),
        "y": random.randint(-500, -100),
        "size": size,
        "value": coin_type["value"],
        "color": coin_type["color"],
    }


def make_car(player_x):
    x = random_lane_x(obstacle_w)

    return {
        "x": x,
        "y": random.randint(-700, -100),
        "speed": random.randint(0, 2)
    }


def make_hazard(player_x):
    x = random_lane_x(50)

    return {
        "x": x,
        "y": random.randint(-800, -150),
        "w": 50,
        "h": 25,
        "type": random.choice(["oil", "slow"])
    }


def make_powerup():
    types = ["nitro", "shield", "repair"]

    return {
        "x": random_lane_x(30),
        "y": random.randint(-900, -200),
        "size": 30,
        "type": random.choice(types)
    }


# Game state
def new_game(settings):
    if settings["difficulty"] == "easy":
        obstacle_speed = 4
        spawn_rate = 0.010
    elif settings["difficulty"] == "hard":
        obstacle_speed = 7
        spawn_rate = 0.025
    else:
        obstacle_speed = 5
        spawn_rate = 0.017

    return {
        "player_x": WIDTH // 2 - player_w // 2,
        "player_y": HEIGHT - player_h - 20,
        "player_speed": 6,
        "base_player_speed": 6,
        "obstacle_speed": obstacle_speed,
        "spawn_rate": spawn_rate,
        "coins": 0,
        "distance": 0,
        "score": 0,
        "line_y": 0,
        "coin": make_coin(),
        "cars": [],
        "hazards": [],
        "powerups": [],
        "active_power": None,
        "power_timer": 0,
        "shield": False,
        "finished": False,
        "finish_distance": 5000,
        "name_input": "",
        "saved": False
    }


settings = load_settings()
game = new_game(settings)
state = "menu"


# Drawing helpers
def draw_text(text, x, y, color=WHITE, use_small=False):
    used_font = small_font if use_small else font
    img = used_font.render(text, True, color)
    screen.blit(img, (x, y))


def draw_button(text, x, y, w, h):
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, GRAY, rect)
    pygame.draw.rect(screen, WHITE, rect, 2)
    img = font.render(text, True, WHITE)
    screen.blit(img, (x + (w - img.get_width()) // 2, y + (h - img.get_height()) // 2))
    return rect


def draw_menu():
    screen.fill(BLACK)

    draw_text("RACER EXTENDED", 95, 80)

    play = draw_button("Play", 120, 160, 160, 45)
    leaderboard = draw_button("Leaderboard", 120, 220, 160, 45)
    settings_btn = draw_button("Settings", 120, 280, 160, 45)
    quit_btn = draw_button("Quit", 120, 340, 160, 45)

    return play, leaderboard, settings_btn, quit_btn


def draw_settings():
    screen.fill(BLACK)

    draw_text("SETTINGS", 145, 70)
    draw_text("Difficulty: " + settings["difficulty"], 100, 150)
    draw_text("Sound: " + str(settings["sound"]), 100, 190)
    draw_text("Press 1 Easy, 2 Normal, 3 Hard", 55, 260, WHITE, True)
    draw_text("Press S to toggle sound", 95, 290, WHITE, True)
    draw_text("Press ESC to go back", 100, 330, WHITE, True)


def draw_leaderboard():
    screen.fill(BLACK)

    draw_text("LEADERBOARD", 120, 50)

    data = load_leaderboard()

    y = 110
    rank = 1

    if not data:
        draw_text("No scores yet", 135, 180, WHITE, True)

    for item in data:
        line = str(rank) + ". " + item["name"] + " | " + str(item["score"]) + " | " + str(item["distance"])
        draw_text(line, 45, y, WHITE, True)
        y += 30
        rank += 1

    draw_text("ESC - Back", 145, 540, WHITE, True)


def draw_road(game):
    screen.fill(GREEN)

    pygame.draw.rect(screen, GRAY, (road_x, 0, road_w, HEIGHT))
    pygame.draw.rect(screen, WHITE, (road_x, 0, 5, HEIGHT))
    pygame.draw.rect(screen, WHITE, (road_x + road_w - 5, 0, 5, HEIGHT))

    for i in range(1, 3):
        x = road_x + i * lane_w
        for y in range(-80, HEIGHT, 80):
            pygame.draw.rect(screen, WHITE, (x - 3, y + game["line_y"], 6, 40))


def draw_game(game):
    draw_road(game)

    screen.blit(player_img, (game["player_x"], game["player_y"]))

    for car in game["cars"]:
        screen.blit(obstacle_img, (car["x"], car["y"]))

    coin = game["coin"]
    coin_rect = pygame.Rect(coin["x"], coin["y"], coin["size"], coin["size"])
    pygame.draw.ellipse(screen, coin["color"], coin_rect)
    pygame.draw.ellipse(screen, WHITE, (coin["x"] + 6, coin["y"] + 5, 6, 6))

    for hazard in game["hazards"]:
        rect = pygame.Rect(hazard["x"], hazard["y"], hazard["w"], hazard["h"])

        if hazard["type"] == "oil":
            pygame.draw.ellipse(screen, BLACK, rect)
        else:
            pygame.draw.rect(screen, RED, rect)
            pygame.draw.line(screen, WHITE, (hazard["x"], hazard["y"]), (hazard["x"] + hazard["w"], hazard["y"] + hazard["h"]), 2)

    for powerup in game["powerups"]:
        rect = pygame.Rect(powerup["x"], powerup["y"], powerup["size"], powerup["size"])

        if powerup["type"] == "nitro":
            clr = BLUE
            label = "N"
        elif powerup["type"] == "shield":
            clr = PURPLE
            label = "S"
        else:
            clr = GREEN
            label = "R"

        pygame.draw.rect(screen, clr, rect)
        draw_text(label, powerup["x"] + 8, powerup["y"] + 2, WHITE, True)

    draw_text("Score: " + str(game["score"]), 10, 10, WHITE, True)
    draw_text("Coins: " + str(game["coins"]), 10, 32, WHITE, True)
    draw_text("Dist: " + str(game["distance"]), 10, 54, WHITE, True)

    if game["active_power"]:
        seconds = game["power_timer"] // 60
        draw_text(game["active_power"] + " " + str(seconds), 260, 10, WHITE, True)

    if game["shield"]:
        draw_text("Shield ON", 260, 32, WHITE, True)


def draw_game_over(game):
    screen.fill(BLACK)

    draw_text("GAME OVER", 130, 90)
    draw_text("Score: " + str(game["score"]), 135, 150)
    draw_text("Distance: " + str(game["distance"]), 120, 190)

    if not game["saved"]:
        draw_text("Enter name:", 130, 260, WHITE, True)
        draw_text(game["name_input"], 130, 290)
        draw_text("ENTER - Save", 120, 350, WHITE, True)
    else:
        draw_text("Saved", 160, 280)
        draw_text("R - Retry", 140, 340, WHITE, True)
        draw_text("M - Menu", 140, 370, WHITE, True)


# Update game
def update_game(game):
    keys = pygame.key.get_pressed()

    current_player_speed = game["player_speed"]

    if game["active_power"] == "nitro":
        current_player_speed += 4

    if keys[pygame.K_LEFT] and game["player_x"] > road_x + 5:
        game["player_x"] -= current_player_speed

    if keys[pygame.K_RIGHT] and game["player_x"] < road_x + road_w - player_w - 5:
        game["player_x"] += current_player_speed

    game["line_y"] += game["obstacle_speed"]
    if game["line_y"] >= 80:
        game["line_y"] = 0

    game["distance"] += game["obstacle_speed"]
    game["score"] = game["coins"] * 10 + game["distance"] // 10

    if game["distance"] % 900 < game["obstacle_speed"]:
        game["obstacle_speed"] += 1
        game["spawn_rate"] += 0.004

    if game["active_power"]:
        game["power_timer"] -= 1
        if game["power_timer"] <= 0:
            game["active_power"] = None

    if random.random() < game["spawn_rate"]:
        game["cars"].append(make_car(game["player_x"]))

    if random.random() < game["spawn_rate"] / 2:
        game["hazards"].append(make_hazard(game["player_x"]))

    if random.random() < 0.004:
        game["powerups"].append(make_powerup())

    game["coin"]["y"] += game["obstacle_speed"]

    if game["coin"]["y"] > HEIGHT:
        game["coin"] = make_coin()

    player_rect = pygame.Rect(
        int(game["player_x"] + player_w * 0.25),
        int(game["player_y"] + player_h * 0.10),
        int(player_w * 0.50),
        int(player_h * 0.80)
    )

    coin = game["coin"]
    coin_rect = pygame.Rect(coin["x"], coin["y"], coin["size"], coin["size"])

    if player_rect.colliderect(coin_rect):
        game["coins"] += coin["value"]
        game["coin"] = make_coin()
        play_sound("coin")

    new_cars = []

    for car in game["cars"]:
        car["y"] += game["obstacle_speed"] + car["speed"]

        car_rect = pygame.Rect(
            int(car["x"] + obstacle_w * 0.25),
            int(car["y"] + obstacle_h * 0.10),
            int(obstacle_w * 0.50),
            int(obstacle_h * 0.80)
        )

        if player_rect.colliderect(car_rect):
            if game["shield"]:
                game["shield"] = False
                play_sound("hit")
            else:
                play_sound("game_over")
                return "game_over"

        if car["y"] < HEIGHT:
            new_cars.append(car)

    game["cars"] = new_cars

    new_hazards = []

    for hazard in game["hazards"]:
        hazard["y"] += game["obstacle_speed"]
        hazard_rect = pygame.Rect(hazard["x"], hazard["y"], hazard["w"], hazard["h"])

        if player_rect.colliderect(hazard_rect):
            if hazard["type"] == "oil":
                game["player_speed"] = max(3, game["player_speed"] - 1)
            else:
                game["obstacle_speed"] = max(3, game["obstacle_speed"] - 1)
        else:
            if hazard["y"] < HEIGHT:
                new_hazards.append(hazard)

    game["hazards"] = new_hazards

    new_powerups = []

    for powerup in game["powerups"]:
        powerup["y"] += game["obstacle_speed"]
        p_rect = pygame.Rect(powerup["x"], powerup["y"], powerup["size"], powerup["size"])

        if player_rect.colliderect(p_rect):
            play_sound("power")
            if powerup["type"] == "nitro":
                game["active_power"] = "nitro"
                game["power_timer"] = 240

            elif powerup["type"] == "shield":
                game["active_power"] = "shield"
                game["power_timer"] = 600
                game["shield"] = True

            elif powerup["type"] == "repair":
                game["player_speed"] = game["base_player_speed"]
                if game["hazards"]:
                    game["hazards"].pop(0)

        else:
            if powerup["y"] < HEIGHT:
                new_powerups.append(powerup)

    game["powerups"] = new_powerups

    return "game"


running = True

while running:
    clock.tick(60)

    if state == "menu":
        buttons = draw_menu()

    elif state == "settings":
        draw_settings()

    elif state == "leaderboard":
        draw_leaderboard()

    elif state == "game":
        state = update_game(game)
        draw_game(game)

    elif state == "game_over":
        draw_game_over(game)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if state == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN:
                play, leaderboard_btn, settings_btn, quit_btn = buttons

                if play.collidepoint(event.pos):
                    game = new_game(settings)
                    state = "game"

                elif leaderboard_btn.collidepoint(event.pos):
                    state = "leaderboard"

                elif settings_btn.collidepoint(event.pos):
                    state = "settings"

                elif quit_btn.collidepoint(event.pos):
                    running = False

        elif state == "settings":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    settings["difficulty"] = "easy"
                    save_settings(settings)

                elif event.key == pygame.K_2:
                    settings["difficulty"] = "normal"
                    save_settings(settings)

                elif event.key == pygame.K_3:
                    settings["difficulty"] = "hard"
                    save_settings(settings)

                elif event.key == pygame.K_s:
                    settings["sound"] = not settings["sound"]
                    save_settings(settings)

                elif event.key == pygame.K_ESCAPE:
                    state = "menu"

        elif state == "leaderboard":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = "menu"

        elif state == "game_over":
            if event.type == pygame.KEYDOWN:
                if not game["saved"]:
                    if event.key == pygame.K_RETURN:
                        name = game["name_input"]

                        if name == "":
                            name = "Player"

                        save_score(name, game["score"], game["distance"])
                        game["saved"] = True

                    elif event.key == pygame.K_BACKSPACE:
                        game["name_input"] = game["name_input"][:-1]

                    else:
                        if len(game["name_input"]) < 12:
                            game["name_input"] += event.unicode

                else:
                    if event.key == pygame.K_r:
                        game = new_game(settings)
                        state = "game"

                    elif event.key == pygame.K_m:
                        state = "menu"

pygame.quit()
