
from pygame.sprite import Sprite
from pygame.sprite import Group
import bullet
import pygame
import os
import random


class Soldier(Sprite):
    def __init__(self, char_type, x, y, scale, speed, screen, ai_settings, ammo, grenades):
        super(Soldier, self).__init__()
        self.alive = True 
        self.char_type = char_type
        self.speed = speed
        self.ammo = ammo
        self.start_ammo = ammo 
        self.shoot_cooldown = 0
        self.grenades = grenades
        self.health = 100
        self.max_health = self.health
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = [ ]
        self.frame_index = 0
        self.action = 0
        self.ai_settings = ai_settings
        self.update_time = pygame.time.get_ticks()
        self.bullet_group = Group()
        self.grenade_group = Group()
        self.explosion_group = Group()
        
        #ai specific
        self.move_counter = 0 
        self.idling = False
        self.idling_counter = 0
        #create a rect to see if the player is in front
        self.vision = pygame.Rect(0, 0, 150, 20)



        animation_types = ['idle', 'Run', 'Jump', 'Death']
        for animation in animation_types:
            temp_list = []
            num_of_frames = len(os.listdir(f'images/{self.char_type}/{animation}'))

            for i in range(num_of_frames):
                img = pygame.image.load(f'images/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
            

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.screen = screen
        self.moving_left = False
        self.moving_right = False 
        self.shoot = False
        self.grenade = False
        self.grenade_thrown = False


    def update(self):
        self.update_animation()
        self.check_alive()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1 

    def move(self, world, ai_settings, water_group, exit_group):
        dx = 0 
        dy = 0
        gravity = 0.75
        screen_scroll = 0 
        


        if self.moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if self.moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1 
        if self.jump == True and self.in_air == False:
            self.vel_y = -11 
            self.jump = False
            self.in_air = True
        
        self.vel_y += gravity
        if self.vel_y >10:
            self.vel_y
        dy += self.vel_y


        #check collision 
        for tile in world.obstacle_list:
           
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                if self.char_type == 'enemy':
                    self.direction *= -1
                    self.move_counter = 0
           
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
               
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
               
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom

        if pygame.sprite.spritecollide(self, water_group, False):
            self.health = 0 
        
        level_complete = False
        if pygame.sprite.spritecollide(self, exit_group, False):
            level_complete = True 

        if self.rect.bottom > ai_settings.screen_height:
            self.health = 0 

        #checks if gone off the screen
        if self.char_type == 'player':
            if self.rect.left + dx <0 or self.rect.right + dx > ai_settings.screen_width:
                dx = 0

        
        self.rect.x += dx
        self.rect.y += dy

        #does the scroll 
        if self.char_type == 'player':
            if (self.rect.right > ai_settings.screen_width - ai_settings.scroll_thresh and ai_settings.bg_scroll < (world.level_length * ai_settings.TILE_SIZE) - ai_settings.screen_width) \
                or (self.rect.left < ai_settings.scroll_thresh and ai_settings.bg_scroll > abs(dx)):
                self.rect.x -= dx 
                screen_scroll = -dx
                
        return screen_scroll, level_complete

    def shoot_bullet(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            bullet1 = bullet.Bullet(self.rect.centerx + (0.75 * self.rect.size[0] * self.direction), self.rect.centery, self.direction, self.screen)
            self.bullet_group.add(bullet1)
            self.ammo -= 1


    def update_animation(self):
        ANIMATION_COOLDOWN = 100 
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1 
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) -1
            else:
                self.frame_index = 0 
    
    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0 
            self.update_time = pygame.time.get_ticks()

    
    def move_bullet(self):
        for bullet in self.bullet_group:
            bullet.update(self.ai_settings)
    
    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)
        
        
    def draw(self):
        self.screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)    
        for bullet in self.bullet_group.sprites():
            bullet.draw_bullet()
   
    
    def ai(self, player, TILE_SIZE, world, ai_settings, water_group, exit_group):
        if self.alive and player.alive:
            if self.idling == False and random.randint(1, 200) ==1:
                self.update_action(0)
                self.idling = True
                self.idling_counter = 50

            #check ai near the player 
            if self.vision.colliderect(player.rect):
                self.update_action(0)
                self.shoot_bullet()
                self.move_bullet()
            else:

                if self.idling == False:
                    if self.direction == 1:
                        self.moving_right = True 
                    else:
                        self.moving_right = False 
                    self.moving_left = not self.moving_right
                    self.move(world, ai_settings, water_group, exit_group)
                    self.update_action(1)
                    self.move_counter += 1
                    #update vision as the ai moves 
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery )
                    

                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1 
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False
                        self.update_action(1)
        self.rect.x += ai_settings.screen_scroll
            