import pygame
from settings import *


class Upgrade:
    def __init__(self, player):
        self.display = pygame.display.get_surface()
        self.player = player

        self.attributeLen = len(player.baseStats)
        self.attributeNames = list(player.baseStats.keys())
        self.maxValues = list(player.maxStats.values())

        self.font = pygame.font.Font(FONT, FONTSIZE)

        self.height = self.display.get_height() * 0.8
        self.width = self.display.get_width() // 6
        self.createItems()

        self.selectionIndex = 0
        self.selectionTime = None
        self.canMove = True

    def input(self):
        keys = pygame.key.get_pressed()
        if self.canMove:
            if keys[pygame.K_RIGHT]:
                self.selectionIndex += 1
                if self.selectionIndex > self.attributeLen - 1:
                    self.selectionIndex = 0

                self.canMove = False
                self.selectionTime = pygame.time.get_ticks()

            elif keys[pygame.K_LEFT]:
                self.selectionIndex -= 1
                if self.selectionIndex < 0:
                    self.selectionIndex = self.attributeLen - 1

                self.canMove = False
                self.selectionTime = pygame.time.get_ticks()

            elif keys[pygame.K_SPACE]:
                self.canMove = False
                self.selectionTime = pygame.time.get_ticks()
                self.items[self.selectionIndex].trigger(self.player)

    def createItems(self):
        self.items = []
        top = self.display.get_height() * 0.1
        width = self.display.get_width()

        increment = width // self.attributeLen

        for item, index in enumerate(range(self.attributeLen)):
            left = (item * increment) + (increment - self.width) // 2

            self.items.append(Item(left, top, self.width, self.height, index, self.font))

    def cooldown(self):
        if not self.canMove:
            currentTime = pygame.time.get_ticks()

            if currentTime - self.selectionTime >= 300:
                self.canMove = True

    def displayMenu(self):
        self.input()
        self.cooldown()

        for index, item in enumerate(self.items):
            name = self.attributeNames[index]
            maxVal = self.maxValues[index]
            value = self.player.getValue(index)
            cost = self.player.getCost(index)

            item.displayItem(self.display, self.selectionIndex, name, value, maxVal, cost)


class Item:
    def __init__(self, left, top, width, height, index, font):
        self.rect = pygame.Rect(left, top, width, height)
        self.index = index
        self.font = font

    def displayAttributes(self, surface, name, cost, selected):
        colour = UPGRADETEXTCOLOUR if selected else FONTCOLOUR

        titleSurface = self.font.render(name, False, colour)
        titleRect = titleSurface.get_rect(midtop=self.rect.midtop + pygame.math.Vector2(0, 20))

        costSurface = self.font.render('Cost: ' + str(cost), False, colour)
        costRect = costSurface.get_rect(midbottom=self.rect.midbottom + pygame.math.Vector2(0, -20))

        surface.blit(costSurface, costRect)
        surface.blit(titleSurface, titleRect)

    def displayBars(self, surface, value, maxValue, selected):
        top = self.rect.midtop + pygame.math.Vector2(0, 60)
        bottom = self.rect.midbottom + pygame.math.Vector2(0, -60)
        colour = BARCOLOURSELECTED if selected else BARCOLOUR

        fullHeight = bottom.y - top.y
        normalised = (value / maxValue) * fullHeight
        valueRect = pygame.Rect(top.x - 15, bottom.y - normalised, 30, 30)

        pygame.draw.line(surface, colour, top, bottom, 5)
        pygame.draw.rect(surface, colour, valueRect)

    def trigger(self, player):
        upgradeAtt = list(player.baseStats.keys())[self.index]
        if player.exp >= player.upgradeCosts[upgradeAtt] and player.baseStats[upgradeAtt] < player.maxStats[upgradeAtt]:
            player.exp -= player.upgradeCosts[upgradeAtt]
            player.baseStats[upgradeAtt] *= 1.2
            player.upgradeCosts[upgradeAtt] *= 1.2

    def displayItem(self, surface, selectIndex, name, value, maxValue, cost):
        if self.index == selectIndex:
            pygame.draw.rect(surface, UPGRADEBGCOLOURSELECTED, self.rect)
            pygame.draw.rect(surface, UIBORDERCOLOUR, self.rect, 4)
        else:
            pygame.draw.rect(surface, UIBGCOLOUR, self.rect)
            pygame.draw.rect(surface, UIBORDERCOLOUR, self.rect, 4)

        self.displayAttributes(surface, name, cost, self.index == selectIndex)
        self.displayBars(surface, value, maxValue, self.index == selectIndex)
