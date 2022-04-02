import pygame
class Background():
    def __init__(self, screen):
        self.screen = screen
 
    def draw_bg(self, ai_settings, screen):
        self.screen.fill(ai_settings.bg_color)
        pygame.draw.line(screen, ai_settings.red, (0,300), (ai_settings.screen_width, 300) )
