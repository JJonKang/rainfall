#Rainfall's main file

#importing from controls and buttons
import pygame
import buttons as buttons
import chars as chars
from sys import exit #true exit program

#================================================================================
#
#
#                           MAIN CLASS
#                            
#
class Game():
    def __init__(self):
        #initializing and starting up the program
        pygame.init()
        self.screen = pygame.display.set_mode((800, 500))
        pygame.display.set_caption("something special")
        icon = pygame.image.load('images/rain.jpg')
        pygame.display.set_icon(icon)
        self.clock = pygame.time.Clock()

        #text starter
        self.basic_font = pygame.font.Font('font/Tiny5-Regular.ttf', 50)
        self.smaller_basic_font = pygame.font.Font('font/Tiny5-Regular.ttf', 25)
        self.text_surf = self.basic_font.render('default 0', False, 'white')
        self.text_rect = self.text_surf.get_rect(center = (400, 50))

        #player default
        self.player = chars.Player()
        #enemy default
        self.enemy = chars.Enemy()

        #horiz walls
        self.wall_surf_hor = pygame.Surface((800, 20)).convert()
        self.wall_surf_hor.fill("#371138")
        self.top_wall_rect = self.wall_surf_hor.get_rect(center = (400, 10))
        self.bot_wall_rect = self.wall_surf_hor.get_rect(center = (400, 490))

        #vert walls
        self.wall_surf_vert = pygame.Surface((20, 500)).convert()
        self.wall_surf_vert.fill("#371138")
        self.left_wall_rect = self.wall_surf_vert.get_rect(center = (10, 250))
        self.right_wall_rect = self.wall_surf_vert.get_rect(center = (790, 250))

        #use this for collision checks for walls
        self.wall_rects = [self.top_wall_rect, self.bot_wall_rect, self.left_wall_rect, self.right_wall_rect]

        #currently unused
        self.wall_bonk = pygame.mixer.Sound('audio/bonk.wav')

    #play text
    def play_text(self):
        play_text_surf = self.smaller_basic_font.render('PLAY', False, 'white')
        play_text_rect = play_text_surf.get_rect(center = (400, 200))
        self.screen.blit(play_text_surf, play_text_rect)

    #mainly for instructions on how to play
    def instructions(self):
        self.screen.blit(self.text_surf, self.text_rect)
        help_items = {'WASD or ARROWS to MOVE':'move',
                    'F or J to BOOST':'dash',
                    'E or K to FOCUS':'focus',
                    'Space to INTERACT':'interact'}
        y_offset = 0
        instruction_clear = 0
        for text, req in help_items.items():
            if req in self.player.get_req():
                instruction_clear += 1
                line_color = "#73C655"
            else:
                line_color = 'white'
            help_surf = self.smaller_basic_font.render(text, False, line_color)
            help_rect = help_surf.get_rect(center = (400, 362 + y_offset))
            y_offset += 25
            self.screen.blit(help_surf, help_rect)
        return instruction_clear == 4

    #cooldown visualization text
    def cd_visualization(self):
        cd_text_surf = self.smaller_basic_font.render(str((self.player.get_cooldown() + 59) // 60), False, 'white')
        cd_text_rect = cd_text_surf.get_rect(center = (770, 34))
        self.screen.blit(cd_text_surf, cd_text_rect)

    def health_visualization(self):
        health_text_surf = self.smaller_basic_font.render(str(self.player.get_health()), False, 'white')
        health_text_rect = health_text_surf.get_rect(center = (30, 34))
        self.screen.blit(health_text_surf, health_text_rect)

    def run(self):
        while True:
            for event in pygame.event.get():
                #exits the game
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            #sets up the background
            self.screen.fill('black')
            self.screen.blit(self.wall_surf_hor, self.top_wall_rect)
            self.screen.blit(self.wall_surf_hor, self.bot_wall_rect)
            self.screen.blit(self.wall_surf_vert, self.left_wall_rect)
            self.screen.blit(self.wall_surf_vert, self.right_wall_rect)

            #buttons variables
            play_button_rect, help_button_rect = buttons.intro(self.screen)    

            #instructions text
            self.play_text()
            proceed = self.instructions()

            #enemy spawn and projectile checks/spawn
            if(self.enemy.get_spawn() == True):
                self.enemy.object(self.screen)
                if self.enemy.get_bullet_timer() > 0:
                    self.enemy.bullet_update(self.screen, self.player)
                    self.enemy.set_bullet_timer_reduction(1)
                else:
                    self.enemy.shoot(18)        

            #controlling the player
            keys = pygame.key.get_pressed()
            self.player.movement(keys, self.wall_rects) #note the wall_rects for future reference, not sure if it'll need to be removed later
            self.player.object(self.screen)

            #boost cooldown visual and health visual
            self.cd_visualization()
            self.health_visualization()

            #collision checks and wall sound
            # if player.bonk_cd != 0:
            #     player.bonk_cd -= 1
            player_rect = self.player.get_rect()
            if player_rect.colliderect(play_button_rect) and keys[pygame.K_SPACE]:
                if proceed == True:
                    self.text_surf = self.basic_font.render('START', False, "#270061")
                    self.player.set_req('interact')
                    self.enemy.set_spawn(True)
                else:
                    self.text_surf = self.basic_font.render('FINISH INSTRUCTIONS', False, "#270061")
                    self.player.set_req('interact')
                self.text_rect = self.text_surf.get_rect(center = (400, 50))
            elif player_rect.colliderect(help_button_rect) and keys[pygame.K_SPACE]:
                self.text_surf = self.basic_font.render('help 1', False, "#1b005b")
                self.text_rect = self.text_surf.get_rect(center = (400, 50))
                self.player.set_req('interact')
            if self.player.get_collide() == True:
                # if player.bonk_cd == 0:
                #     player.bonk_cd = 60
                #     wall_bonk.play()
                self.text_surf = self.basic_font.render('walled', False, "#741c1c")
                self.text_rect = self.text_surf.get_rect(center = (400, 50))
                self.player.set_collide(False)

            if self.player.get_health() == 0:
                self.screen.fill('black')
                self.text_surf = self.basic_font.render('YOUR HP HAS REDUCED TO 0', False, "#381100")
                self.text_rect = self.text_surf.get_rect(center = (400, 50))
                self.screen.blit(self.text_surf, self.text_rect)

            #don't touch
            pygame.display.update()
            self.clock.tick(60) #60 fps

if __name__ == '__main__':
    game = Game()
    game.run()