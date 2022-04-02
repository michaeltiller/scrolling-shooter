import pygame
import sys
from bullet import Bullet


def update_screen(soilder):
    soilder.draw()

def check_events(player):
    if player.alive:
        if player.shoot:
            player.shoot_bullet()
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

def update_screen(player, enemy):
    
    enemy.draw()
    enemy.update()
    player.draw()
    player.move_bullet()
    player.update()

    if pygame.sprite.spritecollide(player, enemy.bullet_group, False):
        if player.alive:
            player.health -= 5
            for bullet in enemy.bullet_group:
                bullet.kill()
            

        
        
    if pygame.sprite.spritecollide(enemy, player.bullet_group, False):
        if enemy.alive:
            enemy.health -= 25
            for bullet in player.bullet_group:
                bullet.kill()
        
            
    
    
    pygame.display.update()