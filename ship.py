import pygame

class Ship():
    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect() 
        self.image = pygame.image.load('images/ship_1_cropped.bmp')
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.settings = ai_game.settings
        self.x = float(self.rect.x)
        self.y = self.rect.y
        self.visible = True
        self._blink_interval = 200  # мс
        self._last_blink = 0
    
    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed    
                
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed    
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed    
            
        self.rect.x = self.x
        self.rect.y = self.y    
            
        # управляем миганием при неуязвимости
        if self.ai_game.invulnerable:
            now = pygame.time.get_ticks()
            if now - self._last_blink >= self._blink_interval:
                self.visible = not self.visible
                self._last_blink = now
        else:
            self.visible = True    
    
    def blitime(self):
        if self.visible:
            self.screen.blit(self.image, self.rect)