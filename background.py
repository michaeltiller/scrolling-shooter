import pygame
class Background():
    def __init__(self, screen):
        self.screen = screen
        self.pine1_img = pygame.image.load('images/Background/pine1.png').convert_alpha()
        self.pine2_img = pygame.image.load('images/Background/pine2.png').convert_alpha()
        self.mountain_img = pygame.image.load('images/Background/mountain.png').convert_alpha()
        self.sky_img = pygame.image.load('images/Background/sky_cloud.png').convert_alpha()
        

 
    def draw_bg(self, ai_settings, screen):
        self.screen.fill(ai_settings.bg_color)
        width = self.sky_img.get_width()
        for x in range(5):
            self.screen.blit(self.sky_img, ((x * width) - ai_settings.bg_scroll * 0.5 ,0))
            self.screen.blit(self.mountain_img, ((x * width) - ai_settings.bg_scroll * 0.6 , ai_settings.screen_height - self.mountain_img.get_height() - 300))
            self.screen.blit(self.pine1_img, ((x * width) - ai_settings.bg_scroll * 0.7, ai_settings.screen_height - self.pine1_img.get_height() - 150))
            self.screen.blit(self.pine2_img, ((x * width)- ai_settings.bg_scroll * 0.8, ai_settings.screen_height - self.pine2_img.get_height()))
