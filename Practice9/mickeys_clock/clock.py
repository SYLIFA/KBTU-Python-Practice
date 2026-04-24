import pygame
import time

class MickeyClock:
    def __init__(self, center_x, center_y):
        self.center = (center_x, center_y)
        image_dir = "Practice9/mickeys_clock/images"

        # 1. Загружаем твой фон (mickeyclock.jpeg)
        try:
            bg_img = pygame.image.load(f"{image_dir}/mickeyclock.jpeg").convert()
            self.bg = pygame.transform.scale(bg_img, (600, 600))
        except:
            self.bg = None

        # 2. Так как картинок рук нет, оставляем надежные заглушки
        try:
            self.left_hand = pygame.image.load(f"{image_dir}/left_hand.png").convert_alpha()
            self.right_hand = pygame.image.load(f"{image_dir}/right_hand.png").convert_alpha()
        except:
            # Левая рука (секунды) - красная
            self.left_hand = pygame.Surface((300, 20), pygame.SRCALPHA)
            pygame.draw.rect(self.left_hand, (255, 0, 0), (150, 0, 150, 20)) 
            # Правая рука (минуты) - черная
            self.right_hand = pygame.Surface((300, 30), pygame.SRCALPHA)
            pygame.draw.rect(self.right_hand, (0, 0, 0), (150, 0, 150, 30))

    def get_angles(self):
        t = time.localtime()
        sec_angle = t.tm_sec * 6
        min_angle = t.tm_min * 6 + (t.tm_sec * 0.1)
        return min_angle, sec_angle

    def draw(self, surface):
        # Рисуем фон
        if self.bg:
            surface.blit(self.bg, (0, 0))
        else:
            surface.fill((255, 255, 255))
            pygame.draw.circle(surface, (200, 200, 200), self.center, 250, 5)

        min_angle, sec_angle = self.get_angles()

        # Правая рука (Минуты)
        rotated_right = pygame.transform.rotate(self.right_hand, -min_angle + 90)
        rect_right = rotated_right.get_rect(center=self.center)
        surface.blit(rotated_right, rect_right)

        # Левая рука (Секунды)
        rotated_left = pygame.transform.rotate(self.left_hand, -sec_angle + 90)
        rect_left = rotated_left.get_rect(center=self.center)
        surface.blit(rotated_left, rect_left)