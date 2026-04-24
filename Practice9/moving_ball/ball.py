import pygame

class Ball:
    def __init__(self, x, y, radius, color, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = speed

    def draw(self, surface):
        # Рисуем красный круг
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

    def move(self, dx, dy, screen_width, screen_height):
        # Рассчитываем новую позицию
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        
        # Проверка границ: шар не выйдет за пределы экрана
        if self.radius <= new_x <= screen_width - self.radius:
            self.x = new_x
        if self.radius <= new_y <= screen_height - self.radius:
            self.y = new_y