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
    def __init__(self, image_file: str, height: float, width: float, id: int):
        super().__init__()
        picture = pygame.image.load(image_file)
        surf = pygame.Surface((picture.get_width() * 20, height / 4))
        for i in range(20):
            surf.blit(picture, (i * picture.get_width(), 0))
        self.surf = surf
        self.rect = self.surf.get_rect()
        self.rect.bottomleft = vec(id * self.rect.width, height)

        self.screen_width = width
        self.screen_height = height

    def move(self, dt: float, moving_speed: float) -> None:
        if self.rect.bottomright[0] <= 0:
            print(self.screen_width)
            self.rect.bottomleft = vec(self.rect.width, self.rect.bottomleft[1])
        self.rect.bottomleft += vec(moving_speed * dt, 0.0)


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
        group = groups[0]
        hits = pygame.sprite.spritecollide(self, group, False)
        for hit in hits:
            if isinstance(hit, Floor) and self.vel.y >= 0:
                self.vel.y = 0
                self.pos.y = hits[0].rect.top + 1
                self.jumping = False

            if isinstance(hit, Obstacle):
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

    def __init__(self, width: int, height: int):
        super().__init__()
        self.surf = pygame.Surface((50, 100))
        self.surf.fill((182, 255, 0))
        self.rect = self.surf.get_rect()
        self.rect.bottomleft = vec(width, height * 3 / 4)

        self.screen_with = width,
        self.screen_height = height,

    def move(self, dt: float, moving_speed: float):
        self.rect.midbottom += vec(moving_speed * dt, 0.0)

        if self.rect.bottomright[0] <= 0:
            print(self.screen_with)
            self.rect.bottomleft = vec(self.screen_with[0], self.rect.bottomleft[1])
