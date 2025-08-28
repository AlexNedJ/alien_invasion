import pygame
from pygame.sprite import Sprite

class Alian(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        # запускаем изображение прищельца и назначаем атрибут rect
        self.image = pygame.image.load('images/alien_invasion_1.bmp')
        self.rect = self.image.get_rect()
        # каждый новый прищелец появляеться в левом верхнем углу экрана
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # сохранение точной горизонтальной позиции прищельца
        self.x = float(self.rect.x)
    
    def check_edges(self):
        """Возвращает True, если пришелец достиг края экрана (слева или справа)."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
        return False

    def update(self):
        # движение вправо
        self.x += (self.settings.alian_speed * self.settings.fleet_direction)
        self.rect.x = self.x