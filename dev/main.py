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

#text
basic_font = pygame.font.Font('font/Tiny5-Regular.ttf', 50)
text_surf = basic_font.render('default 0', False, 'white')
text_rect = text_surf.get_rect(center = (400, 50))

#player default
player = controls.Player()
player_rect = player.rect

#================================================================================
#
#
#                                MAIN LOOP
#
#
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.fill('black')
    play_rect, help_rect = buttons.intro(screen)

    #text
    screen.blit(text_surf, text_rect)

    #controlling the player
    keys = pygame.key.get_pressed()
    player.movement(keys)
    player.object(screen)

    if player_rect.colliderect(play_rect) and keys[pygame.K_SPACE]:
        text_surf = basic_font.render('click 1', False, "#270061")
        text_rect = text_surf.get_rect(center = (400, 50))

    elif player_rect.colliderect(help_rect) and keys[pygame.K_SPACE]:
        text_surf = basic_font.render('help 1', False, "#1b005b")
        text_rect = text_surf.get_rect(center = (400, 50))


    #don't touch
    pygame.display.update()
    clock.tick(60)