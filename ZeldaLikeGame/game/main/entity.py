from math import sin

import pygame

from game.main import util


class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.animations = None
        self.frameIndex = 0
        self.animationSpeed = 0.1
        self.direction = pygame.math.Vector2()

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hBox.x += self.direction.x * speed
        self.collision('h')
        self.hBox.y += self.direction.y * speed
        self.collision('v')
        self.rect.center = self.hBox.center

    def collision(self, dir):
        if dir == 'h':
            for sprite in self.obstacles:
                if sprite.hBox.colliderect(self.hBox):
                    if self.direction.x > 0:  # moving to the right
                        self.hBox.right = sprite.hBox.left

                    if self.direction.x < 0:  # otherwise, moving left
                        self.hBox.left = sprite.hBox.right

        if dir == 'v':
            for sprite in self.obstacles:
                if sprite.hBox.colliderect(self.hBox):
                    if self.direction.y > 0:  # moving down
                        self.hBox.bottom = sprite.hBox.top

                    else:  # moving up
                        self.hBox.top = sprite.hBox.bottom

    def getAssets(self):
        path = "../res/player"

        for animation in self.animations.keys():
            newPath = path + '/' + animation
            self.animations[animation] = util.importFolder(newPath)

    def waveValue(self):
        val = sin(pygame.time.get_ticks())

        if val >= 0:
            return 255

        else:
            return 0
