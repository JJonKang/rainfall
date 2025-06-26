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
#                                DEFUNCT
#                            Wall Collision
#
#
def wall_collision():
    for wall in wall_rects:
        if player_rect.colliderect(wall):
            #top wall and bottom wall collision checks
            if wall == top_wall_rect or wall == bot_wall_rect:
                if player_rect.centery < wall.centery:
                    player.set_y(wall.top - player_rect.height)
                else:
                    player.set_y(wall.bottom)
                text_surf = basic_font.render('walled', False, "#741c1c")
                text_rect = text_surf.get_rect(center = (400, 50))

            #left wall and right wall collision checks
            if wall == left_wall_rect or wall == right_wall_rect:
                if player_rect.centerx < wall.centerx:
                    player.set_x(wall.left - player_rect.width)
                else:
                    player.set_x(wall.right)
                text_surf = basic_font.render('walled', False, "#741c1c")
                text_rect = text_surf.get_rect(center = (400, 50))

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
    player.movement(keys, wall_rects) #note the wall_rects for future reference, not sure if it'll need to be removed later
    player.object(screen)

    #collision checks
    if player_rect.colliderect(play_rect) and keys[pygame.K_SPACE]:
        text_surf = basic_font.render('click 1', False, "#270061")
        text_rect = text_surf.get_rect(center = (400, 50))
    elif player_rect.colliderect(help_rect) and keys[pygame.K_SPACE]:
        text_surf = basic_font.render('help 1', False, "#1b005b")
        text_rect = text_surf.get_rect(center = (400, 50))
    if player.get_collide() == True:
        text_surf = basic_font.render('walled', False, "#741c1c")
        text_rect = text_surf.get_rect(center = (400, 50))
        player.set_collide(False)

    #don't touch
    pygame.display.update()
    clock.tick(60) #60 fps