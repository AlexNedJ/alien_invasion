import sys

import pygame

class AlianInvasion:
    def __init__(self):
        pygame.init()
        self.bg_color = (230, 230, 230)

        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Alian  Invasion")

    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            self.screen.fill(self.bg_color)
            pygame.display.flip()
if __name__ == '__main__':
    ai = AlianInvasion()
    ai.run_game()