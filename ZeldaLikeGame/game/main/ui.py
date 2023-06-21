import pygame
from settings import *


class UI:
    def __init__(self):
        self.surface = pygame.display.get_surface()
        self.font = pygame.font.Font(FONT, FONTSIZE)

        self.healthBar = pygame.Rect(20, 10, BARWIDTH, BARHEIGHT)
        self.energyBar = pygame.Rect(20, 40, BARWIDTH, BARHEIGHT)

        self.weaponImgs = []
        self.magicImgs = []

        for weapon in weapons.values():
            path = weapon['img']
            weapon = pygame.image.load(path).convert_alpha()
            self.weaponImgs.append(weapon)

        for mg in magic.values():
            path = mg['img']
            image = pygame.image.load(path).convert_alpha()
            self.magicImgs.append(image)

    def showBars(self, current, maximum, bgRect, colour):
        pygame.draw.rect(self.surface, UIBGCOLOUR, bgRect)

        ratio = current / maximum

        currentWidth = bgRect.width * ratio

        pygame.draw.rect(self.surface, colour, pygame.Rect(bgRect.left, bgRect.top, currentWidth, BARHEIGHT))
        pygame.draw.rect(self.surface, UIBORDERCOLOUR, bgRect, 3)

    def showExp(self, exp):
        text = self.font.render(str(int(exp)), False, FONTCOLOUR)

        textBox = text.get_rect(bottomleft=(20, self.surface.get_size()[1] - 20))

        pygame.draw.rect(self.surface, UIBGCOLOUR, textBox.inflate(20, 20))
        self.surface.blit(text, textBox)
        pygame.draw.rect(self.surface, UIBORDERCOLOUR, textBox.inflate(20, 20), 3)

    def showHealth(self, health):
        text = self.font.render(str(int(health)), False, FONTCOLOUR)

        textBox = text.get_rect(bottomleft=(40, self.surface.get_size()[1] - 20))

        pygame.draw.rect(self.surface, UIBGCOLOUR, textBox.inflate(20, 20))
        self.surface.blit(text, textBox)
        pygame.draw.rect(self.surface, UIBORDERCOLOUR, textBox.inflate(20, 20), 3)

    def selectBox(self, left, top, switched):
        bgRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)

        pygame.draw.rect(self.surface, UIBGCOLOUR, bgRect)

        if switched:
            pygame.draw.rect(self.surface, ACTIVEUICOLOUR, bgRect, 3)
        else:
            pygame.draw.rect(self.surface, UIBORDERCOLOUR, bgRect, 3)

        return bgRect

    def drawWeapon(self, player):
        background = self.selectBox(BARWIDTH + 40, 10, not player.canSwitchWeapon)
        weaponSurface = self.weaponImgs[player.weaponIndex]
        weaponRect = weaponSurface.get_rect(center=background.center)

        self.surface.blit(weaponSurface, weaponRect)

    def drawMagic(self, player):
        background = self.selectBox(BARWIDTH + BOXSIZE + 60, 10, not player.canSwitchMagic)
        magicSurface = self.magicImgs[player.magicIndex]
        magicRect = magicSurface.get_rect(center=background.center)

        self.surface.blit(magicSurface, magicRect)

    def display(self, player):
        self.showBars(player.hp, player.baseStats['hp'], self.healthBar, HEALTHCOLOUR)
        self.showBars(player.stamina, player.baseStats['stamina'], self.energyBar, ENERGYCOLOUR)

        self.showExp(player.exp)

        self.drawWeapon(player)
        self.drawMagic(player)
