import sys
from seting import Settings
from ship import Ship
import pygame
from bullet import Bullet
from alien import Alian

class AlianInvasion:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        self.background = self.settings.background
        pygame.display.set_caption("Alian Invasion")
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.alians = pygame.sprite.Group()
        self._create_fleet()

    def run_game(self):
        while True:
            self._check_events()
            self.ship.update()
            self._update_screen()
            self.bullets.update()
            self._update_bullets_()
            
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event) # событие нажатие на кнопку

            elif event.type == pygame.KEYUP: # событие отпустили кнопку
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.rect.x += 1
            self.ship.moving_right = True
                    
        elif event.key == pygame.K_LEFT:
            self.ship.rect.x -= 1
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
                
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
                
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    
    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
                    
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
                
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
                
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False
            
    def _update_bullets_(self):
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet) 
                
    def _create_fleet(self):
        alian = Alian(self)
        alian_width = alian.rect.width
        alian_width, alian_height = alian.rect.size
        available_space_x = self.settings.screen_width - (2 * alian_width)
        number_alians_x = available_space_x - (2 * alian_width) // ( 2 * alian_width) 
        # определение количество рядов помещенных на экран
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alian_height) - ship_height)
        number_rows = available_space_y // (2 * alian_height)

        # создание флота прищельцев
        for row_number in range(number_rows):
            for alian_number in range(number_alians_x):
                self._create_alian(alian_number, row_number)
    
    
    
    def _create_alian(self, alian_number, row_number):
        alian = Alian(self)
        alian_width, alian_height = alian.rect.size
        alian.x = alian_width + 2 * alian_width * alian_number
        alian.rect.x = alian.x
        alian.rect.y = alian.rect.height + 2 * alian.rect.height * row_number
        self.alians.add(alian)
                       
    def _update_screen(self):
        self.screen.blit(self.settings.background, self.settings.moon_pos)
        self.ship.blitime()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.alians.draw(self.screen)
        pygame.display.flip()
        
if __name__ == '__main__':
    ai = AlianInvasion()
    ai.run_game()