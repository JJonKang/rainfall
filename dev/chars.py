#characters
import pygame
import math
import projectiles as projectiles
class Player:
    #for now the multipler for speed is simply 3
    def __init__(self, x = 275, y = 250,spd_mult = 4):
        self.x = x
        self.y = y
        self.spd_mult = spd_mult
        self.spd_mult_default = spd_mult
        self.spd_lock = False

        self.req = set()

        self.bonk_cd = 0

        self.dash_cd = 0
        self.invuln = False

        self.image = pygame.Surface((18,18))
        self.clr_default = 'white'
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.collide = False
        self.health = 3

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
            self.invuln = True
        else:
            if self.dash_cd > 120:
                self.dash_cd -= 1
            elif self.dash_cd > 0:
                self.spd_mult = self.spd_mult_default
                self.image.fill("#a48bff")
                self.dash_cd -= 1
                self.spd_lock = False
                self.invuln = False
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
    def set_y(self, y):
        self.y = y

    def set_deny(self, deny):
        self.deny = deny

    def set_collide(self, collide):
        self.collide = collide

    def set_req(self, req):
        self.req.add(req)

    def set_health_reduce(self, reduce):
        self.health -= reduce

    def get_collide(self):
        return self.collide
    
    def get_rect(self):
        return self.rect
    
    def get_cooldown(self):
        return self.dash_cd
    
    def get_req(self):
        return self.req
    
    def get_health(self):
        return self.health
    
    def get_invuln(self):
        return self.invuln
    
class Enemy:
    def __init__(self):
        self.x = 750
        self.y = 250

        self.image = pygame.Surface((18,18))
        self.clr_default = "#5100ff"
        self.rect = self.image.get_rect(center = (self.x, self.y))

        #might replace this collide as for player collision damage in the future
        self.collide = False

        #spawn indicator
        self.spawn = False

        #bullet memory list
        self.bullets = []

        #bullet cooldown
        self.bullet_timer = 0

        #angle alteration
        self.alteration = 0

    def shoot(self, count = 26):
        direction = (2 * math.pi) / count
        for a in range(count):
            angle = a * direction + self.alteration
            bullet = projectiles.Bullet(self.x, self.y, 8, angle)
            self.bullets.append(bullet)
        self.bullet_timer = 5
        self.alteration += 5

    def bullet_update(self, screen, player):
        width, height = screen.get_size()
        updated_bullets = []
        for bullet in self.bullets:
            if player.get_health() == 0:
                return False
            x, y = bullet.get_pos()
            if x >= 25 and x < width - 25 and y >= 25 and y < height - 25:
                bullet.update()
                bullet.object(screen)
                if bullet.rect.colliderect(player.get_rect()) and player.get_invuln() == False:
                    player.set_health_reduce(1)
                    continue
                updated_bullets.append(bullet)
        self.bullets = updated_bullets
        return True

    def object(self, obj):
        self.image.fill(self.clr_default)
        obj.blit(self.image, self.rect)

    def set_spawn(self, spawn):
        self.spawn = spawn

    def set_bullet_timer_reduction(self, time):
        self.bullet_timer -= time

    def get_spawn(self):
        return self.spawn
    
    def get_bullets_list(self):
        return self.bullets
    
    def get_bullet_timer(self):
        return self.bullet_timer