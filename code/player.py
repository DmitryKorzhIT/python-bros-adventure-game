import pygame
from settings import PLAYER_MULTIPLIER
from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,groups,obstacle_sprites):
        super().__init__(groups)

        # image
        self.image = pygame.image.load('../graphics/player/down/down_1.png').convert_alpha()
        image_width = self.image.get_width()
        image_height = self.image.get_height()
        self.image = pygame.transform.scale(self.image,
            (image_width * PLAYER_MULTIPLIER, image_height * PLAYER_MULTIPLIER))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0,-6)

        # graphics setup
        self.import_player_assets()
        self.status = 'down'

        # animation
        self.frame_index = 0
        self.animation_speed = 0.11

        # movement
        self.direction = pygame.math.Vector2()
        self.speed = 3 # int(2)  # if put a float, then movement speed will be different
        self.obstacle_sprites = obstacle_sprites

    def import_player_assets(self):
        path = '../graphics/player/'
        self.animations = {'up': [],'down': [],'left': [],'right': [],
                           'up_idle': [],'down_idle': [],'left_idle': [],'right_idle': [],
                           'up_attack': [],'down_attack': [],'left_attack': [],'right_attack': [],
                           'up_sleep': [],'down_sleep': [],'left_sleep': [],'right_sleep': []
                           }
        for animation_key, animation_val in self.animations.items():
            animations = import_folder(f'{path}{animation_key}/')
            animations_scaled = []

            # scale each image in self.animations
            for image in animations:
                image_w = image.get_width()
                image_h = image.get_height()
                image_scaled = pygame.transform.scale(image,
                    (image_w*PLAYER_MULTIPLIER,image_h*PLAYER_MULTIPLIER))
                animations_scaled.append(image_scaled)

            self.animations[animation_key] = animations_scaled

    def input(self):
        keys = pygame.key.get_pressed()

        # movement input
        if keys[pygame.K_w]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_s]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0

        if keys[pygame.K_a]:
            self.direction.x = -1
            self.status = 'left'
        elif keys[pygame.K_d]:
            self.direction.x = 1
            self.status = 'right'
        else:
            self.direction.x = 0

    def move(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.y += self.direction.y * self.speed
        self.collision('vertical')
        self.hitbox.x += self.direction.x * self.speed
        self.collision('horizontal')
        self.rect.center = self.hitbox.center

    def collision(self,direction):
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:  # moving up
                        self.hitbox.top = sprite.hitbox.bottom
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # moving left
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:  # moving right
                        self.hitbox.left = sprite.hitbox.right

    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status:
                self.status += '_idle'

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed

        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def update(self):
        self.input()
        self.get_status()
        self.animate()
        self.move()
