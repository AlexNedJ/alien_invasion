class Settings():
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (0, 0, 0)
        self.ship_speed = 1      
        # это параметры снаряда
        self.bullet_speed = 0.5
        self.bullet_width = 3
        self.bullet_heigth = 15
        self.bullet_color = (255, 0, 0)
        self.bullet_allowed = 3