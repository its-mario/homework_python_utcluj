import pygame
from pygame.locals import *
import sys

ACC = 0.5
FRIC = -0.12
FPS = 60

vec = pygame.math.Vector2


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location, react: pygame.Rect):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        picture = pygame.image.load(image_file)
        surface = pygame.transform.scale(picture, (react.width, react.height))
        self.surf = surface
        self.rect = react
        self.rect.left, self.rect.top = location

    def move(self, dt: float):
        pass


class Floor(pygame.sprite.Sprite):
    def __init__(self, height: float, width: float):
        super().__init__()
        self.surf = pygame.Surface((width, height/4))
        self.surf.fill((182, 255, 0))
        self.rect = self.surf.get_rect(midbottom=( width/2 , height))

    def move(self, dt: float):
        pass


class Player(pygame.sprite.Sprite):
    def __init__(self, image_file, position, width: int, heigth: int):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        picture = pygame.image.load(image_file)
        self.surf = pygame.transform.scale(picture, (width, heigth))
        self.rect = self.surf.get_rect()
        self.rect.left, self.rect.top = position

        self.width = width
        self.height = heigth
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.pos = vec(50, 100)

    def update(self):
        pass
        # getting groups in wich the player exists it should be only one
        groups = self.groups()

        # getting the group
        group = groups[0]
        hits = pygame.sprite.spritecollide(self, group, False)
        if self.vel.y > 0:
            if len(hits) > 1:
                self.vel.y = 0
                self.pos.y = hits[0].rect.top + 1

    def move(self, dt: float):
        self.acc = vec(0, 0)

        self.acc.y = 9.18
        self.vel += self.acc * dt
        self.pos += self.vel

        self.rect.midbottom = self.pos
