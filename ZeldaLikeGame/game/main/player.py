import random
import sys

import pygame

from game.main import util
from settings import *
from entity import Entity


class Player(Entity):
    def __init__(self, position, group, obstacleSprites, createAttack, destroyweapon, createMagic):
        super().__init__(group)

        self.vulnerable = True
        self.hurtTime = None

        self.image = pygame.image.load("../res/test/player.png")
        self.rect = self.image.get_rect(topleft=position)

        self.obstacles = obstacleSprites

        self.hBox = self.rect.inflate(-6, HBOXOFFSET['player'])

        self.attacking = False  # Whether the player is attacking
        self.attackTime = None  # The time the player has attacked

        self.canSwitchWeapon = True  # Whether the player can switch weapon
        self.canSwitchMagic = True
        self.switchTime = None  # The time the player switched weapon

        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'up_idle': [], 'down_idle': [], 'right_idle': [], 'left_idle': [],
                           'up_attack': [], 'down_attack': [], 'right_attack': [], 'left_attack': []
                           }

        self.getAssets()  # Gets the sprites for the player's directions
        self.status = 'up'  # The current direction for the player

        # Using parameter methods allows the weapon to be created and destroyed in the
        # level class
        self.spriteForWeapon = createAttack  # Generates the weapon using parameter method
        self.destroySprite = destroyweapon  # Destroys the weapon using parameter method

        self.weaponIndex = random.randint(0, 4)  # Randomly selects an initial weapon
        self.weapon = list(weapons.keys())[self.weaponIndex]  # Gets the weapon from the index above

        self.spriteForMagic = createMagic
        self.magicIndex = 0
        self.magic = list(magic.keys())[self.magicIndex]

        self.baseStats = {'hp': 100, 'stamina': 60, 'attack': 10, 'magic': 4,
                          'speed': 5}

        self.maxStats = {'hp': 300, 'stamina': 140, 'attack': 20, 'magic': 10,
                         'speed': 10}

        self.upgradeCosts = {'hp': 100, 'stamina': 100, 'attack': 100, 'magic': 150,
                             'speed': 100}

        self.hp = self.baseStats['hp']
        self.stamina = self.baseStats['stamina']
        self.exp = 0
        self.speed = self.baseStats['speed']

        self.dead = False

    def getStatus(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if 'idle' not in self.status and 'attack' not in self.status:
                self.status = self.status + '_idle'

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if 'idle' in self.status:
                self.status = self.status.replace('idle', 'attack')

            if 'attack' not in self.status:
                self.status = self.status + '_attack'

        else:
            if 'attack' in self.status:
                self.status.replace('attack', '')

    def input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            self.direction.y = -1
            self.status = 'up'

        elif pressed[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = 'down'

        else:
            self.direction.y = 0

        if pressed[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = 'left'

        elif pressed[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = 'right'

        else:
            self.direction.x = 0

        # Check attack
        if pressed[pygame.K_z] and not self.attacking:
            self.attacking = True
            self.attackTime = pygame.time.get_ticks()
            self.spriteForWeapon()

        # Check magic
        if pressed[pygame.K_x] and not self.attacking:
            self.attacking = True
            self.attackTime = pygame.time.get_ticks()

            style = list(magic.keys())[self.magicIndex]
            strength = list(magic.values())[self.magicIndex]['strength'] + self.baseStats['magic']
            cost = list(magic.values())[self.magicIndex]['cost']

            self.spriteForMagic(style, strength, cost)

        if pressed[pygame.K_a] and self.canSwitchWeapon:
            self.canSwitchWeapon = False
            self.switchTime = pygame.time.get_ticks()

            self.weaponIndex += 1
            if self.weaponIndex > len(list(weapons.keys())) - 1:
                self.weaponIndex = 0

            self.weapon = list(weapons.keys())[self.weaponIndex]

        if pressed[pygame.K_s] and self.canSwitchMagic:
            self.canSwitchMagic = False
            self.switchTime = pygame.time.get_ticks()

            self.magicIndex += 1
            if self.magicIndex > len(list(magic.keys())) - 1:
                self.magicIndex = 0

            self.magic = list(magic.keys())[self.magicIndex]

    def getWeaponDamage(self):
        return self.baseStats['attack'] + weapons[self.weapon]['dmg']

    def getMagicDamage(self):
        return self.baseStats['magic'] + magic[self.magic]['strength']

    def getValue(self, index):
        return list(self.baseStats.values())[index]

    def getCost(self, index):
        return list(self.upgradeCosts.values())[index]

    def recoverEnergy(self):
        if self.stamina < self.baseStats['stamina']:
            self.stamina += 0.001 * self.baseStats['magic']

        else:
            self.stamina = self.baseStats['stamina']

    def cooldown(self):
        timeOfInput = pygame.time.get_ticks()

        if self.attacking:
            if timeOfInput - self.attackTime >= 250 + weapons[self.weapon]['cd']:
                self.attacking = False
                self.destroySprite()

        if not self.canSwitchWeapon:
            if timeOfInput - self.switchTime >= 100:
                self.canSwitchWeapon = True

        if not self.canSwitchMagic:
            if timeOfInput - self.switchTime >= 100:
                self.canSwitchMagic = True

        if not self.vulnerable:
            if timeOfInput - self.hurtTime >= 500:
                self.vulnerable = True

    def animate(self):
        animationImages = self.animations[self.status]

        self.frameIndex += self.animationSpeed

        if self.frameIndex >= len(animationImages):
            self.frameIndex = 0

        self.image = animationImages[int(self.frameIndex)]
        self.rect = self.image.get_rect(center=self.hBox.center)

        if not self.vulnerable:
            alpha = self.waveValue()
            self.image.set_alpha(alpha)

        else:
            self.image.set_alpha(255)

    def checkDeath(self):
        self.dead = True if self.hp <= 0 else False

    def update(self):
        self.checkDeath()
        if self.dead:

            pygame.quit()
            sys.exit()

        self.input()
        self.cooldown()
        self.getStatus()
        self.animate()
        self.move(self.speed)
        self.recoverEnergy()
