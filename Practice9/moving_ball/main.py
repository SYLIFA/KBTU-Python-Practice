import pygame
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from ball import Ball

def main():
    # Инициализация Pygame
    pygame.init()
    
    # Настройки экрана
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Moving Ball - WASD & Arrows")
    
    # Настройки времени (FPS)
    clock = pygame.time.Clock()

    # Создаем объект шара (в центре, радиус 25, красный, скорость 20)
    my_ball = Ball(WIDTH // 2, HEIGHT // 2, 25, (255, 0, 0), 20)

    running = True
    while running:
        # Очищаем экран (оливковый)
        screen.fill((229, 233 , 227))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Обработка нажатий (KEYDOWN срабатывает один раз при нажатии)
            elif event.type == pygame.KEYDOWN:
                # ВВЕРХ: Стрелка Вверх или W
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    my_ball.move(0, -1, WIDTH, HEIGHT)
                
                # ВНИЗ: Стрелка Вниз или S
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    my_ball.move(0, 1, WIDTH, HEIGHT)
                
                # ВЛЕВО: Стрелка Влево или A
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    my_ball.move(-1, 0, WIDTH, HEIGHT)
                
                # ВПРАВО: Стрелка Вправо или D
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    my_ball.move(1, 0, WIDTH, HEIGHT)

        # Рисуем шар
        my_ball.draw(screen)
        
        # Обновляем дисплей
        pygame.display.flip()
        
        # Держим 60 кадров в секунду
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()