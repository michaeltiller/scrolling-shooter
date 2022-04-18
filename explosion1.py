import pygame 
from pygame.sprite import Sprite
class Explosion(Sprite):
    def __init__(self, x, y, scale):
        super(Explosion, self).__init__()
        self.images = [ ]
        for num in range(1, 6):
            img = pygame.image.load(f'images/explosion/exp{num}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.images.append(img)
        self.frame_index = 0
        self.image= self.images[self.frame_index]
        
      
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0
       
    def update(self, ai_settings):
        self.rect.x += ai_settings.screen_scroll
        explosion_speed = 4 

        self.counter +=1 
        if self.counter >= explosion_speed:
            self.counter = 0 
            self.frame_index += 1 
            if self.frame_index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.frame_index]