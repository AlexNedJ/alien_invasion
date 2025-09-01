import pygame

class Settings():
    def __init__(self):
        self.alian_speed = 0.2
        self.fleet_drop_speed = 10
        self.fleet_direction = 1 # 1 обозначает движение вправо; -1 - влево
        self.screen_width = 800
        self.screen_height = 600
        self.background = pygame.image.load('images/moon.bmp')
        self.moon_pos = (self.screen_width - self.background.get_width(), 0)
        self.meteorite= pygame.image.load('images/meteorite-1414819_1280.bmp')
        self.meteorite_pos = (self.screen_height - self.meteorite.get_width(), 0)
        self.ship_speed = 1      
        # это параметры снаряда
        self.bullet_speed = 0.5
        self.bullet_width = 3
        self.bullet_heigth = 15
        self.bullet_color = (255, 0, 0)
        self.bullet_allowed = 3