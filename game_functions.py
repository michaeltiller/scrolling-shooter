import pygame
import sys
from bullet import Bullet
from grenade1 import Grenade
import itemdrops
import world1
import csv


def update_screen(soilder):
    soilder.draw()

def check_events(player, ai_settings, restart_button, screen, enemy_group, item_box_group, decoration_group, water_group, exit_group, img_list):
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
            world_data = reset_level(enemy_group, player, item_box_group, decoration_group, water_group, exit_group, ai_settings)
            with open(f'level{ai_settings.level}_data.csv', newline = '') as csvfile:
                reader = csv.reader(csvfile, delimiter = ',')
                for x, row in enumerate(reader):
                    for y, tile in enumerate(row):
                        world_data[x][y] = int(tile)
            world = world1.World()
            player, health_bar = world.process_data(world_data, img_list, ai_settings, screen, enemy_group, item_box_group, decoration_group, water_group, exit_group)
        
        
        
    
def check_inputs( player):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player.moving_left = True 
            if event.key == pygame.K_d:
                player.moving_right = True 
            if event.key == pygame.K_w and player.alive:
                player.jump = True 
            if event.key == pygame.K_q :
                player.grenade = True 

            if event.key == pygame.K_SPACE:
                player.shoot = True

            if event.key == pygame.K_ESCAPE:
                sys.exit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player.moving_left = False
            if event.key == pygame.K_d:
                player.moving_right = False
            if event.key == pygame.K_SPACE:
                player.shoot = False
            if event.key == pygame.K_q:
                player.grenade = False
                player.grenade_thrown = False

def update_screen(player, screen, ai_settings, enemy_group, item_box_group, world, water_group, exit_group, decoration_group ):
    
    player.draw()
    player.move_bullet()
    player.update()
    for enemy in enemy_group:
        enemy.draw()
        enemy.update()
        enemy.ai(player, ai_settings.TILE_SIZE, world, ai_settings, water_group, exit_group)
        enemy.move_bullet()
    player.grenade_group.update(ai_settings, player, enemy_group, ai_settings.TILE_SIZE, world)
    player.grenade_group.draw(screen)
    player.explosion_group.update(ai_settings)
    player.explosion_group.draw(screen)
    item_box_group.update(player, ai_settings)
    water_group.update(ai_settings)
    exit_group.update(ai_settings)
    decoration_group.update(ai_settings)
    water_group.draw(screen)
    exit_group.draw(screen)
    item_box_group.draw(screen)
    decoration_group.draw(screen)

def check_player_bullet_collision(player, enemy_group):
    for enemy in enemy_group:
        if pygame.sprite.spritecollide(player, enemy.bullet_group, False):
            if player.alive:
                player.health -= 5
                for bullet in enemy.bullet_group:
                    bullet.kill()
                

        
    for enemy in enemy_group:     
        if pygame.sprite.spritecollide(enemy, player.bullet_group, False):
            if enemy.alive:
                enemy.health -= 25
                for bullet in player.bullet_group:
                    bullet.kill()
        
            
    
    
    

def draw_text(text, font, text_color, x, y, screen):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))

def reset_level(enemy_group, player, item_box_group, decoration_group, water_group, exit_group, ai_settings):
    enemy_group.empty()
    player.bullet_group.empty()
    player.grenade_group.empty()
    player.explosion_group.empty()
    item_box_group.empty()
    decoration_group.empty()
    water_group.empty()
    exit_group.empty()
    data = []
    for row in range(ai_settings.ROWS):
        r = [-1] * ai_settings.COLS
        data.append(r)
    return data 