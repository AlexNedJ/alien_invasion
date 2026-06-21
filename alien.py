import pygame
import random

class Alian(pygame.sprite.Sprite):
    def __init__(self, screen, settings, x=None, y=None, speed_y=None, speed_x=None):
        super().__init__()
        self.screen = screen
        self.settings = settings
        # запускаем изображение прищельца и назначаем атрибут rect
        self.image = pygame.image.load('images/alien_invasion_1.bmp')
        self.rect = self.image.get_rect()
        self.rect.x = x if x is not None else self.rect.width
        self.rect.y = y if y is not None else self.rect.height
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.speed_y = speed_y if speed_y is not None else random.uniform(self.settings.alian_wind_min, self.settings.alian_speed_max)
        self.speed_x = speed_x if speed_x is not None else random.uniform(self.settings.alian_wind_min, self.settings.alian_wind_max)
    

    def update(self):
            self.x += self.speed_x
            self.y += self.speed_y
            self.rect.x = int(self.x)
            self.rect.y = int(self.y)
            if self.rect.top > self.screen.get_rect().bottom:
                self.y = float(-self.rect.height)
                self.x = random.randint(0, self.settings.screen_width - self.rect.width)
                self.speed_y = random.uniform(self.settings.alian_speed_min, self.settings.alian_speed_max)
                self.speed_x = random.uniform(self.settings.alian_wind_min, self.settings.alian_wind_max)
            # Если корабль пришельца вышла за правый край, меняем направление на противоположное
            if self.rect.right > self.screen.get_rect().right:
                self.x = self.screen.get_rect().right - self.rect.width
                self.speed_x = -abs(self.speed_x)  # Движение влево
            # Если корабль пришельца вышла за левый край, меняем направление на противоположное
            elif self.rect.left < 0:
                self.x = 0
                self.speed_x = abs(self.speed_x) 