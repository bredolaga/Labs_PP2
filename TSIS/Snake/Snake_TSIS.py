import pygame
import random
import json
import os
import psycopg2

pygame.init()
pygame.mixer.init()


WIDTH = 600
HEIGHT = 600
CELL = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Extended")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 26)
small_font = pygame.font.SysFont("Arial", 18)

BLACK = (0, 0, 0)
GREEN = (40, 180, 40)
RED = (220, 40, 40)
DARK_RED = (120, 0, 0)
YELLOW = (240, 210, 30)
BLUE = (50, 140, 240)
WHITE = (255, 255, 255)
GRAY = (80, 80, 80)
PURPLE = (160, 80, 255)

SETTINGS_FILE = "snake_settings.json"

DB_NAME = "phonebook_db"
DB_USER = "morjinka"
DB_PASSWORD = ""
DB_HOST = "localhost"
DB_PORT = "5432"

SOUND_FILES = {
    "eat": "eat.wav",
    "poison": "poison.wav",
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


# Settings
def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as file:
            return json.load(file)

    return {
        "snake_color": "green",
        "grid": True,
        "sound": True
    }


def save_settings(settings):
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=4)


settings = load_settings()


# Database
def get_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )


def create_db_tables():
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS game_sessions (
                id SERIAL PRIMARY KEY,
                player_id INTEGER REFERENCES players(id),
                score INTEGER NOT NULL,
                level INTEGER NOT NULL,
                played_at TIMESTAMP DEFAULT NOW()
            )
        """)

        conn.commit()
        cur.close()
        conn.close()

    except Exception as error:
        print("Database error:", error)


def save_result(username, score, level):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO players(username)
            VALUES (%s)
            ON CONFLICT (username) DO NOTHING
        """, (username,))

        cur.execute("SELECT id FROM players WHERE username = %s", (username,))
        player_id = cur.fetchone()[0]

        cur.execute("""
            INSERT INTO game_sessions(player_id, score, level)
            VALUES (%s, %s, %s)
        """, (player_id, score, level))

        conn.commit()
        cur.close()
        conn.close()

    except Exception as error:
        print("Database error:", error)


