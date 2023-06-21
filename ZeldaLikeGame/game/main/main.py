import pygame
import sys
from settings import *
from level import Level

from debug import debug


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Zelda Game")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.level = Level()

        music = pygame.mixer.Sound('../res/audio/main.ogg')
        music.play(loops=-1)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.level.toggleMenu()

            self.screen.fill(WATERCOLOUR)
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
