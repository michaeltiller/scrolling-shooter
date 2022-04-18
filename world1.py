from player import Soldier
import healthbar1
import itemdrops
import tileclasses



class World():
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, data, img_list, ai_settings, screen, enemy_group, item_box_group, decoration_group, water_group, exit_group):
        self.level_length = len(data[0])
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * ai_settings.TILE_SIZE 
                    img_rect.y = y * ai_settings.TILE_SIZE 
                    tile_data = (img, img_rect)
                    if tile >= 0 and tile <= 8:
                        self.obstacle_list.append(tile_data)
                    elif tile >= 9 and tile <= 10:
                        water = tileclasses.Water(img, x * ai_settings.TILE_SIZE, y * ai_settings.TILE_SIZE, ai_settings.TILE_SIZE )
                        water_group.add(water)
                    elif tile >= 11 and tile <= 14:
                        decoration = tileclasses.Decoration(img,x * ai_settings.TILE_SIZE, y * ai_settings.TILE_SIZE, ai_settings.TILE_SIZE )
                        decoration_group.add(decoration)
                    elif tile == 15:
                        player = Soldier('player', x * ai_settings.TILE_SIZE , y * ai_settings.TILE_SIZE, 1.65,  5, screen, ai_settings, 20, 5)
                        health_bar = healthbar1.HealthBar(10, 10, player.health, player.health)
                    
                    elif tile == 16:
                        enemy = Soldier('enemy', x * ai_settings.TILE_SIZE, y * ai_settings.TILE_SIZE, 1.65, 2, screen, ai_settings, 20, 0)
                        enemy_group.add(enemy)
                    elif tile == 17:
                        item_box = itemdrops.ItemBox('Ammo', x * ai_settings.TILE_SIZE , y * ai_settings.TILE_SIZE, ai_settings.TILE_SIZE)
                        item_box_group.add(item_box)

                    elif tile == 18:
                        item_box = itemdrops.ItemBox('Grenade',  x * ai_settings.TILE_SIZE , y * ai_settings.TILE_SIZE, ai_settings.TILE_SIZE)
                        item_box_group.add(item_box)

                    elif tile == 19:
                        item_box = itemdrops.ItemBox('Health',  x * ai_settings.TILE_SIZE , y * ai_settings.TILE_SIZE, ai_settings.TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 20:
                        exit = tileclasses.Exit(img,x * ai_settings.TILE_SIZE, y * ai_settings.TILE_SIZE, ai_settings.TILE_SIZE )
                        exit_group.add(exit)

        return player, health_bar 
    
    def draw(self, screen, ai_settings):
        for tile in self.obstacle_list:
            tile[1][0] += ai_settings.screen_scroll
            screen.blit(tile[0], tile[1])
            
                    
