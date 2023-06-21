import random

import pygame

from settings import *


class MagicPlayer:
    def __init__(self, animationPlayer):
        self.animation = animationPlayer

    def heal(self, player, strength, cost, groups):
        if player.stamina >= cost:
            player.hp += strength
            if player.hp >= player.baseStats['hp']:
                player.hp = player.baseStats['hp']
            else:
                player.stamina -= cost

    def flame(self, player, strength, cost, groups):
        if player.stamina >= cost:
            player.stamina -= cost
            status = player.status.split('_')[0]

            if status == 'right':
                direction = pygame.math.Vector2(1, 0)

            elif status == 'left':
                direction = pygame.math.Vector2(-1, 0)

            elif status == 'up':
                direction = pygame.math.Vector2(0, -1)

            else:
                direction = pygame.math.Vector2(0, 1)

            for i in range(1, 6):
                if direction.x:
                    offset = direction.x * i * TILESIZE
                    x = player.rect.centerx + offset + random.randint(-TILESIZE // 3, TILESIZE // 3)
                    y = player.rect.centery + random.randint(-TILESIZE // 3, TILESIZE // 3)

                    self.animation.generateParticles((x, y), 'flame', groups)

                else:
                    offset = direction.y * i * TILESIZE
                    x = player.rect.centerx + random.randint(-TILESIZE // 3, TILESIZE // 3)
                    y = player.rect.centery + offset + random.randint(-TILESIZE // 3, TILESIZE // 3)

                    self.animation.generateParticles((x, y), 'flame', groups)

