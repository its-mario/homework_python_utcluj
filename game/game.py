# Example file showing a circle moving on screen
import pygame

from entities import *

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
pygame.display.set_caption("Dino")

# loading the things
player_pos = pygame.Vector2(
    screen.get_width() / 2,
    screen.get_height() / 2
)

player = Player(
    'assets/player/DinoSprites_vita_idl.png',
    player_pos,
    height=50,
    width=50
)
#
# bg = pygame.image.load()
background = Background(
    "assets/background/1.png",
    [0, 0],
    screen.get_rect()
)

floor = Floor(
    height=screen.get_height(),
    width=screen.get_width()
)

obstacle_1 = Obstacle(
    height=screen.get_height(),
    width=screen.get_width(),
)

all_sprites = pygame.sprite.Group()
all_sprites.add(floor)
all_sprites.add(player)

obstacles = pygame.sprite.Group()
obstacles.add(player)
obstacles.add(obstacle_1)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            player.jump()
        if event.type == LOSE_EVENT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    # screen.fill("purple")

    screen.fill([255, 255, 255])
    screen.blit(background.surf, background.rect)

    player.move(dt)
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    obstacle_1.move(dt)
    for entity in obstacles:
        screen.blit(entity.surf, entity.rect)

    all_sprites.update()
    obstacles.update()

    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
