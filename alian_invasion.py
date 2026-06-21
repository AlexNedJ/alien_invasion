import sys
from seting import Settings
from ship import Ship
import pygame
from bullet import Bullet
from alien import Alian
import random
from button import Button

class AlianInvasion:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock() 
        self.game_active = False
        self.game_over_font = pygame.font.Font(None, 74)
        self.button_font = pygame.font.Font(None, 36)
        self.menu_items = [{'text': 'Resume', 'action': self._resume_game},
                           {'text': 'Settings', 'action': self._show_settings},
                           {'text': 'Main Menu', 'action': self._goto_main_menu},
                           {'text': 'Exit', 'action': self._quit_game},
                           ]
        self.selected_item = 0
        self.paused = False
        self.menu_font = pygame.font.Font(None, 36) 
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.screen_rect = self.screen.get_rect()
        self.score = 0
        self.hits_for_extra_life = 0            # счетчик попаданий для доп. жизни
        self.lives = 3                          # начальные жизни
        self.invulnerable = False               # флаг неуязвимости после попадания
        self.invulnerable_start = 0
        self.invulnerable_duration = 2000      # мс — длительность неуязвимости
        self.font = pygame.font.Font(None, self.settings.score_font_size)
    
        self.background = self.settings.background
        pygame.display.set_caption("Alian Invasion!")
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.alians = pygame.sprite.Group()
        self._create_fleet()
        
        # Создание кнопки Play.
        self.play_button = Button(self, "Play")
        
        # ----- moon animation init -----
        self.moon_surf = getattr(self.settings, 'moon', None)
        if not self.moon_surf:
            try:
                self.moon_surf = pygame.image.load('images/moon.bmp').convert_alpha()
            except Exception:
                self.moon_surf = pygame.Surface((80, 80), pygame.SRCALPHA)
                pygame.draw.circle(self.moon_surf, (200, 200, 200), (40, 40), 40)
        self.moon_w, self.moon_h = self.moon_surf.get_size()
        box_w, box_h = 220, 220
        self.moon_box = pygame.Rect(self.settings.screen_width - box_w - 10, 10, box_w, box_h)
        self.moon_x = random.uniform(self.moon_box.left, self.moon_box.right - self.moon_w)
        self.moon_y = random.uniform(self.moon_box.top, self.moon_box.bottom - self.moon_h)
        self.moon_vx = random.uniform(-0.025, 0.025)   # скорость в пикселях/мс (маленькая)
        self.moon_vy = random.uniform(-0.015, 0.015)
        self.moon_change_timer = 0
            
    def _update_background_objects(self):
        # --- moon ---
        self.moon_x += self.moon_vx
        self.moon_y += self.moon_vy
        # отскок внутри коробки
        if self.moon_x < self.moon_box.left:
            self.moon_x = self.moon_box.left
            self.moon_vx *= -1
        if self.moon_x > self.moon_box.right - self.moon_w:
            self.moon_x = self.moon_box.right - self.moon_w
            self.moon_vx *= -1
        if self.moon_y < self.moon_box.top:
            self.moon_y = self.moon_box.top
            self.moon_vy *= -1
        if self.moon_y > self.moon_box.bottom - self.moon_h:
            self.moon_y = self.moon_box.bottom - self.moon_h
            self.moon_vy *= -1

        if self.moon_change_timer > 3000:  # каждые ~3 секунды немного меняем направление
            self.moon_vx = random.uniform(-0.03, 0.03)
            self.moon_vy = random.uniform(-0.02, 0.02)
            
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event) # событие нажатие на кнопку

            elif event.type == pygame.KEYUP: # событие отпустили кнопку
                self._check_keyup_events(event)
                
    def _check_play_button(self, mouse_pos):
        """Запускает новую игру при нажатии кнопки Play."""
        if not self.game_active:
            button_clicked = self.play_button.rect.collidepoint(mouse_pos)
            if button_clicked:
                self._reset_game()

    def _check_keydown_events(self, event):
        # Игра активна и не на паузе — обработка управления
        if self.game_active and not self.paused:
            if event.key == pygame.K_ESCAPE:
                self.paused = True
                return
            if event.key == pygame.K_RIGHT:
                self.ship.moving_right = True
            elif event.key == pygame.K_LEFT:
                self.ship.moving_left = True
            elif event.key == pygame.K_UP:
                self.ship.moving_up = True
            elif event.key == pygame.K_DOWN:
                self.ship.moving_down = True
            elif event.key == pygame.K_SPACE:
                self._fire_bullet()
            elif event.key == pygame.K_q:
                sys.exit()
            return

        # Меню паузы
        if self.paused:
            if event.key == pygame.K_ESCAPE:
                self.paused = False
            elif event.key == pygame.K_UP:
                self.selected_item = (self.selected_item - 1) % len(self.menu_items)
            elif event.key == pygame.K_DOWN:
                self.selected_item = (self.selected_item + 1) % len(self.menu_items)
            elif event.key == pygame.K_RETURN:
                action = self.menu_items[self.selected_item].get('action')
                if callable(action):
                    action()
            return

        # Главное меню / экран Game Over
        if not self.game_active:
            if event.key == pygame.K_RETURN:
                self._reset_game()
            elif event.key == pygame.K_ESCAPE and self.lives <= 0:
                sys.exit()
    
    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
                    
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
                
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
                
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False
    
    def _reset_game(self):
        # Сброс игры к начальному состоянию
        self.game_active = True
        self.score = 0
        self.hits_for_extra_life = 0
        self.lives = 3
        self.bullets.empty()
        self.alians.empty()
        
        self.ship.rect.midbottom = self.screen_rect.midbottom
        self.ship.x = float(self.ship.rect.x)
        self.ship.y = float(self.ship.rect.y)
        
        self._create_fleet()

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            
    def _update_bullets(self):
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet) 
        self._check_bullet_alien()
        
        if not self.alians:
            self.bullets.empty()
            self._create_fleet()
                        
    def _check_bullet_alien(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.alians, True, True)
            
        if collisions:
            # подсчет уничтоженных пришельцев в этой итерации
            destroyed = sum(len(v) for v in collisions.values())
            self.score += destroyed
            self.hits_for_extra_life += destroyed
            # каждые 50 попаданий даем +1 жизнь
            while self.hits_for_extra_life >= 50:
                self.lives += 1
                self.hits_for_extra_life -= 50
                       
    def _update_screen(self):
        self.screen.fill((0, 0, 0)) # clear screen
        # отрисовка Луны (перед основным фоном, но позади корабля/пришельцев)
        self.screen.blit(self.moon_surf, (int(self.moon_x), int(self.moon_y)))   
                
        if self.game_active:
            self.ship.blitime()
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.alians.draw(self.screen)
            
            # Отображение счета и жизней
            score_text = self.font.render(f'Score: {self.score}', True, self.settings.score_color)
            score_rect = score_text.get_rect()
            score_rect.right = self.settings.screen_width - 10
            score_rect.top = 10
            self.screen.blit(score_text, score_rect)

            lives_text = self.font.render(f'Lives: {self.lives}', True, self.settings.score_color)
            lives_rect = lives_text.get_rect()
            lives_rect.left = 10
            lives_rect.top = 10
            self.screen.blit(lives_text, lives_rect)
            
            if self.paused:
                self._draw_pause_menu()
                
        elif self.lives <= 0:
            # Отображение экрана Game Over
            game_over_text = self.game_over_font.render("GAME OVER", True, (255, 0, 0))
            score_text = self.font.render(f'Final Score: {self.score}', True, self.settings.score_color)
            retry_text = self.button_font.render("Press ENTER to retry or ESC to quit", True, (255, 255, 255))
            
            game_over_rect = game_over_text.get_rect(center=(self.settings.screen_width // 2, self.settings.screen_height // 2 - 50))
            score_rect = score_text.get_rect(center=(self.settings.screen_width // 2, self.settings.screen_height // 2 + 10))
            retry_rect = retry_text.get_rect(center=(self.settings.screen_width // 2, self.settings.screen_height // 2 + 60))
            
            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(score_text, score_rect)
            self.screen.blit(retry_text, retry_rect)   
        else:
            self.play_button.draw_button()
            
        pygame.display.flip()
    
    def _draw_pause_menu(self):
        # Затемнение экрана
        s = pygame.Surface((self.settings.screen_width, self.settings.screen_height))
        s.set_alpha(128)
        s.fill((0, 0, 0))
        self.screen.blit(s, (0, 0))
        
        # Отрисовка меню
        menu_y = self.settings.screen_height // 2 - (len(self.menu_items) * 40) // 2
        for i, item in enumerate(self.menu_items):
            color = (255, 255, 0) if i == self.selected_item else (255, 255, 255)
            text = self.menu_font.render(item['text'], True, color)
            rect = text.get_rect(center=(self.settings.screen_width // 2, menu_y + i * 40))
            self.screen.blit(text, rect)
            
    def _resume_game(self):
        self.paused = False
    
    def _show_settings(self):
        # Заглушка для будущих настроек
        print("Settings menu - to be implemented")
    
    def _goto_main_menu(self):
        self.paused = False
        self.game_active = False
        # Не очищаем данные игры, чтобы можно было вернуться
    
    def _quit_game(self):
        pygame.quit()
        sys.exit()
                
    def _update_alians(self):
        self.bullets.update()
        # обновление позиций прищельцев
        self.alians.update()
        
        # столкновение корабля с пришельцем
        if pygame.sprite.spritecollideany(self.ship, self.alians):
            if not self.invulnerable:
                self._ship_hit()
    
    def _ship_hit(self):
        # удаляем те пришельцы, которые пересеклись с кораблем
        pygame.sprite.spritecollide(self.ship, self.alians, True)
        self.lives -= 1
        if self.lives <= 0:
            self.game_active = False
        else:
            self.invulnerable = True
            self.invulnerable_start = pygame.time.get_ticks()
            self.ship.visible = False
            
        # включаем неуязвимость и мигание
        self.invulnerable = True
        self.invulnerable_start = pygame.time.get_ticks()
        # сбрасываем видимость корабля (мигание контролируется в ship.update)
        self.ship.visible = False
    
    def _create_fleet(self):
        alian = Alian(self.screen, self.settings)
        alian_width, alian_height = alian.rect.size
        for _ in range(self.settings.number_alians):
            x = random.randint(0, self.settings.screen_width - alian_width)
            y = random.randint(-self.settings.screen_height, 0)
            speed_y = random.uniform(self.settings.alian_speed_min, self.settings.alian_speed_max)
            speed_x = random.uniform(self.settings.alian_wind_min, self.settings.alian_wind_max)
            alian = Alian(self.screen, self.settings, x, y, speed_y, speed_x)
            self.alians.add(alian)
    
    def _check_invulnerability(self):
        if self.invulnerable:
            now = pygame.time.get_ticks()
            if now - self.invulnerable_start >= self.invulnerable_duration:
                self.invulnerable = False
                self.ship.visible = True
                
    def run_game(self):
        while True:
            self._check_events()
            if self.game_active and not self.paused:
                self.ship.update()
                self._update_bullets()
                self._update_alians()
                self._check_invulnerability()
                self._update_background_objects()
            self._update_screen()
                        
if __name__ == '__main__':
    ai = AlianInvasion()
    ai.run_game()