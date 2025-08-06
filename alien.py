import pygame
from pygame.sprite import Sprite

class Alian(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        # запускаем изображение прищельца и назначаем атрибут rect
        self.image = pygame.image.load('images/alien_invasion_1.bmp')
        self.rect = self.image.get_rect()
        # каждый новый прищелец появляеться в левом верхнем углу экрана
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # сохранение точной горизонтальной позиции прищельца
        self.x = float(self.rect.x)