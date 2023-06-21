import pygame


class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, group):
        super().__init__(group)
        direction = player.status.split("_")[0]

        self.image = pygame.image.load(f'../res/weapons/{player.weapon}/{direction}.png').convert_alpha()

        self.spriteType = 'weapon'

        if direction == 'right':
            self.rect = self.image.get_rect(midleft=player.rect.midright + pygame.math.Vector2(0, 16))

        elif direction == 'left':
            self.rect = self.image.get_rect(midright=player.rect.midleft + pygame.math.Vector2(0, 16))

        if direction == 'up':
            self.rect = self.image.get_rect(midbottom=player.rect.midtop + pygame.math.Vector2(-16, 0))

        elif direction == 'down':
            self.rect = self.image.get_rect(midtop=player.rect.midbottom + pygame.math.Vector2(-16, 0))
