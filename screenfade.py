import pygame

class ScreenFade():
    def __init__(self, direction, colour, speed):
        self.direction = direction 
        self.colour = colour 
        self.speed = speed
        self.fade_counter = 0 

    
    def fade(self, screen, ai_settings):
        fade_complete = False
        self.fade_counter += self.speed

        if self.direction == 1:
            pygame.draw.rect(screen, self.colour, (0 - self.fade_counter,0, ai_settings.screen_width // 2, ai_settings.screen_height))
            pygame.draw.rect(screen, self.colour, (ai_settings.screen_width // 2 + self.fade_counter, 0, ai_settings.screen_width, ai_settings.screen_height))
            pygame.draw.rect(screen, self.colour, (0, 0-self.fade_counter, ai_settings.screen_width, ai_settings.screen_height //2))
            pygame.draw.rect(screen, self.colour, (0, ai_settings.screen_height // 2 + self.fade_counter, ai_settings.screen_width, ai_settings.screen_height))

        if self.direction == 2:
            pygame.draw.rect(screen, self.colour, (0,0, ai_settings.screen_width, 0 + self.fade_counter))
        if self.fade_counter >= ai_settings.screen_width:
            fade_complete = True 
        
        return fade_complete