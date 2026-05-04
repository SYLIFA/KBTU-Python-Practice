import pygame
import random
import time
import json
import os

# --- НАСТРОЙКИ ---
WIDTH, HEIGHT = 800, 600
BLOCK_SIZE = 20
WHITE, BLACK, RED, GREEN, YELLOW, BLUE = (255,255,255), (0,0,0), (255,0,0), (0,255,0), (255,255,0), (0,0,255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("KBTU Snake: Level Up Edition")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 20)

class Food:
    def __init__(self):
        self.spawn()

    def spawn(self):
        # 80% обычная (1 очко), 20% золотая (5 очков)
        self.weight = random.choices([1, 5], weights=[80, 20])[0]
        self.color = YELLOW if self.weight == 5 else RED
        self.pos = [random.randrange(1, (WIDTH//BLOCK_SIZE)) * BLOCK_SIZE,
                    random.randrange(1, (HEIGHT//BLOCK_SIZE)) * BLOCK_SIZE]
        self.timer = time.time() + 7 if self.weight == 5 else None # Золотая исчезнет через 7 сек

    def draw(self):
        # Если золотая еда просрочена, спавним новую
        if self.timer and time.time() > self.timer:
            self.spawn()
        pygame.draw.rect(screen, self.color, (self.pos[0], self.pos[1], BLOCK_SIZE, BLOCK_SIZE))

class Snake:
    def __init__(self):
        self.pos = [100, 60]
        self.body = [[100, 60], [80, 60], [60, 60]]
        self.dir = "RIGHT"
        self.speed = 10

    def move(self, new_dir):
        if new_dir == "UP" and self.dir != "DOWN": self.dir = "UP"
        if new_dir == "DOWN" and self.dir != "UP": self.dir = "DOWN"
        if new_dir == "LEFT" and self.dir != "RIGHT": self.dir = "LEFT"
        if new_dir == "RIGHT" and self.dir != "LEFT": self.dir = "RIGHT"

        if self.dir == "UP": self.pos[1] -= BLOCK_SIZE
        if self.dir == "DOWN": self.pos[1] += BLOCK_SIZE
        if self.dir == "LEFT": self.pos[0] -= BLOCK_SIZE
        if self.dir == "RIGHT": self.pos[0] += BLOCK_SIZE

        self.body.insert(0, list(self.pos))

    def draw(self):
        for i, part in enumerate(self.body):
            color = GREEN if i == 0 else (0, 150, 0) # Голова светлее
            pygame.draw.rect(screen, color, (part[0], part[1], BLOCK_SIZE, BLOCK_SIZE))

# --- ПРЕПЯТСТВИЯ (СТЕНЫ) ---
def get_walls(level):
    walls = []
    if level >= 2:
        # Рисуем стену посередине
        for i in range(200, 600, BLOCK_SIZE):
            walls.append([i, 300])
    if level >= 3:
        # Добавляем вертикальные колонны
        for i in range(100, 500, BLOCK_SIZE):
            walls.append([200, i])
            walls.append([600, i])
    return walls

def main_game():
    snake = Snake()
    food = Food()
    score = 0
    level = 1
    running = True
    new_dir = "RIGHT"

    while running:
        screen.fill(BLACK)
        walls = get_walls(level)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP: new_dir = "UP"
                if event.key == pygame.K_DOWN: new_dir = "DOWN"
                if event.key == pygame.K_LEFT: new_dir = "LEFT"
                if event.key == pygame.K_RIGHT: new_dir = "RIGHT"

        snake.move(new_dir)

        # Проверка: съели еду?
        if snake.pos == food.pos:
            score += food.weight
            food.spawn()
            # Повышение уровня каждые 5 очков
            if score >= level * 5:
                level += 1
                snake.speed += 2 # Змейка ускоряется
        else:
            snake.body.pop()

        # Проверка: столкновение со стеной или собой?
        if (snake.pos[0] < 0 or snake.pos[0] >= WIDTH or 
            snake.pos[1] < 0 or snake.pos[1] >= HEIGHT or
            snake.pos in snake.body[1:] or
            snake.pos in walls):
            running = False

        # Отрисовка
        snake.draw()
        food.draw()
        for wall in walls:
            pygame.draw.rect(screen, BLUE, (wall[0], wall[1], BLOCK_SIZE, BLOCK_SIZE))
        
        # Инфо
        info = font.render(f"Score: {score}  Level: {level}  Speed: {snake.speed}", True, WHITE)
        screen.blit(info, (10, 10))

        pygame.display.flip()
        clock.tick(snake.speed)

    # Game Over
    screen.fill(RED)
    msg = font.render(f"GAME OVER! Score: {score}", True, WHITE)
    screen.blit(msg, (WIDTH//2-100, HEIGHT//2))
    pygame.display.flip()
    time.sleep(2)

if __name__ == "__main__":
    main_game()