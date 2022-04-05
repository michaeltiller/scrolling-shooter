import pygame
import sys
from bullet import Bullet
from grenade1 import Grenade

def update_screen(soilder):
    soilder.draw()

def check_events(player):
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

def update_screen(player, enemy, screen, ai_settings, enemy_group, TILE_SIZE, item_box_group):
    for enemy in enemy_group:
        enemy.draw()
        enemy.update()
    player.draw()
    player.move_bullet()
    player.update()
    player.grenade_group.update(ai_settings, player, enemy_group, TILE_SIZE)
    player.grenade_group.draw(screen)
    player.explosion_group.update()
    player.explosion_group.draw(screen)
    item_box_group.update(player)
    item_box_group.draw(screen)


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
        
            
    
    
    pygame.display.update()

def draw_text(text, font, text_color, x, y, screen):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))

