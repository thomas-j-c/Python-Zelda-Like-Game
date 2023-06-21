import pygame

from game.main.enemy import Enemy
from settings import *
from tile import Tile
from player import Player
from debug import debug
from weapon import Weapon
import util
from ui import UI
from particleEffects import *
from magic import MagicPlayer
from upgrade import Upgrade

import random


class Level:
    def __init__(self):

        self.visibleSprites = YSortCameraGroup()
        self.obstacleSprite = pygame.sprite.Group()

        self.currentAttack = None
        self.attackSprites = pygame.sprite.Group()
        self.attackableSprites = pygame.sprite.Group()

        self.createMap()

        self.paused = False
        self.ui = UI()
        self.upgrade = Upgrade(self.player)

        self.animationPlayer = Animation()
        self.magicPlayer = MagicPlayer(self.animationPlayer)

    def createMap(self):
        layout = {
            "boundary": util.importCSVLayout("../map/map_FloorBlocks.csv"),
            "grass": util.importCSVLayout("../map/map_Grass.csv"),
            "object": util.importCSVLayout("../map/map_Objects.csv"),
            'entities': util.importCSVLayout('../map/map_Entities.csv')
        }

        graphics = {
            "grass": util.importFolder("../res/grass"),
            "objects": util.importFolder("../res/objects")
        }

        for style, world in layout.items():
            for rowIndex, row in enumerate(world):
                for colIndex, col in enumerate(row):
                    if col != '-1':
                        x = colIndex * TILESIZE
                        y = rowIndex * TILESIZE

                        if style == 'boundary':
                            Tile((x, y), [self.obstacleSprite], "nonVis")

                        elif style == "grass":
                            listOfGraphics = graphics.get("grass")
                            Tile((x, y),
                                 [self.visibleSprites, self.obstacleSprite, self.attackableSprites],
                                 "grass",
                                 random.choice(listOfGraphics))

                        elif style == "object":
                            surf = graphics.get("objects")
                            Tile((x, y), [self.visibleSprites, self.obstacleSprite],
                                 "object", surf[int(col)])

                        elif style == 'entities':
                            if col == '394':
                                self.player = Player((x, y), [self.visibleSprites], self.obstacleSprite, self.createWeapon,
                                                     self.destroyWeapon, self.createMagic)
                            elif col == '390':
                                Enemy('bamboo', (x, y),
                                      [self.visibleSprites, self.attackableSprites],
                                      self.obstacleSprite,
                                      self.damagePlayer,
                                      self.triggerDeathParticles,
                                      self.addExp)

                            elif col == '391':
                                Enemy('spirit', (x, y),
                                      [self.visibleSprites, self.attackableSprites],
                                      self.obstacleSprite, self.damagePlayer,
                                      self.triggerDeathParticles,
                                      self.addExp)

                            elif col == '392':
                                Enemy('raccoon', (x, y),
                                      [self.visibleSprites, self.attackableSprites],
                                      self.obstacleSprite,
                                      self.damagePlayer,
                                      self.triggerDeathParticles,
                                      self.addExp)

    def playerAttack(self):
        if self.attackSprites:
            for attack in self.attackSprites:
                collided = pygame.sprite.spritecollide(attack, self.attackableSprites, False)
                if collided:
                    for target in collided:
                        if target.spriteType == 'grass':
                            pos = target.rect.center - pygame.math.Vector2(0, 50)
                            for leaf in range(random.randint(4, 8)):
                                self.animationPlayer.grassParticles(pos, [self.visibleSprites])
                            target.kill()

                        else:
                            target.getDamage(self.player, attack.spriteType)

    def damagePlayer(self, value, attackType):
        if self.player.vulnerable:
            self.player.hp -= value
            self.player.vulnerable = False
            self.player.hurtTime = pygame.time.get_ticks()

            self.animationPlayer.generateParticles(self.player.rect.center, attackType, [self.visibleSprites])

    def triggerDeathParticles(self, pos, monster):
        self.animationPlayer.generateParticles(pos, monster, [self.visibleSprites])

    def createWeapon(self):
        self.currentAttack = Weapon(self.player, [self.visibleSprites, self.attackSprites])

    def createMagic(self, style, strength, cost):
        if style == 'heal':
            self.animationPlayer.generateParticles(self.player.rect.center, 'heal', [self.visibleSprites])
            self.animationPlayer.generateParticles(self.player.rect.center, 'aura', [self.visibleSprites])
            self.magicPlayer.heal(self.player, strength, cost, [self.visibleSprites])

        else:
            self.magicPlayer.flame(self.player, strength, cost, [self.visibleSprites, self.attackSprites])

    def addExp(self, value):
        self.player.exp += value

    def destroyWeapon(self):
        if self.currentAttack:
            self.currentAttack.kill()

        self.currentAttack = None

    def toggleMenu(self):
        self.paused = not self.paused

    def run(self):
        self.visibleSprites.__draw__(self.player)
        self.ui.display(self.player)

        if self.paused:
            self.upgrade.displayMenu()
        else:
            self.visibleSprites.update()
            self.visibleSprites.enemyUpdate(self.player)
            self.playerAttack()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        self.displaySurface = pygame.display.get_surface()
        self.middle = (self.displaySurface.get_size()[0] // 2, self.displaySurface.get_size()[1] // 2)
        self.camera = pygame.math.Vector2()

        self.floorImage = pygame.image.load("../res/tilemap/ground.png").convert()
        self.floorRect = self.displaySurface.get_rect(topleft=(0, 0))

    def __draw__(self, player):
        # Always draws the player in the centre of the screen
        self.camera.x = player.rect.centerx - self.middle[0]
        self.camera.y = player.rect.centery - self.middle[1]

        # Display the map
        self.displaySurface.blit(self.floorImage, self.floorRect.topleft - self.camera)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            newPos = sprite.rect.topleft - self.camera
            self.displaySurface.blit(sprite.image, newPos)

    def enemyUpdate(self, player):
        # Gets all the enemy sprites
        enemySprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'spriteType') and sprite.spriteType == 'enemy']

        for enemy in enemySprites:
            enemy.enemyUpdate(player)
