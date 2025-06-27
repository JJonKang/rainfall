#controls file
#currently only contains the player
import pygame
class Player:
    #for now the multipler for speed is simply 3
    def __init__(self, x = 300, y = 250,spd_mult = 3):
        self.x = x
        self.y = y
        self.spd_mult = spd_mult
        self.spd_mult_default = spd_mult
        self.spd_lock = False

        self.req = set()

        self.bonk_cd = 0

        self.dash_cd = 0

        self.image = pygame.Surface((18,18))
        self.clr_default = 'white'
        self.rect = self.image.get_rect(center = (self.y, self.x))
        self.collide = False

    #moves the player depending on wasd or arrow keys
    def movement(self, key, collision):

        #keeping the former position
        old_rect = self.rect.copy()

        #"dash": doubles speed of player, cooldown
        if (key[pygame.K_f] or key[pygame.K_j]) and self.spd_lock == False and self.dash_cd == 0:
            self.req.add('dash')
            self.spd_mult = self.spd_mult_default * 2
            self.dash_cd = 180
            self.image.fill('blue')
            self.spd_lock = True
        else:
            if self.dash_cd > 120:
                self.dash_cd -= 1
            elif self.dash_cd > 0:
                self.spd_mult = self.spd_mult_default
                self.image.fill("#a48bff")
                self.dash_cd -= 1
                self.spd_lock = False
            else:
                self.spd_mult = self.spd_mult_default
                self.image.fill(self.clr_default)
                self.spd_lock = False
        
        #"focus": slows player by half, no cooldown
        if (key[pygame.K_e] or key[pygame.K_k]) and self.spd_lock == False:
            self.req.add('focus')
            if self.dash_cd > 0 and self.dash_cd < 120:
                self.spd_mult = self.spd_mult_default - 2
                self.image.fill("#749e00")
            else:
                self.spd_mult = self.spd_mult_default - 2
                self.image.fill("#ff9100")

        #left/right movement
        if key[pygame.K_d] or key[pygame.K_RIGHT]:
            self.req.add('move')
            self.rect.x += self.spd_mult
        if key[pygame.K_a] or key[pygame.K_LEFT]:
            self.req.add('move')
            self.rect.x -= self.spd_mult

        #left/right collision check
        for collide in collision:
            if collide.colliderect(self.rect):
                self.rect.x = old_rect.x
                self.collide = True
                break

        #up/down movement
        if key[pygame.K_w] or key[pygame.K_UP]:
            self.req.add('move')
            self.rect.y -= self.spd_mult
        if key[pygame.K_s] or key[pygame.K_DOWN]:
            self.req.add('move')
            self.rect.y += self.spd_mult

        #up/down collision check
        for collide in collision:
            if collide.colliderect(self.rect):
                self.rect.y = old_rect.y
                self.collide = True
                break
    
    #draws the player's position
    def object(self, obj):
        obj.blit(self.image, self.rect)

    #getters and setters
    def get_pos(self):
        print(self.x, self.y, self.spd_mult)

    def set_x(self, x):
        self.x = x
    
    def set_y(self, y):
        self.y = y

    def set_deny(self, deny):
        self.deny = deny

    def set_collide(self, collide):
        self.collide = collide

    def set_req(self, req):
        self.req.add(req)

    def get_collide(self):
        return self.collide
    
    def get_cooldown(self):
        return self.dash_cd
    
    def get_req(self):
        return self.req