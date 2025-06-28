import pygame
import math
class Bullet:
    def __init__(self, x = 0, y = 0, speed = 5, angle = 0):
        self.x = x
        self.y = y
        self.speed = speed
        self.velocity_x = math.cos(angle) * self.speed
        self.velocity_y = math.sin(angle) * self.speed

        self.image = pygame.Surface((6,6))
        self.clr_default = 'red'
        self.rect = self.image.get_rect(center = (self.x, self.y))

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.rect = self.image.get_rect(center = (self.x, self.y))

    def object(self, obj):
        self.image.fill(self.clr_default)
        obj.blit(self.image, self.rect)

    def get_pos(self):
        return self.x, self.y