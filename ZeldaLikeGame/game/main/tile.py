import pygame
from settings import TILESIZE, HBOXOFFSET


class Tile(pygame.sprite.Sprite):
    def __init__(self, position, group, spritetype, surface=pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(group)
        self.spriteType = spritetype
        self.image = surface
        yOffset = HBOXOFFSET[spritetype]

        if spritetype == "object":
            self.rect = self.image.get_rect(topleft=(position[0], position[1] - TILESIZE))

        self.rect = self.image.get_rect(topleft=position)
        self.hBox = self.rect.inflate(0, yOffset)
