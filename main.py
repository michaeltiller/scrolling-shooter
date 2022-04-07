import pygame
from player import Soldier
import game_functions as gf
from settings import Settings
from background import Background
from pygame.sprite import Group
import itemdrops
import healthbar1

def run_game():
    pygame.init()

    
    ai_settings = Settings()
    
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    background = Background(screen)
    pygame.display.set_caption("mikey's shooter")
    clock = pygame.time.Clock()
    FPS = 60

    enemy_group = Group()
    item_box_group = Group()
    
    player = Soldier('player', 200, 200, 1.65,  5, screen, ai_settings, 20, 5)
    health_bar = healthbar1.HealthBar(10, 10, player.health, player.health)
    enemy = Soldier('enemy', 400, 200, 1.65, 2, screen, ai_settings, 20, 0)
    enemy_group.add(enemy)
    TILE_SIZE = 40

    gf.add_item_box(item_box_group, TILE_SIZE)

    font = pygame.font.SysFont('Futura', 30)
   
    while True:
        clock.tick(FPS)
        background.draw_bg(ai_settings, screen)
        gf.draw_text(f'AMMO: {player.ammo}', font, (255,255,255), 10, 35, screen)
        gf.draw_text(f'GRENADES: {player.grenades}', font, (255,255,255), 10, 60, screen)
        health_bar.draw(player.health, screen)
        gf.check_events(player)
        player.update_animation()
        player.move()
        
    
        gf.update_screen(player, enemy, screen, ai_settings, enemy_group, TILE_SIZE, item_box_group)
        

run_game()
    

   
            
            

    

    
