import pygame
import buttons as buttons
import controls as controls
from sys import exit #true exit program

pygame.init()
screen = pygame.display.set_mode((800, 500))
pygame.display.set_caption("something special")
icon = pygame.image.load('images/rain.jpg')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

player = controls.Player()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.fill('black')
    buttons.intro(screen)
    #controlling the player
    keys = pygame.key.get_pressed()
    player.movement(keys)
    player.object(screen)
    player.get_pos()
    pygame.display.update()
    clock.tick(60)