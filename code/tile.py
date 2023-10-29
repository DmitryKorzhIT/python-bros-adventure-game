import pygame
from settings import TILESIZE, PLAYER_MULTIPLIER

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,groups,surf=pygame.Surface((TILESIZE,TILESIZE))):
        super().__init__(groups)

        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-2)
