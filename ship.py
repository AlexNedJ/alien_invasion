import pygame

class Ship():
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()  # Исправлено!
        self.image = pygame.image.load('images/ship_1_cropped.bmp')
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        self.moving_right = False
        self.moving_left = False
        self.settings = ai_game.settings
        self.x = float(self.rect.x)
    
    def update(self):
        if self.moving_right :
            self.x += self.settings.ship_speed
        if self.moving_left:
            self.x -= self.settings.ship_speed
        self.rect.x = self.x

    def blitime(self):
        self.screen.blit(self.image, self.rect)