import pygame
from settings import TILESIZE
from support import import_csv_layout
from player import Player
from tile import Tile
from ui import UI

class Level:
    def __init__(self):

        # get the display surface
        self.display_surf = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.objects_sprites = pygame.sprite.Group()

        # create map
        self.create_map()

        self.ui = UI()

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('../map/map_FloorBlocks.csv'),
            'floor': import_csv_layout('../map/map_Floor.csv'),
            'objects': import_csv_layout('../map/map_Objects.csv')
        }

        objects = {
            'acquaintance': pygame.image.load('../graphics/objects/acquaintance/acquaintance_1.png').convert_alpha(),
            'mushroom': pygame.image.load('../graphics/objects/mushroom.png').convert_alpha(),
            'potion': pygame.image.load('../graphics/objects/potion.png').convert_alpha(),
        }

        for layout_key, layout_value in layouts.items():
            for row_index, row in enumerate(layout_value):
                for col_index, col in enumerate(row):
                    x = col_index * TILESIZE
                    y = row_index * TILESIZE
                    if layout_key == 'boundary':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if col == '0':
                            Tile((x,y),[self.obstacle_sprites],surf=pygame.Surface((4,4)))

                    if layout_key == 'objects':
                        if col == '1':  # Acquaintance
                            Tile((x,y),
                                 [self.visible_sprites,self.obstacle_sprites],
                                 objects['acquaintance'])
                        elif col == '2':  # Mushroom
                            Tile((x, y),
                                 [self.visible_sprites],
                                 objects['mushroom'])
                        elif col == '3':  # Potion
                            Tile((x, y),
                                 [self.visible_sprites,self.obstacle_sprites],
                                 objects['potion'])
                            print('potion:',x,y)
                        elif col == '4':  # Player
                            self.player = Player((x,y),
                                                 [self.visible_sprites],
                                                 self.obstacle_sprites)
                            print('player:',x,y)

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.ui.display(self.player)


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_width() // 2
        self.half_height = self.display_surface.get_height() // 2
        self.offset = pygame.math.Vector2()

        # creating the floor
        self.floor_surf = pygame.image.load('../graphics/tilemap/ground_2.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

    def custom_draw(self,player):

        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf,floor_offset_pos)

        # drawing the sprites
        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_rect = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_rect)
