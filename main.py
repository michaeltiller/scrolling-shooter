import pygame
from player import Soldier
import game_functions as gf
from settings import Settings
from background import Background
from pygame.sprite import Group

def run_game():
    pygame.init()

    
    ai_settings = Settings()
    
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    background = Background(screen)
    pygame.display.set_caption("mikey's shooter")
    clock = pygame.time.Clock()
    FPS = 60

    enemy_group = Group()

    player = Soldier('player', 200, 200, 3,  5, screen, ai_settings, 20, 5)
    enemy = Soldier('enemy', 400, 200, 3, 5, screen, ai_settings, 20, 0)
    enemy_group.add(enemy)
    TILE_SIZE = 40


     
   
    while True:
        clock.tick(FPS)
        background.draw_bg(ai_settings, screen)
        
        gf.check_events(player)
        player.update_animation()
        player.move()
        
    
        gf.update_screen(player, enemy, screen, ai_settings, enemy_group, TILE_SIZE)
        

run_game()
    

   
            
            

    

    
