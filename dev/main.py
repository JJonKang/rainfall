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
smaller_basic_font = pygame.font.Font('font/Tiny5-Regular.ttf', 25)
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

wall_bonk = pygame.mixer.Sound('audio/bonk.wav')

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
#                           SETTING UP/FOUNDATIONS
#                            
#
def nothing():
    pass

#================================================================================
#
#
#                                  TEXT
#                            
#

#mainly for instructions on how to play
def instructions():
    screen.blit(text_surf, text_rect)
    help_items = {'WASD or ARROWS to MOVE':'move',
                  'F or J to BOOST':'dash',
                  'E or K to FOCUS':'focus',
                  'Space to INTERACT':'interact'}
    y_offset = 0
    for text, req in help_items.items():
        if req in player.get_req():
            line_color = "#73C655"
        else:
            line_color = 'white'
        help_surf = smaller_basic_font.render(text, False, line_color)
        help_rect = help_surf.get_rect(center = (400, 362 + y_offset))
        y_offset += 25
        screen.blit(help_surf, help_rect)

#cooldown visualization text
def cd_visualization():
    cd_text_surf = smaller_basic_font.render(str((player.get_cooldown() + 59) // 60), False, 'white')
    cd_text_rect = cd_text_surf.get_rect(center = (770, 34))
    screen.blit(cd_text_surf, cd_text_rect)

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
    play_button_rect, help_button_rect = buttons.intro(screen)    

    #instructions text
    instructions()

    #controlling the player
    keys = pygame.key.get_pressed()
    player.movement(keys, wall_rects) #note the wall_rects for future reference, not sure if it'll need to be removed later
    player.object(screen)

    #boost cooldown visual
    cd_visualization()

    #collision checks and wall sound
    if player.bonk_cd != 0:
        player.bonk_cd -= 1

    if player_rect.colliderect(play_button_rect) and keys[pygame.K_SPACE]:
        text_surf = basic_font.render('click 1', False, "#270061")
        text_rect = text_surf.get_rect(center = (400, 50))
        player.set_req('interact')
    elif player_rect.colliderect(help_button_rect) and keys[pygame.K_SPACE]:
        text_surf = basic_font.render('help 1', False, "#1b005b")
        text_rect = text_surf.get_rect(center = (400, 50))
        player.set_req('interact')
    if player.get_collide() == True:
        if player.bonk_cd == 0:
            player.bonk_cd = 60
            wall_bonk.play()
        text_surf = basic_font.render('walled', False, "#741c1c")
        text_rect = text_surf.get_rect(center = (400, 50))
        player.set_collide(False)

    #don't touch
    pygame.display.update()
    clock.tick(60) #60 fps