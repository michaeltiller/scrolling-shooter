import pygame 
import explosion1
from pygame.sprite import Sprite

class Grenade(Sprite):
    def __init__(self, x, y, direction):
        super(Grenade, self).__init__()
        self.timer = 100
        self.vel_y = -11

        self.speed = 7
        self.image  = pygame.image.load('images/icons/grenade.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
    
    def update(self, ai_settings, player, enemy_group, TILE_SIZE):
        gravity = 0.75
        self.vel_y += gravity
        dx = self.direction * self.speed
        dy = self.vel_y

       

        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.speed=0
        if self.rect.left + dx <0 or self.rect.right + dx > ai_settings.screen_width:
            self.direction *= -1 
            dx = self.direction * self.speed
        
        self.rect.x += dx
        self.rect.y += dy

        self.timer -= 1
        if self.timer <=0:
            self.kill()
            explosion = explosion1.Explosion(self.rect.x, self.rect.y, 0.5)
            player.explosion_group.add(explosion)

            if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2 and abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 2:
                player.health -= 50
            
            for enemy in enemy_group:
                if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 2 and abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 2:
                    enemy.health -= 50



