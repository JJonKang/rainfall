import pygame
class Player:
    #for now the multipler for speed is simply 1
    def __init__(self, x = 300, y = 250,spd_mult = 3):
        self.x = x
        self.y = y
        self.spd_mult = spd_mult

        self.deny = False #collision, denies movement

        self.image = pygame.Surface((20,20))
        self.image.fill('white')
        self.rect = self.image.get_rect(center = (self.y, self.x))

    def movement(self, key):
        if self.deny == True:
            return
        
        if key[pygame.K_d] or key[pygame.K_RIGHT]:
            self.rect.x += self.spd_mult
        if key[pygame.K_a] or key[pygame.K_LEFT]:
            self.rect.x -= self.spd_mult
        if key[pygame.K_w] or key[pygame.K_UP]:
            self.rect.y -= self.spd_mult
        if key[pygame.K_s] or key[pygame.K_DOWN]:
            self.rect.y += self.spd_mult
    
    def object(self, obj):
        obj.blit(self.image, self.rect)

    def get_pos(self):
        print(self.x, self.y, self.spd_mult)

    def set_x(self, x):
        self.x = x
    
    def set_y(self, y):
        self.y = y

    def set_deny(self, deny):
        self.deny = deny