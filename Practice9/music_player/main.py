import pygame
import psycopg2
import random
import json
import sys

# --- Настройки ---
WIDTH, HEIGHT = 600, 600
BLOCK_SIZE = 20
FPS = 10

# Цвета
WHITE, BLACK, RED, GREEN, BLUE, DARK_RED, GRAY = (255,255,255), (0,0,0), (255,0,0), (0,255,0), (0,0,255), (139,0,0), (100,100,100)

pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Arial', 24)

# --- БАЗА ДАННЫХ (psycopg2) ---
def connect_db():
    # ВСТАВЬ СВОИ ДАННЫЕ ОТ POSTGRESQL ЗДЕСЬ
    return psycopg2.connect(dbname="your_db", user="postgres", password="password", host="localhost")

def init_db():
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS players (id SERIAL PRIMARY KEY, username VARCHAR(50) UNIQUE NOT NULL);
            CREATE TABLE IF NOT EXISTS game_sessions (
                id SERIAL PRIMARY KEY, player_id INTEGER REFERENCES players(id), 
                score INTEGER NOT NULL, level_reached INTEGER NOT NULL, played_at TIMESTAMP DEFAULT NOW()
            );
        """)
        conn.commit()
        cur.close(); conn.close()
    except Exception as e: print("Ошибка БД:", e)

def save_score(username, score, level):
    conn = connect_db()
    cur = conn.cursor()
    # Сохраняем игрока, если его нет
    cur.execute("INSERT INTO players (username) VALUES (%s) ON CONFLICT DO NOTHING RETURNING id", (username,))
    cur.execute("SELECT id FROM players WHERE username = %s", (username,))
    player_id = cur.fetchone()[0]
    # Сохраняем результат
    cur.execute("INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s)", (player_id, score, level))
    conn.commit()
    cur.close(); conn.close()

def get_top_10():
    conn = connect_db()
    cur = conn.cursor()
    # JOIN двух таблиц для лидерборда - ВАЖНО ДЛЯ ЗАЩИТЫ!
    cur.execute("""
        SELECT p.username, g.score, g.level_reached 
        FROM game_sessions g JOIN players p ON g.player_id = p.id 
        ORDER BY g.score DESC LIMIT 10
    """)
    res = cur.fetchall()
    cur.close(); conn.close()
    return res

# --- ИГРОВАЯ ЛОГИКА И СОСТОЯНИЯ ---
init_db()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 4: Advanced Snake")
clock = pygame.time.Clock()

with open('settings.json', 'r') as f:
    settings = json.load(f)

# Глобальные переменные
state = "MENU"  # Состояния: MENU, GAME, GAMEOVER, LEADERBOARD
username = ""
score, level = 0, 1

# --- Функции отрисовки ---
def draw_text(text, x, y, color=WHITE):
    screen.blit(font.render(text, True, color), (x, y))

def run_menu():
    global state, username
    screen.fill(BLACK)
    draw_text("Snake Game", 250, 100, GREEN)
    draw_text(f"Имя: {username}_", 200, 200)
    draw_text("Нажми ENTER для старта", 180, 300)
    draw_text("Нажми L для Лидерборда", 180, 350)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and username:
                state = "GAME"
            elif event.key == pygame.K_l:
                state = "LEADERBOARD"
            elif event.key == pygame.K_BACKSPACE:
                username = username[:-1]
            else:
                username += event.unicode

def run_leaderboard():
    global state
    screen.fill(BLACK)
    draw_text("TOP 10", 250, 50, GREEN)
    top = get_top_10()
    for i, row in enumerate(top):
        draw_text(f"{i+1}. {row[0]} - Score: {row[1]} (Lvl {row[2]})", 100, 100 + i*30)
    draw_text("Нажми ESC для возврата", 150, 500, RED)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            state = "MENU"

def run_game():
    global state, score, level
    snake = [(100, 100), (80, 100), (60, 100)]
    dx, dy = BLOCK_SIZE, 0
    food = (random.randint(0, (WIDTH//BLOCK_SIZE)-1) * BLOCK_SIZE, random.randint(0, (HEIGHT//BLOCK_SIZE)-1) * BLOCK_SIZE)
    poison = (-100, -100) # Яд за полем изначально
    powerup = (-100, -100)
    powerup_spawn_time = 0
    obstacles = []
    
    score = 0
    level = 1
    speed = FPS
    running = True
    
    while running:
        screen.fill(BLACK)
        if settings['grid']:
            for x in range(0, WIDTH, BLOCK_SIZE): pygame.draw.line(screen, GRAY, (x,0), (x,HEIGHT))
            for y in range(0, HEIGHT, BLOCK_SIZE): pygame.draw.line(screen, GRAY, (0,y), (WIDTH,y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and dy == 0: dx, dy = 0, -BLOCK_SIZE
                elif event.key == pygame.K_DOWN and dy == 0: dx, dy = 0, BLOCK_SIZE
                elif event.key == pygame.K_LEFT and dx == 0: dx, dy = -BLOCK_SIZE, 0
                elif event.key == pygame.K_RIGHT and dx == 0: dx, dy = BLOCK_SIZE, 0

        # Движение
        head = (snake[0][0] + dx, snake[0][1] + dy)
        snake.insert(0, head)

        # Коллизии
        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT or head in snake[1:] or head in obstacles:
            save_score(username, score, level)
            state = "GAMEOVER"
            return

        # Еда
        if head == food:
            score += 10
            if score % 30 == 0: 
                level += 1
                speed += 2
                # С 3 уровня добавляем препятствия
                if level >= 3:
                    for _ in range(5): obstacles.append((random.randint(0, (WIDTH//BLOCK_SIZE)-1) * BLOCK_SIZE, random.randint(0, (HEIGHT//BLOCK_SIZE)-1) * BLOCK_SIZE))
            
            food = (random.randint(0, (WIDTH//BLOCK_SIZE)-1) * BLOCK_SIZE, random.randint(0, (HEIGHT//BLOCK_SIZE)-1) * BLOCK_SIZE)
            # Спавн яда (с шансом)
            if random.random() > 0.5:
                poison = (random.randint(0, (WIDTH//BLOCK_SIZE)-1) * BLOCK_SIZE, random.randint(0, (HEIGHT//BLOCK_SIZE)-1) * BLOCK_SIZE)
            
            # Спавн паверапа
            if random.random() > 0.7:
                powerup = (random.randint(0, (WIDTH//BLOCK_SIZE)-1) * BLOCK_SIZE, random.randint(0, (HEIGHT//BLOCK_SIZE)-1) * BLOCK_SIZE)
                powerup_spawn_time = pygame.time.get_ticks()
        else:
            snake.pop() # Убираем хвост, если ничего не съели

        # Яд
        if head == poison:
            if len(snake) <= 2:
                save_score(username, score, level)
                state = "GAMEOVER"
                return
            snake.pop(); snake.pop() # Отнимаем 2 сегмента
            poison = (-100, -100)

        # Паверап (исчезает через 8 сек)
        current_time = pygame.time.get_ticks()
        if powerup != (-100, -100) and current_time - powerup_spawn_time > 8000:
            powerup = (-100, -100) # Пропал
        if head == powerup:
            score += 50
            powerup = (-100, -100)

        # Отрисовка
        for ob in obstacles: pygame.draw.rect(screen, GRAY, (ob[0], ob[1], BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(screen, RED, (food[0], food[1], BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(screen, DARK_RED, (poison[0], poison[1], BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(screen, BLUE, (powerup[0], powerup[1], BLOCK_SIZE, BLOCK_SIZE))
        
        for s in snake: pygame.draw.rect(screen, settings['snake_color'], (s[0], s[1], BLOCK_SIZE, BLOCK_SIZE))
        
        draw_text(f"Score: {score} Lvl: {level}", 10, 10)
        
        pygame.display.flip()
        clock.tick(speed)

def run_gameover():
    global state
    screen.fill(BLACK)
    draw_text("GAME OVER", 230, 200, RED)
    draw_text(f"Счет: {score} | Уровень: {level}", 200, 250)
    draw_text("Нажми ENTER для Рестарта", 180, 350)
    draw_text("Нажми ESC для Меню", 180, 400)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN: state = "GAME"
            elif event.key == pygame.K_ESCAPE: state = "MENU"

# --- MAIN LOOP (State Machine) ---
while True:
    if state == "MENU": run_menu()
    elif state == "GAME": run_game()
    elif state == "GAMEOVER": run_gameover()
    elif state == "LEADERBOARD": run_leaderboard()
    
    pygame.display.flip()
    clock.tick(FPS)