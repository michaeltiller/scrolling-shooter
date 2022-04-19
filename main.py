
from xml.etree.ElementTree import TreeBuilder
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
from pygame import mixer 
import screenfade


def run_game():
    pygame.init()
    mixer.init()

    
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
    restart_button = button.Button(ai_settings.screen_width //2 - 100, ai_settings.screen_height // 2 - 50, restart_img, 2)

    intro_fade = screenfade.ScreenFade(1, (0,0,0), 4 )
    death_fade = screenfade.ScreenFade(2, (255, 192, 203), 4 )
    
    pygame.mixer.music.load('audio/audio_music2.mp3')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1, 0.0, 5000)
    jump_fx = pygame.mixer.Sound('audio/audio_jump.wav')
    jump_fx.set_volume(0.5)
    shot_fx = pygame.mixer.Sound('audio/audio_shot.wav')
    shot_fx.set_volume(0.5)
    grenade_fx = pygame.mixer.Sound('audio/audio_grenade.wav')
    grenade_fx.set_volume(0.5)


    start_game = False
    start_intro = False
    

    

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
                start_intro = True
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
                start_intro = True
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
            gf.update_screen(player, screen, ai_settings, enemy_group, item_box_group, world, water_group,exit_group, decoration_group, shot_fx, grenade_fx)

            if start_intro == True:
                if intro_fade.fade(screen, ai_settings):
                    start_intro = False
                    intro_fade.fade_counte = 0

            if player.alive:
                if player.shoot:
                    player.shoot_bullet(shot_fx)
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
                if death_fade.fade(screen, ai_settings):
                    if restart_button.draw(screen):
                        death_fade.fade_counter = 0
                        start_intro = True
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
            
            
            
        gf.check_inputs(player, jump_fx)
        pygame.display.update()

run_game()
    

   
            
            

    

    
