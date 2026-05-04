import pygame
import random
import time
import os
from persistence import load_settings, save_settings, save_score, load_leaderboard

# --- ИНИЦИАЛИЗАЦИЯ ---
pygame.init()
W, H = 400, 600
SCREEN = pygame.display.set_mode((W, H))
pygame.display.set_caption("KBTU Racer PRO")
CLOCK = pygame.time.Clock()
FONT = pygame.font.SysFont("Verdana", 20)
BIG_FONT = pygame.font.SysFont("Verdana", 35, bold=True)

# Цвета
WHITE, BLACK, RED, GREEN, BLUE = (255,255,255), (0,0,0), (255,0,0), (0,255,0), (0,0,255)
GRAY, YELLOW = (128,128,128), (255,255,0)

# --- КЛАССЫ ОБЪЕКТОВ ---
class Player(pygame.sprite.Sprite):
    def __init__(self, color_name):
        super().__init__()
        self.image = pygame.Surface((45, 80))
        self.image.fill(pygame.Color(color_name))
        self.rect = self.image.get_rect(center=(W//2, H-70))
        self.lives = 3
        self.shield = False
        self.nitro_until = 0

    def update(self):
        keys = pygame.key.get_pressed()
        speed = 10 if time.time() < self.nitro_until else 5
        if keys[pygame.K_LEFT] and self.rect.left > 0: self.rect.x -= speed
        if keys[pygame.K_RIGHT] and self.rect.right < W: self.rect.x += speed

class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.Surface((50, 80))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(random.randint(40, W-40), -100))
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > H:
            self.rect.top = -100
            self.rect.center = (random.randint(40, W-40), 0)

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, p_type):
        super().__init__()
        self.type = p_type # 'nitro', 'shield', 'repair'
        self.image = pygame.Surface((30, 30))
        color = YELLOW if p_type == 'nitro' else BLUE if p_type == 'shield' else GREEN
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(random.randint(30, W-30), -50))

    def update(self, speed):
        self.rect.y += speed
        if self.rect.top > H: self.kill()

# --- ЭКРАНЫ И ЛОГИКА ---
def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    SCREEN.blit(img, (x, y))

def menu_screen():
    settings = load_settings()
    while True:
        SCREEN.fill(GRAY)
        draw_text("RACER PRO", BIG_FONT, BLACK, 90, 100)
        play_btn = pygame.Rect(100, 250, 200, 50)
        set_btn = pygame.Rect(100, 320, 200, 50)
        
        pygame.draw.rect(SCREEN, WHITE, play_btn)
        pygame.draw.rect(SCREEN, WHITE, set_btn)
        draw_text("PLAY", FONT, BLACK, 170, 260)
        draw_text("SETTINGS", FONT, BLACK, 150, 330)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_btn.collidepoint(event.pos): return "GAME"
                if set_btn.collidepoint(event.pos): return "SETTINGS"
        
        pygame.display.flip()

def game_loop():
    settings = load_settings()
    player = Player(settings['car_color'])
    enemy_speed = 5 if settings['difficulty'] == "Medium" else 3 if settings['difficulty'] == "Easy" else 8
    
    enemies = pygame.sprite.Group(Enemy(enemy_speed))
    powerups = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group(player)
    
    score = 0
    distance = 0
    running = True
    
    while running:
        SCREEN.fill(WHITE)
        distance += enemy_speed / 10
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "MENU"

        # Спавн бонусов
        if random.random() < 0.01:
            p = PowerUp(random.choice(['nitro', 'shield', 'repair']))
            powerups.add(p); all_sprites.add(p)

        # Обновление
        player.update()
        enemies.update()
        powerups.update(enemy_speed)

        # Коллизии
        if pygame.sprite.spritecollide(player, enemies, True):
            if player.shield:
                player.shield = False
                enemies.add(Enemy(enemy_speed))
            else:
                player.lives -= 1
                if player.lives <= 0:
                    save_score("Boss", int(score + distance), int(distance))
                    return "OVER"
                enemies.add(Enemy(enemy_speed))

        p_hits = pygame.sprite.spritecollide(player, powerups, True)
        for p in p_hits:
            if p.type == 'nitro': player.nitro_until = time.time() + 5
            elif p.type == 'shield': player.shield = True
            elif p.type == 'repair': player.lives = min(3, player.lives + 1)

        # Отрисовка
        all_sprites.draw(SCREEN)
        enemies.draw(SCREEN)
        
        # UI в игре
        draw_text(f"Lives: {player.lives} | Score: {int(score + distance)}", FONT, BLACK, 10, 10)
        if player.shield: draw_text("SHIELD ACTIVE", FONT, BLUE, 10, 40)
        if time.time() < player.nitro_until: draw_text("NITRO!!!", FONT, YELLOW, 10, 70)

        pygame.display.flip()
        CLOCK.tick(60)

# --- ГЛАВНЫЙ ЗАПУСК ---
def main():
    state = "MENU"
    while state:
        if state == "MENU": state = menu_screen()
        elif state == "GAME": state = game_loop()
        elif state == "OVER":
            time.sleep(2) # Пауза перед выходом в меню
            state = "MENU"
        else: state = None

if __name__ == "__main__":
    main()