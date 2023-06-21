import math

import pygame

from game.main import util
from settings import *
from entity import Entity


class Enemy(Entity):
    def __init__(self, name, pos, group, obstacleSprites, damagePlayer, deathEffect, addExp):
        super().__init__(group)

        self.font = pygame.font.Font(FONT, FONTSIZE)
        self.surface = pygame.display.get_surface()

        self.attackedTime = None
        self.animations = {'idle': [], 'move': [], 'attack': []}
        self.spriteType = 'enemy'

        self.getAssets(name)
        self.status = 'idle'

        self.image = self.animations[self.status][self.frameIndex]
        self.rect = self.image.get_rect(topleft=pos)

        self.hBox = self.rect.inflate(0, -10)
        self.obstacles = obstacleSprites

        monsterData = enemies[name]

        self.name = name
        self.speed = monsterData['speed']
        self.health = monsterData['health']
        self.exp = monsterData['exp']
        self.attackDMG = monsterData['dmg']
        self.res = monsterData['res']
        self.attackRad = monsterData['attackRad']
        self.noticeRad = monsterData['noticeRad']
        self.attackType = monsterData['attackType']

        self.canAttack = True
        self.attackTime = None
        self.damagePlayer = damagePlayer
        
        self.vulnerable = True  # Can the enemy be attacked

        self.deathEffect = deathEffect
        self.addExp = addExp

    def getAssets(self, name):
        path = f'../res/monsters/{name}/'

        for a in self.animations.keys():
            self.animations[a] = util.importFolder(path + a)

    def getPlayerDistanceAngle(self, player):
        player = pygame.math.Vector2(player.rect.center)
        enemy = pygame.math.Vector2(self.rect.center)

        result = player - enemy
        distance = result.magnitude()

        if distance > 0:
            angle = result.normalize()
        else:
            angle = pygame.math.Vector2()

        return distance, angle

    def getStatus(self, player):
        distance, angle = self.getPlayerDistanceAngle(player)

        if distance <= self.attackRad and self.canAttack:
            if self.status != 'attack':
                self.frameIndex = 0
            self.status = 'attack'

        elif distance <= self.noticeRad:
            self.status = 'move'

        else:
            self.status = 'idle'

    def animate(self):
        animationFrames = self.animations[self.status]
        self.frameIndex += self.animationSpeed

        if self.frameIndex >= len(animationFrames):
            if self.status == 'attack':
                self.canAttack = False
            self.frameIndex = 0

        self.image = animationFrames[int(self.frameIndex)]
        self.rect = self.image.get_rect(center=self.hBox.center)

        if not self.vulnerable:
            alpha = self.waveValue()
            self.image.set_alpha(alpha)

        else:
            self.image.set_alpha(255)

    def cooldowns(self):
        currentTime = pygame.time.get_ticks()
        lengthOfAttack = self.animationSpeed * len(self.animations[self.status])

        if not self.canAttack:
            if currentTime - self.attackTime >= lengthOfAttack + 400:
                self.canAttack = True
                self.attackTime = None
                
        if not self.vulnerable:
            if currentTime - self.attackedTime >= 500:
                self.vulnerable = True
                self.attackedTime = None

    def getDamage(self, player, attackType):
        if self.vulnerable:
            self.direction = self.getPlayerDistanceAngle(player)[1]
            if attackType == 'weapon':
                self.health -= player.getWeaponDamage()

                print(f'{self.name} hit with {player.weapon} ({player.getWeaponDamage()}), now has {self.health} hp')

            else:  # Magic Damage
                self.health -= player.getMagicDamage()
            
            self.attackedTime = pygame.time.get_ticks()
            self.vulnerable = False
        
        return self.health
    
    def checkDeath(self):
        if self.health <= 0:
            self.deathEffect(self.rect.center, self.name)
            self.addExp(self.exp)
            self.kill()

    def knockback(self):
        if not self.vulnerable:
            self.direction *= -self.res

    def action(self, player):
        if self.status == 'attack':
            self.attackTime = pygame.time.get_ticks()
            self.damagePlayer(self.attackDMG, self.attackType)

        elif self.status == 'move':
            self.direction = self.getPlayerDistanceAngle(player)[1]

        else:
            self.direction = pygame.math.Vector2()

    def update(self):
        self.knockback()
        self.move(self.speed)
        self.animate()
        self.cooldowns()
        self.checkDeath()

    def enemyUpdate(self, player):
        self.getStatus(player)
        self.action(player)
