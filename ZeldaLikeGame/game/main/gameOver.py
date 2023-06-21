import pygame
from settings import *


class GameOver:
    def __init__(self, player, surface):
        self.surface = surface
        self.player = player
        self.font = pygame.font.Font(FONT, FONTSIZE)
        self.rect = pygame.Rect(20,
                                self.surface.get_height() * 0.1,
                                self.surface.get_width() * 0.1,
                                self.surface.get_height() * 0.8,
                                )

    def displayScreen(self):
        pygame.draw.rect(self.surface, UIBGCOLOUR, self.rect)

        colour = UIBGCOLOUR

        gameOverSurf = self.font.render("GAME OVER", False, FONTCOLOUR)
        gameOverRect = gameOverSurf.get_rect()