# Example file showing a circle moving on screen
import math

import pygame

from entities import *

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
start_time = pygame.time.get_ticks()
score = 0
pygame.display.set_caption("Dino")
height = screen.get_height()
width = screen.get_width()

# loading the things
player_pos = pygame.Vector2(
    width / 2,
    height / 2
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
    height=height,
    width=width
)

obstacle_1 = Obstacle(
    height=height,
    width=width,
)


all_entities = pygame.sprite.Group()
all_entities.add(floor)
all_entities.add(player)
all_entities.add(obstacle_1)

score_font = pygame.font.Font("assets/fonts/Tiny5-Regular.ttf", 64)

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
    score = ((pygame.time.get_ticks() - start_time) // 1000) * 100
    score_rendered = score_font.render(f"Score = {score}", 1, (255, 255, 255))

    screen.blit(score_rendered, (width/2 - 100, 100))
    player.move(dt)
    obstacle_1.move(dt)

    for entity in all_entities:
        screen.blit(entity.surf, entity.rect)

    all_entities.update()

    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
