
import pygame
from player import Soldier
import game_functions as gf
from settings import Settings
from background import Background
from pygame.sprite import Group
import button
import csv
import sys
import world1
from grenade1 import Grenade

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
    decoration_group = Group()
    water_group = Group()
    exit_group = Group()
    

    #button 
    start_img = pygame.image.load('images/start_btn.png').convert_alpha()
    exit_img = pygame.image.load('images/exit_btn.png').convert_alpha()
    restart_img = pygame.image.load('images/restart_btn.png').convert_alpha()


    start_button = button.Button(ai_settings.screen_width //2 - 130, ai_settings.screen_height // 2 - 150, start_img, 1)
    exit_button = button.Button(ai_settings.screen_width //2 - 110, ai_settings.screen_height // 2 + 50, exit_img, 1)
    restart_button = button.Button(ai_settings.screen_width //2 - 110, ai_settings.screen_height // 2 + 50, restart_img, 1)
    
    start_game = False
    

    

    font = pygame.font.SysFont('Futura', 30)

    #the tiles are stored in a list 
    img_list = []
    for x in range(ai_settings.TILE_TYPES):
        img = pygame.image.load(f'images/tile/{x}.png').convert_alpha()
        img = pygame.transform.scale(img, (ai_settings.TILE_SIZE, ai_settings.TILE_SIZE)  )
        img_list.append(img)


    world_data = []
    for row in range(ai_settings.ROWS):
        r = [-1] * ai_settings.COLS
        world_data.append(r)
    with open(f'level{ai_settings.level}_data.csv', newline = '') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',')
        for x, row in enumerate(reader):
            for y, tile in enumerate(row):
                world_data[x][y] = int(tile)
    world = world1.World()
    player, health_bar = world.process_data(world_data, img_list, ai_settings, screen, enemy_group, item_box_group, decoration_group, water_group, exit_group)

   
    while True:
        clock.tick(FPS)

        if start_game == False:
            screen.fill(ai_settings.bg_color)
            if start_button.draw(screen):
                start_game = True
            if exit_button.draw(screen):
                sys.exit()
            
        else:
            background.draw_bg(ai_settings, screen)
            gf.draw_text(f'AMMO: {player.ammo}', font, (255,255,255), 10, 35, screen)
            gf.draw_text(f'GRENADES: {player.grenades}', font, (255,255,255), 10, 60, screen)
            health_bar.draw(player.health, screen)
            
            player.update_animation()
            ai_settings.screen_scroll, level_complete = player.move(world, ai_settings, water_group, exit_group)
            ai_settings.bg_scroll -= ai_settings.screen_scroll
            if level_complete:
                ai_settings.level += 1
                ai_settings.bg_scroll = 0 
                world_data = gf.reset_level(enemy_group, player, item_box_group, decoration_group, water_group, exit_group, ai_settings)
                if ai_settings.level <= ai_settings.max_level:
                    with open(f'level{ai_settings.level}_data.csv', newline = '') as csvfile:
                        reader = csv.reader(csvfile, delimiter = ',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world = world1.World()
                    player, health_bar = world.process_data(world_data, img_list, ai_settings, screen, enemy_group, item_box_group, decoration_group, water_group, exit_group)
                        
            
            world.draw(screen, ai_settings)


            if player.alive:
                if player.shoot:
                    player.shoot_bullet()
                elif player.grenade and player.grenade_thrown == False and player.grenades > 0:
                    grenade = Grenade(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction), player.rect.top, player.direction)
                    player.grenade_group.add(grenade)
                    player.grenade_thrown = True
                    player.grenades -= 1
                
                if player.in_air:
                    player.update_action(2)
                elif player.moving_left or player.moving_right:
                    player.update_action(1) #1 is run 
                else:
                    player.update_action(0)
            else:
                ai_settings.screen_scroll = 0 
                if restart_button.draw(screen):
                    ai_settings.bg_scroll = 0 
                    world_data = gf.reset_level(enemy_group, player, item_box_group, decoration_group, water_group, exit_group, ai_settings)
                    with open(f'level{ai_settings.level}_data.csv', newline = '') as csvfile:
                        reader = csv.reader(csvfile, delimiter = ',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world = world1.World()
                    player, health_bar = world.process_data(world_data, img_list, ai_settings, screen, enemy_group, item_box_group, decoration_group, water_group, exit_group)
                        
                

        
            gf.check_player_bullet_collision(player, enemy_group)
            gf.update_screen(player, screen, ai_settings, enemy_group, item_box_group, world, water_group,exit_group, decoration_group )
            
            
        gf.check_inputs(player)
        pygame.display.update()

run_game()
    

   
            
            

    

    
