import pygame

class UI:
    def __init__(self):
        self.display_surf = pygame.display.get_surface()

        # load data
        self.inventory_box_image = \
            pygame.image.load('../graphics/ui/inventory_block_1.png').convert_alpha()

    def inventory_box(self,pos):
        height = self.inventory_box_image.get_height() * 2
        width = self.inventory_box_image.get_width() * 2
        image_scaled = pygame.transform.scale(self.inventory_box_image,(height,width))
        rect = image_scaled.get_rect(topleft = pos)

        self.display_surf.blit(image_scaled,rect)

    def display(self,player):
        for i in range(6):
            pos = (539+(i*34),670)
            self.inventory_box(pos)
