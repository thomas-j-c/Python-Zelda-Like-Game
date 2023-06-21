from csv import reader
from os import walk
import pygame


def importCSVLayout(path):
    level = []
    with open(path) as levelMap:
        layout = reader(levelMap)
        for i in layout:
            level.append(list(i))

    return level


def importFolder(path):
    surfList = []
    for data in walk(path):
        for i in data[2]:
            fullpath = path + "/" + i
            surface = pygame.image.load(fullpath).convert_alpha()
            surfList.append(surface)

    return surfList
