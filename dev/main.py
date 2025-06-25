import pygame
import buttons as buttons
import controls as controls
from sys import exit #true exit program

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("something special")
icon = pygame.image.load('images/rain.jpg')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    buttons.intro(screen)
    pygame.display.update()
    clock.tick(60)