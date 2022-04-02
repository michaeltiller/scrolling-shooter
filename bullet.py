import pygame 
from pygame.sprite import Sprite
class Bullet(Sprite):
    def __init__(self, x, y, direction, screen):
        super(Bullet, self).__init__()
        self.speed = 10
        self.image  = pygame.image.load('images/icons/bullet.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.screen = screen
    
    def update(self, ai_settings):
        self.rect.x += (self.direction * self.speed)

        if self.rect.right <0 or self.rect.left > ai_settings.screen_width:
            self.kill()

        


    
    def draw_bullet(self):
        self.screen.blit(self.image, self.rect)