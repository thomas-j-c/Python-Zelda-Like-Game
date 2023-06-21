import pygame
import random
from util import importFolder


class Animation:
    def __init__(self):
        self.frames = {
            'flame': importFolder('../res/particles/flame/frames'),
            'aura': importFolder('../res/particles/aura'),
            'heal': importFolder('../res/particles/heal/frames'),

            'claw': importFolder('../res/particles/claw'),
            'slash': importFolder('../res/particles/slash'),
            'sparkle': importFolder('../res/particles/sparkle'),
            'leafAttack': importFolder('../res/particles/leaf_attack'),
            'thunder': importFolder('../res/particles/thunder'),

            'squid': importFolder('../res/particles/smoke_orange'),
            'raccoon': importFolder('../res/particles/raccoon'),
            'spirit': importFolder('../res/particles/nova'),
            'bamboo': importFolder('../res/particles/bamboo'),

            'leaf': (
                importFolder('../res/particles/leaf1'),
                importFolder('../res/particles/leaf2'),
                importFolder('../res/particles/leaf3'),
                importFolder('../res/particles/leaf4'),
                importFolder('../res/particles/leaf5'),
                importFolder('../res/particles/leaf6'),
                self.reflectImg(importFolder('../res/particles/leaf1')),
                self.reflectImg(importFolder('../res/particles/leaf2')),
                self.reflectImg(importFolder('../res/particles/leaf3')),
                self.reflectImg(importFolder('../res/particles/leaf4')),
                self.reflectImg(importFolder('../res/particles/leaf5')),
                self.reflectImg(importFolder('../res/particles/leaf6'))
            )
        }

    def reflectImg(self, frames):
        newFrames = []

        for frame in frames:
            flippedFrame = pygame.transform.flip(frame, True, False)
            newFrames.append(flippedFrame)

        return newFrames

    def grassParticles(self, pos, groups):
        frames = random.choice(self.frames['leaf'])
        ParticleEffect(pos, frames, groups)

    def generateParticles(self, pos, animationType, groups):
        frames = self.frames[animationType]
        ParticleEffect(pos, frames, groups)


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups):
        super().__init__(groups)
        self.spriteType = 'magic'
        self.frameIndex = 0
        self.animationSpeed = 0.1
        self.frames = frames
        self.image = frames[self.frameIndex]

        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        self.frameIndex += self.animationSpeed

        if self.frameIndex >= len(self.frames):
            self.kill()

        else:
            self.image = self.frames[int(self.frameIndex)]

    def update(self):
        self.animate()