def load_leaderboard():
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT p.username, g.score, g.level, g.played_at
            FROM game_sessions g
            JOIN players p ON g.player_id = p.id
            ORDER BY g.score DESC
            LIMIT 10
        """)

        rows = cur.fetchall()

        cur.close()
        conn.close()

        return rows

    except Exception as error:
        print("Database error:", error)
        return []


# Helpers
def snake_color():
    if settings["snake_color"] == "blue":
        return BLUE
    if settings["snake_color"] == "yellow":
        return YELLOW
    return GREEN


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


def random_cell():
    x = random.randrange(CELL, WIDTH - CELL, CELL)
    y = random.randrange(CELL, HEIGHT - CELL, CELL)
    return [x, y]


def free_cell(game):
    while True:
        pos = random_cell()

        if pos not in game["snake"] and pos not in game["obstacles"]:
            if game["food"] is None or pos != game["food"]["pos"]:
                if game["poison"] is None or pos != game["poison"]["pos"]:
                    if game["powerup"] is None or pos != game["powerup"]["pos"]:
                        return pos


def make_food(game):
    food_types = [
        {"value": 1, "color": RED, "weight": 65},
        {"value": 2, "color": YELLOW, "weight": 25},
        {"value": 3, "color": BLUE, "weight": 10},
    ]

    food_type = random.choices(food_types, weights=[f["weight"] for f in food_types])[0]

    return {
        "pos": free_cell(game),
        "value": food_type["value"],
        "color": food_type["color"],
        "spawn_time": pygame.time.get_ticks(),
        "lifetime": 5000
    }


def make_poison(game):
    return {
        "pos": free_cell(game),
        "spawn_time": pygame.time.get_ticks(),
        "lifetime": 7000
    }


def make_powerup(game):
    return {
        "pos": free_cell(game),
        "type": random.choice(["speed", "slow", "shield"]),
        "spawn_time": pygame.time.get_ticks(),
        "lifetime": 8000
    }


def make_obstacles(game):
    result = []

    if game["level"] < 3:
        return result

    count = game["level"]

    while len(result) < count:
        pos = random_cell()

        if pos not in game["snake"] and pos not in result:
            result.append(pos)

    return result


def new_game(username):
    game = {
        "username": username,
        "snake": [[300, 300]],
        "dx": CELL,
        "dy": 0,
        "score": 0,
        "level": 1,
        "speed": 8,
        "base_speed": 8,
        "food": None,
        "poison": None,
        "powerup": None,
        "active_power": None,
        "power_end": 0,
        "shield": False,
        "obstacles": [],
        "saved": False
    }

    game["food"] = make_food(game)

    return game


# Screens
def draw_menu(username):
    screen.fill(BLACK)

    draw_text("SNAKE EXTENDED", 185, 80)
    draw_text("Username: " + username, 190, 125, WHITE, True)
    draw_text("Type name before Play", 200, 150, WHITE, True)

    play = draw_button("Play", 220, 200, 160, 45)
    leaderboard = draw_button("Leaderboard", 220, 260, 160, 45)
    settings_btn = draw_button("Settings", 220, 320, 160, 45)
    quit_btn = draw_button("Quit", 220, 380, 160, 45)

    return play, leaderboard, settings_btn, quit_btn


def draw_settings():
    screen.fill(BLACK)

    draw_text("SETTINGS", 230, 70)
    draw_text("Snake color: " + settings["snake_color"], 170, 150)
    draw_text("Grid: " + str(settings["grid"]), 170, 190)
    draw_text("Sound: " + str(settings["sound"]), 170, 230)

    draw_text("1 Green | 2 Blue | 3 Yellow", 160, 300, WHITE, True)
    draw_text("G toggle grid", 225, 330, WHITE, True)
    draw_text("S toggle sound", 220, 360, WHITE, True)
    draw_text("ESC back", 250, 410, WHITE, True)


def draw_leaderboard():
    screen.fill(BLACK)

    draw_text("LEADERBOARD", 210, 50)

    rows = load_leaderboard()
    y = 105

    if not rows:
        draw_text("No scores yet or database is not connected", 145, 200, WHITE, True)

    rank = 1

    for username, score, level, played_at in rows:
        line = str(rank) + ". " + username + " | score " + str(score) + " | level " + str(level)
        draw_text(line, 90, y, WHITE, True)
        y += 28
        rank += 1

    draw_text("ESC back", 250, 540, WHITE, True)


def draw_game(game):
    screen.fill(BLACK)

    if settings["grid"]:
        for x in range(0, WIDTH, CELL):
            pygame.draw.line(screen, (25, 25, 25), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL):
            pygame.draw.line(screen, (25, 25, 25), (0, y), (WIDTH, y))

    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, CELL))
    pygame.draw.rect(screen, GRAY, (0, HEIGHT - CELL, WIDTH, CELL))
    pygame.draw.rect(screen, GRAY, (0, 0, CELL, HEIGHT))
    pygame.draw.rect(screen, GRAY, (WIDTH - CELL, 0, CELL, HEIGHT))

    for obstacle in game["obstacles"]:
        pygame.draw.rect(screen, GRAY, (obstacle[0], obstacle[1], CELL, CELL))

    if game["food"]:
        food = game["food"]
        pygame.draw.rect(screen, food["color"], (food["pos"][0], food["pos"][1], CELL, CELL))

    if game["poison"]:
        poison = game["poison"]
        pygame.draw.rect(screen, DARK_RED, (poison["pos"][0], poison["pos"][1], CELL, CELL))

    if game["powerup"]:
        powerup = game["powerup"]

        if powerup["type"] == "speed":
            color = BLUE
            label = "+"
        elif powerup["type"] == "slow":
            color = YELLOW
            label = "-"
        else:
            color = PURPLE
            label = "S"

        pygame.draw.rect(screen, color, (powerup["pos"][0], powerup["pos"][1], CELL, CELL))
        draw_text(label, powerup["pos"][0] + 4, powerup["pos"][1] - 3, WHITE, True)

    for part in game["snake"]:
        pygame.draw.rect(screen, snake_color(), (part[0], part[1], CELL, CELL))

    text = "Score: " + str(game["score"]) + "  Level: " + str(game["level"])
    draw_text(text, 30, 25, WHITE, True)

    if game["food"]:
        time_left = max(0, (game["food"]["lifetime"] - (pygame.time.get_ticks() - game["food"]["spawn_time"])) // 1000 + 1)
        draw_text("Food: " + str(time_left), 30, 45, WHITE, True)

    if game["active_power"]:
        left = max(0, (game["power_end"] - pygame.time.get_ticks()) // 1000 + 1)
        draw_text("Power: " + game["active_power"] + " " + str(left), 400, 25, WHITE, True)

    if game["shield"]:
        draw_text("Shield ON", 400, 45, WHITE, True)


def draw_game_over(game):
    screen.fill(BLACK)

    draw_text("GAME OVER", 220, 100)
    draw_text("Score: " + str(game["score"]), 235, 170)
    draw_text("Level: " + str(game["level"]), 240, 210)

    if not game["saved"]:
        draw_text("Saving result...", 215, 280)
        save_result(game["username"], game["score"], game["level"])
        game["saved"] = True

    draw_text("R retry", 240, 350, WHITE, True)
    draw_text("M menu", 240, 380, WHITE, True)


# Game update
def update_power(game):
    now = pygame.time.get_ticks()

    if game["active_power"] and now >= game["power_end"]:
        if game["active_power"] == "speed" or game["active_power"] == "slow":
            game["speed"] = game["base_speed"] + (game["level"] - 1) * 2

        game["active_power"] = None


def update_spawns(game):
    now = pygame.time.get_ticks()

    if now - game["food"]["spawn_time"] > game["food"]["lifetime"]:
        game["food"] = make_food(game)

    if game["poison"] is None and random.random() < 0.006:
        game["poison"] = make_poison(game)

    if game["poison"] and now - game["poison"]["spawn_time"] > game["poison"]["lifetime"]:
        game["poison"] = None

    if game["powerup"] is None and random.random() < 0.006:
        game["powerup"] = make_powerup(game)

    if game["powerup"] and now - game["powerup"]["spawn_time"] > game["powerup"]["lifetime"]:
        game["powerup"] = None


def update_game(game):
    update_power(game)
    update_spawns(game)

    head = game["snake"][0]
    new_head = [head[0] + game["dx"], head[1] + game["dy"]]

    if new_head[0] <= 0 or new_head[0] >= WIDTH - CELL:
        play_sound("game_over")
        return "game_over"

    if new_head[1] <= 0 or new_head[1] >= HEIGHT - CELL:
        play_sound("game_over")
        return "game_over"

    if new_head in game["obstacles"]:
        play_sound("game_over")
        return "game_over"

    if new_head in game["snake"]:
        if game["shield"]:
            game["shield"] = False
            play_sound("hit")
        else:
            play_sound("game_over")
            return "game_over"

    game["snake"].insert(0, new_head)

    ate_food = False

    if game["food"] and new_head == game["food"]["pos"]:
        game["score"] += game["food"]["value"]
        ate_food = True
        game["food"] = make_food(game)
        play_sound("eat")

        new_level = game["score"] // 3 + 1

        if new_level > game["level"]:
            game["level"] = new_level
            game["base_speed"] = 8 + (game["level"] - 1) * 2
            game["speed"] = game["base_speed"]
            game["obstacles"] = make_obstacles(game)

    if game["poison"] and new_head == game["poison"]["pos"]:
        game["poison"] = None
        play_sound("poison")

        for i in range(2):
            if len(game["snake"]) > 1:
                game["snake"].pop()

        if len(game["snake"]) <= 1:
            play_sound("game_over")
            return "game_over"

    if game["powerup"] and new_head == game["powerup"]["pos"]:
        play_sound("power")
        power_type = game["powerup"]["type"]
        game["powerup"] = None
        game["active_power"] = power_type
        game["power_end"] = pygame.time.get_ticks() + 5000

        if power_type == "speed":
            game["speed"] += 4
        elif power_type == "slow":
            game["speed"] = max(5, game["speed"] - 3)
        elif power_type == "shield":
            game["shield"] = True
            game["power_end"] = pygame.time.get_ticks() + 20000

    if not ate_food:
        game["snake"].pop()

    return "game"


create_db_tables()

username = ""
game = None
state = "menu"
running = True

while running:
    if state == "game":
        clock.tick(game["speed"])
    else:
        clock.tick(60)

    if state == "menu":
        buttons = draw_menu(username)

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif event.key == pygame.K_RETURN:
                    if username == "":
                        username = "Player"
                    game = new_game(username)
                    state = "game"
                else:
                    if len(username) < 12:
                        username += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                play, leaderboard_btn, settings_btn, quit_btn = buttons

                if play.collidepoint(event.pos):
                    if username == "":
                        username = "Player"

                    game = new_game(username)
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
                    settings["snake_color"] = "green"
                    save_settings(settings)

                elif event.key == pygame.K_2:
                    settings["snake_color"] = "blue"
                    save_settings(settings)

                elif event.key == pygame.K_3:
                    settings["snake_color"] = "yellow"
                    save_settings(settings)

                elif event.key == pygame.K_g:
                    settings["grid"] = not settings["grid"]
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

        elif state == "game":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and game["dx"] != CELL:
                    game["dx"] = -CELL
                    game["dy"] = 0

                elif event.key == pygame.K_RIGHT and game["dx"] != -CELL:
                    game["dx"] = CELL
                    game["dy"] = 0

                elif event.key == pygame.K_UP and game["dy"] != CELL:
                    game["dx"] = 0
                    game["dy"] = -CELL

                elif event.key == pygame.K_DOWN and game["dy"] != -CELL:
                    game["dx"] = 0
                    game["dy"] = CELL

        elif state == "game_over":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game = new_game(username)
                    state = "game"

                elif event.key == pygame.K_m:
                    state = "menu"

pygame.quit()
