#Rainfall's main file

#importing from controls and buttons
import pygame
import buttons as buttons
import controls as controls
from sys import exit #true exit program

#initializing and starting up the program
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

#horiz walls
wall_surf_hor = pygame.Surface((800, 20)).convert()
wall_surf_hor.fill("#371138")
top_wall_rect = wall_surf_hor.get_rect(center = (400, 10))
bot_wall_rect = wall_surf_hor.get_rect(center = (400, 490))

#vert walls
wall_surf_vert = pygame.Surface((20, 500)).convert()
wall_surf_vert.fill("#371138")
left_wall_rect = wall_surf_vert.get_rect(center = (10, 250))
right_wall_rect = wall_surf_vert.get_rect(center = (790, 250))

#use this for collision checks for walls
wall_rects = [top_wall_rect, bot_wall_rect, left_wall_rect, right_wall_rect]


#================================================================================
#
#
#                                MAIN LOOP
#
#
while True:
    for event in pygame.event.get():
        #exits the game
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    #sets up the background
    screen.fill('black')
    screen.blit(wall_surf_hor, top_wall_rect)
    screen.blit(wall_surf_hor, bot_wall_rect)
    screen.blit(wall_surf_vert, left_wall_rect)
    screen.blit(wall_surf_vert, right_wall_rect)

    #buttons variables
    play_rect, help_rect = buttons.intro(screen)

    #text
    screen.blit(text_surf, text_rect)

    #controlling the player
    keys = pygame.key.get_pressed()
    player.movement(keys)
    player.object(screen)

    #collision checks
    if player_rect.colliderect(play_rect) and keys[pygame.K_SPACE]:
        text_surf = basic_font.render('click 1', False, "#270061")
        text_rect = text_surf.get_rect(center = (400, 50))
    elif player_rect.colliderect(help_rect) and keys[pygame.K_SPACE]:
        text_surf = basic_font.render('help 1', False, "#1b005b")
        text_rect = text_surf.get_rect(center = (400, 50))

    if (player_rect.colliderect(bot_wall_rect) or
        player_rect.colliderect(top_wall_rect) or
        player_rect.colliderect(left_wall_rect) or
        player_rect.colliderect(right_wall_rect)):
        player.set_x(0)
        player.set_y(0)
        player.set_deny(True)
        text_surf = basic_font.render('walled', False, "#741c1c")
        text_rect = text_surf.get_rect(center = (400, 50))

    #don't touch
    pygame.display.update()
    clock.tick(60) #60 fps