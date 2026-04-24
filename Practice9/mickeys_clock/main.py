import pygame
import datetime
import os
import sys

pygame.init()

# Устанавливаем размер окна 800x800
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey's Clock")
clock = pygame.time.Clock()

# Пути к файлам
current_dir = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(current_dir, 'images')

def load_hand(name, size):
    path = os.path.join(image_dir, name)
    try:
        img = pygame.image.load(path).convert()
        img.set_colorkey((255, 255, 255)) # Делаем белый фон прозрачным
        return pygame.transform.scale(img, size)
    except:
        print(f"Ошибка: не удалось загрузить {name}")
        return None

# 1. Загружаем фон и растягиваем на всё окно
try:
    bg = pygame.image.load(os.path.join(image_dir, 'bg.png')).convert()
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
except:
    bg = None
    print("Фон bg.png не найден!")

# 2. Загружаем руки (задаем им адекватные размеры, чтобы не тормозило)
# (ширина, высота) - высота это длина стрелки
hand_hour = load_hand('hand_hour.png', (60, 250)) 
hand_min = load_hand('hand_minute.png', (45, 350))

center = (WIDTH // 2, HEIGHT // 2)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Очистка экрана (белый фон)
    screen.fill((255, 255, 255))

    # Рисуем фон
    if bg:
        screen.blit(bg, (0, 0))

    # Время и углы
    now = datetime.datetime.now()
    # В Pygame 0 градусов - это стрелка направо, поэтому считаем от 12 часов
    angle_min = -(now.minute * 6)
    angle_hour = -(now.hour * 30 + now.minute * 0.5)

    # Рисуем стрелки
    if hand_hour and hand_min:
        # Вращаем
        rot_hour = pygame.transform.rotate(hand_hour, angle_hour)
        rot_min = pygame.transform.rotate(hand_min, angle_min)
        
        # Центрируем и выводим
        screen.blit(rot_hour, rot_hour.get_rect(center=center))
        screen.blit(rot_min, rot_min.get_rect(center=center))
    else:
        # Если картинки не подгрузились, рисуем линии (запасной вариант для защиты)
        pygame.draw.line(screen, (0,0,0), center, (WIDTH//2, 100), 10)
        print("Внимание: используются линии вместо картинок")

    pygame.display.flip()
    clock.tick(60)