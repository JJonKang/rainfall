import pygame
class Player:
    #for now the multipler for speed is simply 1
    def __init__(self, x = 25, y = 25,spd_mult = 2.5):
        self.x = x
        self.y = y
        self.spd_mult = spd_mult

        self.image = pygame.Surface((25,25))
        self.image.fill('white')
        self.rect = self.image.get_rect(midbottom=(self.y, self.x))

    def movement(self, key):
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