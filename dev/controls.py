import pygame
class Player:
    #for now the multipler for speed is simply 1
    def __init__(self, x = 0, y = 0,spd_mult = 2.5):
        self.x = x
        self.y = y
        self.spd_mult = spd_mult

    def movement(self, key):
        if key[pygame.K_d] or key[pygame.K_RIGHT]:
            self.x += self.spd_mult
        if key[pygame.K_a] or key[pygame.K_LEFT]:
            self.x -= self.spd_mult
        if key[pygame.K_w] or key[pygame.K_UP]:
            self.y -= self.spd_mult
        if key[pygame.K_s] or key[pygame.K_DOWN]:
            self.y += self.spd_mult
    
    def object(self, obj):
        pygame.draw.rect(obj, (25, 25, 2), (self.x, self.y, 25, 25))

    def get_pos(self):
        print(self.x, self.y, self.spd_mult)