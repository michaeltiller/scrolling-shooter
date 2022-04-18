from pygame.sprite import Sprite
class Decoration(Sprite):
    def __init__(self, img, x, y, TILE_SIZE):
        super(Decoration, self).__init__()
        self.image = img 
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()) )
    
    def update(self, ai_settings):
        self.rect.x += ai_settings.screen_scroll


class Water(Sprite):
    def __init__(self, img, x, y, TILE_SIZE):
        super(Water, self).__init__()
        self.image = img 
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()) )
    def update(self, ai_settings):
        self.rect.x += ai_settings.screen_scroll

class Exit(Sprite):
    def __init__(self, img, x, y, TILE_SIZE):
        super(Exit, self).__init__()
        self.image = img 
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()) )
    def update(self, ai_settings):
        self.rect.x += ai_settings.screen_scroll