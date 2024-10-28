import pygame

vec = pygame.math.Vector2
LOSE_EVENT = pygame.USEREVENT + 1


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location, react: pygame.Rect):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        picture = pygame.image.load(image_file)
        surface = pygame.transform.scale(picture, (react.width, react.height))
        self.surf = surface
        self.rect = react
        self.rect.left, self.rect.top = location


class Floor(pygame.sprite.Sprite):
    def __init__(self, height: float, width: float):
        super().__init__()
        self.surf = pygame.Surface((width, height / 4))
        self.surf.fill((182, 255, 0))
        self.rect = self.surf.get_rect(midbottom=(width / 2, height))


class Player(pygame.sprite.Sprite):
    def __init__(
            self,
            image_file,
            position,
            width: int,
            height: int,
    ):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        picture = pygame.image.load(image_file)
        self.surf = pygame.transform.scale(picture, (width, height))
        self.rect = self.surf.get_rect()
        self.rect.left, self.rect.top = position

        self.width = width
        self.height = height
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.pos = vec(200, 100)
        self.jumping = True

    def update(self):
        # getting groups in which the player exists it should be only one
        groups = self.groups()

        # !!! Attention this function is poorly writen and should be implemented in other way,
        #  but for now this is only reasonable implementation.

        group = groups[0]
        hits = pygame.sprite.spritecollide(self, group, False)
        if self.vel.y > 0:
            if len(hits) > 1:
                self.vel.y = 0
                self.pos.y = hits[0].rect.top + 1
                self.jumping = False

        if len(groups) == 2:
            group = groups[1]
            hits = pygame.sprite.spritecollide(self, group, False)

            if len(hits) > 1:
                event = pygame.event.Event(LOSE_EVENT, {})
                pygame.event.post(event)

    def move(self, dt: float):
        self.acc = vec(0, 0)

        self.acc.y = 9.18
        self.vel += self.acc
        self.pos += self.vel * dt
        self.rect.midbottom = self.pos

    def jump(self):
        if not self.jumping:
            self.vel += (0, -500)
            self.jumping = True


class Obstacle(pygame.sprite.Sprite):

    def __init__(self, width: int, height: int, moving_speed=-500):
        super().__init__()
        self.surf = pygame.Surface((50, 100))
        self.surf.fill((182, 255, 0))
        self.pos = vec(width, height * 3 / 4)
        self.rect = self.surf.get_rect()
        self.rect.left, self.rect.top = self.pos

        self.moving_speed = moving_speed
        self.screen_with = width,
        self.screen_height = height,

    def move(self, dt: float):
        self.pos += vec(self.moving_speed * dt, 0.0)
        self.rect.midbottom = self.pos

        if self.pos.x <= 0:
            print(self.screen_with)
            self.pos.x = self.screen_with[0]
