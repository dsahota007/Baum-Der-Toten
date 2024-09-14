import pygame
from weapon import Weapon, Bullet
import random
from level import Box
import math


class MysteryBox:
    def __init__(self, x, y, width, height, closed_image_path, open_image_path, cost):
        self.box = Box(x, y, width, height)
        
        self.closed_image = pygame.image.load(closed_image_path).convert_alpha()
        self.closed_image = pygame.transform.scale(self.closed_image, (width, height))
        
        self.open_image = pygame.image.load(open_image_path).convert_alpha()
        self.open_image = pygame.transform.scale(self.open_image, (width, height))

        self.image = self.closed_image  # Starting with closed box
        self.x = x
        self.y = y
        self.is_interacting = False  
        self.opened_time = None
        self.selected_weapon_image = None
        self.bobbing_time = 0
        self.cost = cost
        self.selected_weapon_config = None 
        self.animation_image = None
        self.animation_frame_counter = 1
        
    def reset_weapon(self):
        self.selected_weapon_config = None
        self.selected_weapon_image = None
        self.is_interacting = False
        
    def handle_decision(self, key, player_weapons, current_weapon_index, screen, camera, game_score):
        if key == pygame.K_y:  # Player accepts the new weapon
            new_weapon = self.interact(player_weapons[current_weapon_index].player_rect, weapons_list, screen, camera, game_score)
            if new_weapon:
                player_weapons[current_weapon_index] = new_weapon
                
    def load_selected_weapon_image(self, image_path):
        self.selected_weapon_image = pygame.image.load(image_path[0]).convert_alpha()
        # Adjust the size (80, 40) below as per your preference:
        self.selected_weapon_image = pygame.transform.scale(self.selected_weapon_image, (80, 30)) #thickness of gun

    def set_open(self, player_score):
        if player_score.score >= self.cost:  # Check if the player has enough score
            self.image = self.open_image
            player_score.score -= self.cost  # Deduct the cost (950 points)
            self.opened_time = pygame.time.get_ticks()  # Store the time when the box is opened
            self.weapon_appear_time = self.opened_time + 5000  # Set the time when the weapon should appear
            self.animation_image = random.choice(weapons_list)["image_path"][0]
            
    def set_closed(self):
            self.image = self.closed_image
            
    def display_weapon_prompt(self, screen, camera):
        current_time = pygame.time.get_ticks()
        if self.image == self.open_image and self.selected_weapon_image and current_time - self.opened_time > 5000:  # 5000 ms = 5 seconds
            font_path = 'assets/interface/WesternBangBang-Regular.ttf'  # Use your font path or None for default
            font_size = 32
            font = pygame.font.Font(font_path, font_size) if font_path else pygame.font.SysFont(None, font_size)
            
            # Render the fixed prompt
            prompt_text = "Press Q to Pick up "
            prompt_surface = font.render(prompt_text, True, (203, 202, 0))
            
            # Render the weapon name in a different color, like blue
            weapon_name = self.selected_weapon_config['name'][0]  # Assuming name is the first in the list for weapon tiers
            weapon_name_surface = font.render(weapon_name, True, (255, 255, 255))  # RGB for blue
            
            # Combine the two text surfaces
            combined_surface = pygame.Surface((prompt_surface.get_width() + weapon_name_surface.get_width(), prompt_surface.get_height()), pygame.SRCALPHA)
            combined_surface.blit(prompt_surface, (0, 0))
            combined_surface.blit(weapon_name_surface, (prompt_surface.get_width(), 0))
            
            # Position the combined text centered on the box
            box_center_x = self.box.rect.x + self.box.rect.width / 2
            box_center_y = self.box.rect.y
            text_rect = combined_surface.get_rect(center=(box_center_x, box_center_y))
            
            # Adjust the y-coordinate to be displayed above the mystery box
            text_rect.y -= 30
            screen.blit(combined_surface, (text_rect.x + camera.camera_rect.x, text_rect.y + camera.camera_rect.y))
    
    def display_open_prompt(self, screen, player_rect, camera):
        # Check if player is near the Mystery Box and the box is closed
        if self.is_player_nearby(player_rect) and self.image == self.closed_image:
            font_path = 'assets/interface/WesternBangBang-Regular.ttf'  # Replace with your actual font path or None for the default font.
            font_size = 32
            font = pygame.font.Font(font_path, font_size) if font_path else pygame.font.SysFont(None, font_size)
            prompt_text = "Press E to Open the Mystery Box ($950)"
            text_surface = font.render(prompt_text, True, (203, 202, 0))
            prompt_position = (self.box.rect.x + camera.camera_rect.x - 110, self.box.rect.y + camera.camera_rect.y - 10)  # Adjust as needed
            screen.blit(text_surface, prompt_position)
            
    def draw(self, screen, camera, player_rect):  # Now takes player_rect as an argument
        self.box.draw(screen, camera)
        screen.blit(self.image, (self.box.rect.x + camera.camera_rect.x, self.box.rect.y + camera.camera_rect.y))
        self.display_open_prompt(screen, player_rect, camera)
        self.display_weapon_prompt(screen, camera)

        if self.image == self.open_image and pygame.time.get_ticks() < self.weapon_appear_time:
            self.animation_frame_counter += 1

            # Change the gun every 15 frames (0.25 seconds at 60 FPS)
            if self.animation_frame_counter >= 5:
                self.animation_image = random.choice(weapons_list)["image_path"][0]
                self.animation_frame_counter = 0

            # Load the current gun image
            animation_surface = pygame.image.load(self.animation_image).convert_alpha()

            # Adjust the size to maintain the aspect ratio
            original_rect = animation_surface.get_rect()
            aspect_ratio = original_rect.width / original_rect.height
            new_height = 37  # Set your desired height
            new_width = int(new_height * aspect_ratio)  # Calculate width based on aspect ratio

            # Scale the image
            animation_surface = pygame.transform.scale(animation_surface, (new_width, new_height))

            # Display the scaled image
            screen.blit(animation_surface, (self.box.rect.x + camera.camera_rect.x + 5, self.box.rect.y + camera.camera_rect.y - 10))

        elif self.image == self.open_image and self.selected_weapon_image:
            bobbing_offset = math.sin(self.bobbing_time) * 5  # 5 controls the intensity of the bobbing effect
            screen.blit(self.selected_weapon_image, (self.box.rect.x + camera.camera_rect.x + 20, self.box.rect.y + camera.camera_rect.y - 10 + bobbing_offset))
            self.bobbing_time += 0.1 

            
    def interact(self, player_rect, weapons_list, screen, camera, game_score):
        if self.image == self.open_image:  # Make sure the box is open
            if not self.is_interacting:  # If not currently interacting, select a new weapon
                self.selected_weapon_config = random.choice(weapons_list)
                self.is_interacting = True

            new_weapon = Weapon(
                name=self.selected_weapon_config["name"],
                image_path=self.selected_weapon_config["image_path"], 
                screen=screen, 
                camera=camera, 
                score=game_score, 
                bullet_speed=self.selected_weapon_config["bullet_speed"], 
                damage=self.selected_weapon_config["damage"], 
                control_method=self.selected_weapon_config["control_method"],
                clip_size=self.selected_weapon_config["clip_size"],
                stock_ammo=self.selected_weapon_config["stock_ammo"],
                scale_size=self.selected_weapon_config.get("scale_size", (35, 35)),
                fire_rate=self.selected_weapon_config.get("fire_rate", 200),
                reload_time=self.selected_weapon_config.get("reload_time", 1500),
                bullet_color=self.selected_weapon_config["bullet_color"],  # added
                bullet_size=self.selected_weapon_config["bullet_size"],    # added
            )
            self.load_selected_weapon_image(self.selected_weapon_config["image_path"])
            
            return new_weapon
        return None
        
    def provide_weapon(self, player_rect, weapons_list, screen, camera, game_score):
        new_weapon = Weapon(
            name=self.selected_weapon_config["name"],
            image_path=self.selected_weapon_config["image_path"], 
            screen=screen, 
            camera=camera, 
            score=game_score, 
            bullet_speed=self.selected_weapon_config["bullet_speed"], 
            damage=self.selected_weapon_config["damage"], 
            control_method=self.selected_weapon_config["control_method"],
            clip_size=self.selected_weapon_config["clip_size"],
            stock_ammo=self.selected_weapon_config["stock_ammo"],
            scale_size=self.selected_weapon_config.get("scale_size", (35, 35)),
            fire_rate=self.selected_weapon_config.get("fire_rate", 200),
            reload_time=self.selected_weapon_config.get("reload_time", 1500),
            bullet_color=self.selected_weapon_config["bullet_color"],  # added
            bullet_size=self.selected_weapon_config["bullet_size"],  
        )
               
        return new_weapon
    
    
    def select_weapon(self):
        if not self.is_interacting:  # If not currently interacting, select a new weapon
            self.selected_weapon_config = random.choice(weapons_list)
            self.is_interacting = True
            self.load_selected_weapon_image(self.selected_weapon_config["image_path"])
        # self.show_prompt = True
    
    def is_player_nearby(self, player_rect):
        distance = math.sqrt((self.x - player_rect.centerx)**2 + (self.y - player_rect.centery)**2)
        return distance < 100 
    
UPGRADE_COSTS = [5000, 15000, 30000, 50000, 100000]
    
class PackAPunch:
    def __init__(self, x, y, width, height, image_path):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        
        #prompts
        self.font_path = 'assets/interface/WesternBangBang-Regular.ttf'  # Replace with your actual font path or None for the default font.
        self.font_size = 32

    def draw(self, screen, camera):
        screen.blit(self.image, (self.rect.x + camera.camera_rect.x, self.rect.y + camera.camera_rect.y))

    def display_prompt(self, screen, player_rect, camera, active_weapon):  # Add active_weapon as a parameter
        if player_rect.colliderect(self.rect):
            prompt_position = (self.rect.x + camera.camera_rect.x - 160, self.rect.y + camera.camera_rect.y - 30)  # Adjust position as needed
            if active_weapon.tier < 5:
                # The modified line is below
                self._display_pack_a_punch_prompt(screen, prompt_position, active_weapon.tier + 1, active_weapon.tier)  
            else:
                self._display_pack_a_punch_prompt(screen, prompt_position, "max tier", active_weapon.tier) # This line might need modification based on how you want to display when it's max tier.

    def _display_pack_a_punch_prompt(self, screen, position, next_tier, current_tier):
        font = pygame.font.Font(self.font_path, self.font_size) if self.font_path else pygame.font.SysFont(None, self.font_size)
        
        # Determine the cost based on the tier
        cost_dict = {1: 5000, 2: 15000, 3: 30000, 4: 50000, 5: 100000}
        cost = cost_dict.get(next_tier, 0)  # Gets the cost or defaults to 0
        
        # Check if the next tier is a string indicating it's the max tier
        if isinstance(next_tier, str) and next_tier == "max tier":
            prompt_text = f"         Maximum Upgrade Achieved!"
        else:
            prompt_text = f"Press E to Pack-a-Punch! (Tier: {next_tier}, ${cost})"
        
        text_surface = font.render(prompt_text, True, (255, 255, 255))
        screen.blit(text_surface, position)
            
    def interact(self, player_rect, active_weapon, game_score):
            if self.rect.colliderect(player_rect):
                weapon_config = next((item for item in weapons_list if active_weapon.name in item["name"]), None)
                    
                if weapon_config:
                    current_name_index = weapon_config["name"].index(active_weapon.name)
                        
                    if current_name_index < len(weapon_config["name"]) - 1:
                        cost_to_upgrade = UPGRADE_COSTS[current_name_index]
                            
                        if game_score.score >= cost_to_upgrade:
                            # Upgrade weapon's tier
                            active_weapon.name = weapon_config["name"][current_name_index + 1]
                            active_weapon.damage *= 2
                            game_score.score -= cost_to_upgrade
                                
                            # Change weapon image to the one corresponding to its new tier
                            active_weapon.original_image = pygame.image.load(weapon_config["image_path"][current_name_index + 1]).convert_alpha()
                            active_weapon.original_image = pygame.transform.scale(active_weapon.original_image, weapon_config["scale_size"])
                            active_weapon.image = active_weapon.original_image.copy()

                            # Change bullet color to the next one
                            active_weapon.bullet_color = weapon_config["bullet_color"]
                        
class AmmoBox:
    def __init__(self, x, y, width, height, image_path):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.font_path = 'assets/interface/WesternBangBang-Regular.ttf' 
        self.font_size = 32
        self.ammo_cost = [250, 1250, 2500, 5000, 10000, 12500]

    def draw(self, screen, camera):
        screen.blit(self.image, (self.rect.x + camera.camera_rect.x, self.rect.y + camera.camera_rect.y))

    def display_prompt(self, screen, player_rect, camera, active_weapon):  # Add active_weapon as parameter  
        if player_rect.colliderect(self.rect):
            prompt_position = (self.rect.x + camera.camera_rect.x - 120, self.rect.y + camera.camera_rect.y - 30)
            self._display_interaction_prompt(screen, prompt_position, active_weapon.tier)

    def _display_interaction_prompt(self, screen, position, tier):  # Add tier as parameter
        font = pygame.font.Font(self.font_path, self.font_size) if self.font_path else pygame.font.SysFont(None, self.font_size)
        cost = self.ammo_cost[tier]  # Get the cost based on weapon's tier
        prompt_text = f"Press E to buy Ammunition (${cost})"  # Show the cost in the prompt
        text_surface = font.render(prompt_text, True, (255, 129, 120))
        screen.blit(text_surface, position)

    def refill_ammo(self, weapon, game_score):  # Added game_score to handle the score deduction
        if game_score.score >= self.ammo_cost[weapon.tier]:  # Check if the player has enough score
            game_score.score -= self.ammo_cost[weapon.tier]
            weapon.clip_ammo = weapon.clip_size
            weapon.stock_ammo = weapon.original_stock_ammo
        
      
weapons_list = [
    {   #COMPELTE
        "name": ["M1911","Sally - Tier I", "Sally - Tier II","Sally - Tier III", "Sally - Tier IV","Sally - Tier V",],
        "image_path": ["assets/weapons/m1911.png","assets/weapons/m1911_1.png","assets/weapons/m1911_2.png","assets/weapons/m1911_3.png","assets/weapons/m1911_4.png","assets/weapons/m1911_5.png",],
        "bullet_color": [(213, 213, 178), (77,2,255), (229,1,4), (77,2,255), (148,6,215),(3,43,219),  ],
        "bullet_size": (5, 5),
        "scale_size": (45, 45),
        "bullet_speed": 40,
        "damage": 20,
        "control_method": "single/auto" ,
        "fire_rate":400,
        "clip_size": 8,     
        "stock_ammo": 32, 
        "reload_time": 1800,
    },
    {   #COMPLETE
        "name": ["P-90","Pulverizer-99 - Tier I","Pulverizer-99 - Tier II","Pulverizer-99 - Tier III","Pulverizer-99 - Tier IV","Pulverizer-99 - Tier V",],
        "image_path": ["assets/weapons/p90.png","assets/weapons/p90_1.png","assets/weapons/p90_2.png","assets/weapons/p90_3.png","assets/weapons/p90_4.png","assets/weapons/p90_5.png",],
        "bullet_color":  [(213, 213, 178), (224,165,225), (224,134,225), (224,100,225), (224,60,225), (190,0,190),], 
        "bullet_size": (4, 4),
        "scale_size": (70, 45),
        "bullet_speed": 10,
        "damage": 30,
        "control_method": "single/auto", 
        "fire_rate":150,
        "clip_size": 55,     
        "stock_ammo": 110, 
        "reload_time": 1700
    },
    {   #COMPLETE
        "name": ["M4A1","SM4 Raider's Bite - Tier I","SM4 Raider's Bite - Tier II","SM4 Raider's Bite - Tier III","SM4 Raider's Bite - Tier IV","SM4 Raider's Bite - Tier V",],
        "image_path": ["assets/weapons/m4a1.png","assets/weapons/m4a1_1.png","assets/weapons/m4a1_2.png","assets/weapons/m4a1_3.png","assets/weapons/m4a1_4.png","assets/weapons/m4a1_5.png",],
        "bullet_color":  [(213, 213, 178), (251,255,103),(251,255,65),(251,255,0),(177,177,1),(211,143,23)],
        "bullet_size": (5, 5),
        "scale_size": (63, 40),
        "bullet_speed": 40,
        "damage": 25,
        "control_method": "single/auto",
        "fire_rate":100,
        "clip_size": 30,     
        "stock_ammo": 90, 
        "reload_time": 2000
    },
    {   #COMPLETE 
        "name": ["Hauer 77", "Hauer Havocizer - Tier I", "Hauer Havocizer - Tier II", "Hauer Havocizer - Tier III", "Hauer Havocizer - Tier IV","Hauer Havocizer - Tier V"],
        "image_path": ["assets/weapons/hauer.png","assets/weapons/hauer_1.png","assets/weapons/hauer_2.png","assets/weapons/hauer_3.png","assets/weapons/hauer_4.png","assets/weapons/hauer_5.png",],
        "bullet_color": [(255,255,255),(243, 0, 255), (243, 0, 255),(243, 0, 255),(0, 255, 5),(3, 255, 5),],
        "bullet_size": (5, 5),
        "scale_size": (90, 33),
        "bullet_speed": 20,
        "damage": 60,
        "control_method": "shotgun",
        "fire_rate":980,
        "clip_size": 8,     
        "stock_ammo": 48, 
        "reload_time": 4000
    },
    {   #COMPLETE
        "name": ["Famas","Tempest Howler - Tier I","Tempest Howler - Tier II","Tempest Howler - Tier III","Tempest Howler - Tier IV","Tempest Howler - Tier V",],
        "image_path": ["assets/weapons/famas.png","assets/weapons/famas_1.png","assets/weapons/famas_2.png","assets/weapons/famas_3.png","assets/weapons/famas_4.png","assets/weapons/famas_5.png",],
        "bullet_color": [(213, 213, 178),(213, 122, 122),(213, 90, 178),(213, 60, 178),(213, 0, 178),(111, 12, 40),],
        "bullet_size": (5, 5),
        "scale_size": (55, 35),
        "bullet_speed": 10,
        "damage": 40,
        "control_method": "single/auto", 
        "fire_rate":200,
        "clip_size": 30,     
        "stock_ammo": 120, 
        "reload_time": 1600
    },
    {   #COMPELTE
        "name": ["L96A1","Deadeye - Tier I", "Deadeye - Tier II","Deadeye - Tier III", "Deadeye - Tier IV","Deadeye - Tier V",],
        "image_path": ["assets/weapons/l96a1.png","assets/weapons/l96a1_1.png","assets/weapons/l96a1_2.png","assets/weapons/l96a1_3.png","assets/weapons/l96a1_4.png"],
        "bullet_color": [(255, 213, 178),(181, 177, 239),(255, 121, 178),(255, 40, 178),(255, 0, 178),(30, 20, 166),],
        "bullet_size": (8, 8),
        "scale_size": (95, 45),
        "bullet_speed": 98,
        "damage": 87,
        "control_method": "single/auto" ,
        "fire_rate":850,
        "clip_size": 6,     
        "stock_ammo": 42, 
        "reload_time": 2000,
    },
    {   #COMPELTE
        "name": ["Desert Eagle","Blistering Pheonix - Tier I", "Blistering Pheonix - Tier II","Blistering Pheonix - Tier III","Blistering Pheonix - Tier IV","Blistering Pheonix - Tier V",],
        "image_path": ["assets/weapons/deagle.png","assets/weapons/deagle_1.png","assets/weapons/deagle_2.png","assets/weapons/deagle_3.png","assets/weapons/deagle_4.png","assets/weapons/deagle_5.png"],
        "bullet_color": [(213, 213, 178),  (234, 213, 78), (213, 213, 0), (222, 108, 43), (222, 111, 0) ,(254, 34, 0)], 
        "bullet_size": (7, 7),
        "scale_size": (49, 43),
        "bullet_speed": 60,
        "damage": 58,
        "control_method": "single/auto" ,
        "fire_rate":300,
        "clip_size": 6,     
        "stock_ammo": 36, 
        "reload_time": 1500,
    },
    {   #COMPLETE
        "name": ["Carv","Crystilized Rapture - Tier I","Crystilized Rapture - Tier II","Crystilized Rapture - Tier III","Crystilized Rapture - Tier IV","Crystilized Rapture - Tier V",],
        "image_path": ["assets/weapons/carv.png","assets/weapons/carv_1.png","assets/weapons/carv_2.png","assets/weapons/carv_3.png","assets/weapons/carv_4.png","assets/weapons/carv_5.png",],
        "bullet_color": [(213, 213, 178),  (77, 219, 161),  (12, 213, 178),  (0, 213, 178),  (40, 166, 233),  (0, 255, 255),],
        "bullet_size": (7, 7),
        "scale_size": (68, 45),
        "bullet_speed": 60,
        "damage": 40,
        "control_method": "burst",
        "fire_rate":90,
        "clip_size": 30,     
        "stock_ammo": 120, 
        "reload_time": 2000
    },
    {   #COMPLETE
        "name": ["Ray Gun Mark II ","Porter's NukeX2 - Tier I","Porter's NukeX2  - Tier II","Porter's NukeX2 - Tier III","Porter's NukeX2 - Tier IV","Porter's NukeX2 - Tier V",],
        "image_path": ["assets/weapons/raygunmk2.png","assets/weapons/raygunmk2_1.png","assets/weapons/raygunmk2_2.png","assets/weapons/raygunmk2_3.png","assets/weapons/raygunmk2_4.png","assets/weapons/raygunmk2_5.png"],
        "bullet_color": [(0, 250, 81),  (255, 0, 0),  (255, 0, 0),  (255, 0, 0),  (109, 20, 220),  (0, 222, 222)], 
        "bullet_size": (7, 7),
        "scale_size": (90, 55),
        "bullet_speed": 50,
        "damage": 56,
        "control_method": "burst",
        "fire_rate":140,
        "clip_size": 21,     
        "stock_ammo": 90, 
        "reload_time": 2900
    },
    {   #COMPLETE
        "name": ["M16","Skullcrusher - Tier I","Skullcrusher - Tier II","Skullcrusher - Tier III","Skullcrusher - Tier IV","Skullcrusher - Tier V",],
        "image_path": ["assets/weapons/m16.png","assets/weapons/m16_1.png","assets/weapons/m16_2.png","assets/weapons/m16_3.png","assets/weapons/m16_4.png","assets/weapons/m16_5.png",],
        "bullet_color": [(213, 213, 121),  (117, 200, 255), (55, 200, 255),(0, 200, 255),(177, 33, 255),(255, 255, 255),],  
        "bullet_size": (7, 7),
        "scale_size": (85, 45),
        "bullet_speed": 45,
        "damage": 42,
        "control_method": "burst",
        "fire_rate":140,
        "clip_size": 30,     
        "stock_ammo": 90, 
        "reload_time": 2200
    },
    {   #COMPLETE
        "name": ["AK-47","The Avenger - Tier I","The Avenger - Tier II","The Avenger - Tier III","The Avenger - Tier IV","The Avenger - Tier V",],
        "image_path": ["assets/weapons/ak47.png","assets/weapons/ak47_1.png","assets/weapons/ak47_2.png","assets/weapons/ak47_3.png","assets/weapons/ak47_4.png","assets/weapons/ak47_5.png"],
        "bullet_color": [(255, 213, 121),(55, 213, 221),(0, 213, 221),(129, 22, 181),(129, 22, 181),(205, 176, 219)],  
        "bullet_size": (9, 9),
        "scale_size": (80, 30),
        "bullet_speed": 45,
        "damage": 34,
        "control_method": "single/auto",
        "fire_rate":120,
        "clip_size": 35,     
        "stock_ammo": 120, 
        "reload_time": 1900
    },
    {   #COMPLETE
        "name": ["Python","Cobra - Tier I","Cobra - Tier II","Cobra - Tier III","Cobra - Tier IV","Cobra - Tier V",],
        "image_path": ["assets/weapons/python.png","assets/weapons/python_1.png","assets/weapons/python_2.png","assets/weapons/python_3.png","assets/weapons/python_4.png","assets/weapons/python_5.png"],
        "bullet_color": [(255, 213, 121),  (255, 0, 0),  (255, 0, 0),  (255, 0, 0),  (0,222,222),  (0, 222,222),  (0, 222,222), ],
        "bullet_size": (5, 5),
        "scale_size": (84, 55),
        "bullet_speed": 45,
        "damage": 65,
        "control_method": "single/auto",
        "fire_rate":290,
        "clip_size": 6,     
        "stock_ammo": 36, 
        "reload_time": 4000
    },
    {   #COMPLETE
        "name": ["PPsH-41","Resurrected Reaper - Tier I","Resurrected Reaper - Tier II","Resurrected Reaper - Tier III","Resurrected Reaper - Tier IV","Resurrected Reaper - Tier V",],
        "image_path": ["assets/weapons/ppsh.png","assets/weapons/ppsh_1.png","assets/weapons/ppsh_2.png","assets/weapons/ppsh_3.png","assets/weapons/ppsh_4.png","assets/weapons/ppsh_5.png"],
        "bullet_color": [(255, 213, 121),  (255, 199, 255),  (255, 160, 255),  (255, 120, 255),  (213,60,255),  (213, 0,245),  (100, 19,118), ],
        "bullet_size": (6, 6),
        "scale_size": (85, 55),
        "bullet_speed": 60,
        "damage": 23,
        "control_method": "single/auto",
        "fire_rate":70,
        "clip_size": 55,     
        "stock_ammo": 165, 
        "reload_time": 2000
    },
    {   #COMPLETE
        "name": ["AUG","Triple Pheonix - Tier I","ATriple Pheonix - Tier II","Triple Pheonix - Tier III","Triple Pheonix - Tier IV","Triple Pheonix - Tier V",],
        "image_path": ["assets/weapons/aug.png","assets/weapons/aug_1.png","assets/weapons/aug_2.png","assets/weapons/aug_3.png","assets/weapons/aug_4.png","assets/weapons/aug_5.png"],
        "bullet_color": [(255, 244, 199),  (255, 188, 188),  (255, 120, 120),  (255, 60, 60),  (213,0,0),  (255, 0,0),  (255, 0,178), ],
        "bullet_size": (6, 6),
        "scale_size": (70, 45),
        "bullet_speed": 50,
        "damage": 41,
        "control_method": "burst",
        "fire_rate":130,
        "clip_size": 30,     
        "stock_ammo": 90, 
        "reload_time": 2000
    },
    {   #COMPLETE 
        "name": ["SCAR-H","Agarthan's Soul - Tier I","Agarthan's Soul - Tier II","Agarthan's Soul - Tier III","Agarthan's Soul - Tier IV","Agarthan's Soul - Tier V",],
        "image_path": ["assets/weapons/scarh.png","assets/weapons/scarh_1.png","assets/weapons/scarh_2.png","assets/weapons/scarh_3.png","assets/weapons/scarh_4.png","assets/weapons/scarh_5.png"],
        "bullet_color": [(255, 255, 255),  (255, 111, 1),  (1, 155, 244),  (255, 234, 1),  (0,250,0),  (255, 0,255), ],
        "bullet_size": (6, 6),
        "scale_size": (93, 45),
        "bullet_speed": 45,
        "damage": 30,
        "control_method": "single/auto",
        "fire_rate":150,
        "clip_size": 30,     
        "stock_ammo": 60, 
        "reload_time": 2200
    },
    {   #COMPLETE
        "name": ["Spas-12", "Spaz-64 - Tier I", "Spaz-128 - Tier II", "Spaz-256 - Tier III", "Spaz-512 - Tier IV","Spaz-1024 - Tier V"],
        "image_path": ["assets/weapons/spas12.png","assets/weapons/spas12_1.png","assets/weapons/spas12_2.png","assets/weapons/spas12_3.png","assets/weapons/spas12_4.png","assets/weapons/spas12_5.png"],
        "bullet_color": [(255, 255, 255),  (200, 200, 200),  (111, 111, 111),  (70, 60, 60),  (98,78,21),   (98,78,21),  (255, 255,255), ],
        "bullet_size": (4, 4),
        "scale_size": (98, 56),
        "bullet_speed": 27,
        "damage": 53,
        "control_method": "shotgun",
        "fire_rate":450,
        "clip_size": 7,     
        "stock_ammo": 42, 
        "reload_time": 4900
    },
    {   #COMPELTE
        "name": ["Barret .50 Cal","Vortex Vanquisher - Tier I", "Vortex Vanquisher - Tier II","Vortex Vanquisher - Tier III", "Vortex Vanquisher - Tier IV","Vortex Vanquisher - Tier V",],
        "image_path": ["assets/weapons/barret50cal.png","assets/weapons/barret50cal_1.png","assets/weapons/barret50cal_2.png","assets/weapons/barret50cal_3.png","assets/weapons/barret50cal_4.png","assets/weapons/barret50cal_5.png"],
        "bullet_color": [(255, 244, 199),  (222, 255, 255),  (167, 120, 120),  (122, 60, 60),  (12,0,0),  (34, 144,170),  (0, 255,77), ],
        "bullet_size": (10, 10),
        "scale_size": (95, 45),
        "bullet_speed": 85,
        "damage": 75,
        "control_method": "single/auto" ,
        "fire_rate":450,
        "clip_size": 8,     
        "stock_ammo": 32, 
        "reload_time": 2500,
    },
    {   #COMPELTE
        "name": ["Dingo","Dreadnaught Devourer - Tier I", "Dreadnaught Devourer - Tier II","Dreadnaught Devourer - Tier III", "Dreadnaught Devourer - Tier IV","Dreadnaught Devourer - Tier V",],
        "image_path": ["assets/weapons/dingo.png","assets/weapons/dingo_1.png","assets/weapons/dingo_2.png","assets/weapons/dingo_3.png","assets/weapons/dingo_4.png","assets/weapons/dingo_5.png"],
        "bullet_color": [(255, 244, 199),  (222, 255, 255),  (167, 120, 120),  (122, 60, 60),  (12,0,0),  (34, 144,170),  (255, 0,7), ],
        "bullet_size": (4, 4),
        "scale_size": (95, 55),
        "bullet_speed": 35,
        "damage": 28,
        "control_method": "single/auto" ,
        "fire_rate":110,
        "clip_size": 65,     
        "stock_ammo": 195, 
        "reload_time": 4000,
    },
    {   #COMPELTE
        "name": ["MP7","Hyper-7 Havoc - Tier I", "Hyper-14 Havoc - Tier II","Hyper-21 Havoc - Tier III", "Hyper-28 Havoc - Tier IV","Hyper-35 Havoc - Tier V",],
        "image_path": ["assets/weapons/mp7.png","assets/weapons/mp7_1.png","assets/weapons/mp7_2.png","assets/weapons/mp7_3.png","assets/weapons/mp7_4.png","assets/weapons/mp7_5.png",],
        "bullet_color": [(255, 255, 239),  (156, 155, 255),  (155, 155, 120),  (91, 255, 255),  (162,0,255),  (186, 1,255),  (255, 0,187), ],
        "bullet_size": (4, 4),
        "scale_size": (75, 45),
        "bullet_speed": 29,
        "damage": 22,
        "control_method": "single/auto" ,
        "fire_rate":100,
        "clip_size": 30,     
        "stock_ammo": 120, 
        "reload_time": 2000,
    },
    {   #COMPELTE
        "name": ["PDW-57","Predictive Death Wish - Tier I", "Predictive Death Wish - Tier II","Predictive Death Wish - Tier III", "Predictive Death Wish - Tier IV","Predictive Death Wish - Tier V",],
        "image_path": ["assets/weapons/pdw57.png","assets/weapons/pdw57_1.png","assets/weapons/pdw57_2.png","assets/weapons/pdw57_3.png","assets/weapons/pdw57_4.png","assets/weapons/pdw57_5.png",],
        "bullet_color": [(255, 255, 239),  (240, 155, 255),  (245, 100, 120),  (234, 100, 255),  (255,0,155),  (0, 255,255), ],
        "bullet_size": (4, 4),
        "scale_size": (75, 45),
        "bullet_speed": 23,
        "damage": 28,
        "control_method": "single/auto" ,
        "fire_rate":140,
        "clip_size": 50,     
        "stock_ammo": 150, 
        "reload_time": 1700,
    },
    {   #COMPELTE
        "name": ["UMP45","Ultima Moment Paralyzer - Tier I", "Ultima Moment Paralyzer - Tier II","Ultima Moment Paralyzer - Tier III", "Ultima Moment Paralyzer - Tier IV","Ultima Moment Paralyzer - Tier V",],
        "image_path": ["assets/weapons/ump45.png","assets/weapons/ump45_1.png","assets/weapons/ump45_2.png","assets/weapons/ump45_3.png","assets/weapons/ump45_4.png","assets/weapons/ump45_5.png",],
        "bullet_color": [(255, 255, 239),  (230, 255, 0), (230, 255, 0), (230, 255, 0),  (92,130,155),  (255, 0,0), ],
        "bullet_size": (4, 4),
        "scale_size": (95, 59),
        "bullet_speed": 23,
        "damage": 28,
        "control_method": "single/auto" ,
        "fire_rate":140,
        "clip_size": 35,     
        "stock_ammo": 140, 
        "reload_time": 1850,
    },
    {   #COMPELTE
        "name": ["MP5","Ethereal Enforcer - Tier I", "Ethereal Enforcer - Tier II","Ethereal Enforcer - Tier III", "Ethereal Enforcer - Tier IV","Ethereal Enforcer - Tier V",],
        "image_path": ["assets/weapons/mp5.png","assets/weapons/mp5_1.png","assets/weapons/mp5_2.png","assets/weapons/mp5_3.png","assets/weapons/mp5_4.png","assets/weapons/mp5_5.png",],
        "bullet_color": [(255, 255, 239),  (58, 99, 230), (58, 99, 230), (230, 100, 250),  (255,0,185),  (0, 255,30), ],
        "bullet_size": (4, 4),
        "scale_size": (75, 35),
        "bullet_speed": 25,
        "damage": 27,
        "control_method": "single/auto" ,
        "fire_rate":120,
        "clip_size": 30,     
        "stock_ammo": 120, 
        "reload_time": 1700,
    },
    {   #COMPELTE
        "name": ["Galil","The Lamentation - Tier I", "The Lamentation - Tier II","The Lamentation - Tier III", "The Lamentation - Tier IV","The Lamentation - Tier V",],
        "image_path": ["assets/weapons/galil.png","assets/weapons/galil_1.png","assets/weapons/galil_2.png","assets/weapons/galil_3.png","assets/weapons/galil_4.png","assets/weapons/galil_5.png",],
        "bullet_color": [(255, 255, 239),  (233, 99, 22), (233, 99, 22), (230, 0, 0),  (0,255,35),  (255, 22,230), ],
        "bullet_size": (4, 4),
        "scale_size": (95, 55),
        "bullet_speed": 35,
        "damage": 33,
        "control_method": "single/auto" ,
        "fire_rate":150,
        "clip_size": 35,     
        "stock_ammo": 140, 
        "reload_time": 1600,
    },
    {   #COMPELTE
        "name": ["ACR","Apex Predator - Tier I", "Apex Predator - Tier II","Apex Predator - Tier III", "Apex Predator - Tier IV","Apex Predator - Tier V",],
        "image_path": ["assets/weapons/acr.png",],
        "bullet_color": [(255, 255, 239),  (233, 99, 22), (233, 99, 22), (230, 20, 220),  (0,255,35),  (255, 0,0), ],
        "bullet_size": (4, 4),
        "scale_size": (95, 55),
        "bullet_speed": 25,
        "damage": 31,
        "control_method": "single/auto" ,
        "fire_rate":130,
        "clip_size": 30,     
        "stock_ammo": 150, 
        "reload_time": 1750,
    },
    {   #COMPELTE
        "name": ["Krig 6","Kraken's Kiss - Tier I", "Kraken's Kiss - Tier II","Kraken's Kiss - Tier III", "Kraken's Kiss - Tier IV","Kraken's Kiss - Tier V",],
        "image_path": ["assets/weapons/krig6.png","assets/weapons/krig6_1.png","assets/weapons/krig6_2.png","assets/weapons/krig6_3.png","assets/weapons/krig6_4.png","assets/weapons/krig6_5.png",],
        "bullet_color": [(255, 255, 239),  (230, 255, 209),  (230, 255, 209),(230, 26, 160),  (0,255,35),  (255, 0,0) ],
        "bullet_size": (4, 4),
        "scale_size": (95, 55),
        "bullet_speed": 41,
        "damage": 21,
        "control_method": "single/auto" ,
        "fire_rate":145,
        "clip_size": 30,     
        "stock_ammo": 150, 
        "reload_time": 1650,
    },

    {   #COMPELTE
        "name": ["Commando","Kaleidoscope XM8 - Tier I", "Kaleidoscope XM16 - Tier II","Kaleidoscope XM24 - Tier III", "Kaleidoscope XM32 - Tier IV","Kaleidoscope XM40 - Tier V",],
        "image_path": ["assets/weapons/commando.png","assets/weapons/commando_1.png","assets/weapons/commando_2.png","assets/weapons/commando_3.png","assets/weapons/commando_4.png","assets/weapons/commando_5.png",],
        "bullet_color": [(255, 255, 239),  (200, 99, 200), (170, 99, 170), (120, 20, 120),  (60,255,60),  (0, 255,0), ],
        "bullet_size": (4, 4),
        "scale_size": (95, 55),
        "bullet_speed": 33,
        "damage": 27,
        "control_method": "single/auto" ,
        "fire_rate":158,
        "clip_size": 30,     
        "stock_ammo": 150, 
        "reload_time": 1750,
    },
    {   #COMPELTE
        "name": ["Grau 5.56","Verdansk's Needle - Tier I", "Verdansk's Needle - Tier II","Verdansk's Needle - Tier III", "Verdansk's Needle - Tier IV","Verdansk's Needle - Tier V",],
        "image_path": ["assets/weapons/grau.png","assets/weapons/grau_1.png","assets/weapons/grau_2.png","assets/weapons/grau_3.png","assets/weapons/grau_4.png","assets/weapons/grau_5.png",],
        "bullet_color": [(255, 255, 239),  (0, 205, 255),  (0, 205, 255),(255,137 , 0),  (0, 205, 255) ,(255, 0,253) ],
        "bullet_size": (5,5),
        "scale_size": (95, 55),
        "bullet_speed": 40,
        "damage": 23,
        "control_method": "single/auto" ,
        "fire_rate":135,
        "clip_size": 30,     
        "stock_ammo": 150, 
        "reload_time": 2300,
    },

    {   #COMPELTE
        "name": ["AS VAL","Andromeda Vanquish  - Tier I", "Andromeda Vanquish - Tier II","Andromeda Vanquish - Tier III", "Andromeda Vanquish - Tier IV","Andromeda Vanquish - Tier V",],
        "image_path": ["assets/weapons/asval.png","assets/weapons/asval_1.png","assets/weapons/asval_2.png","assets/weapons/asval_3.png","assets/weapons/asval_4.png","assets/weapons/asval_5.png",],
        "bullet_color": [(255, 255, 239),  (255, 255, 0), (255, 0, 222), (255, 20, 0),  (0,244,255),  (255, 127,0), ],
        "bullet_size": (7, 7),
        "scale_size": (95, 55),
        "bullet_speed": 50,
        "damage": 40,
        "control_method": "single/auto" ,
        "fire_rate":90,
        "clip_size": 10,     
        "stock_ammo": 80, 
        "reload_time": 2100,
    },
    {   #COMPELTE
        "name": ["G36C","Drogon - Tier I", "Drogon - Tier II","Drogon - Tier III", "Drogon - Tier IV","Drogon - Tier V",],
        "image_path": ["assets/weapons/g36c.png","assets/weapons/g36c_1.png","assets/weapons/g36c_2.png","assets/weapons/g36c_3.png","assets/weapons/g36c_4.png","assets/weapons/g36c_5.png",],
        "bullet_color": [(255, 255, 239),  (0, 205, 255),  (0, 205, 255),(255,137 , 0),  (0, 205, 255) ,(255, 0,253) ],
        "bullet_size": (5,5),
        "scale_size": (75, 48),
        "bullet_speed": 40,
        "damage": 30,
        "control_method": "single/auto" ,
        "fire_rate":140,
        "clip_size": 30,     
        "stock_ammo": 120, 
        "reload_time": 2300,
    },

    {   #COMPELTE
        "name": ["Ak-74u","74 Ulterior Phantom - Tier I", "74 Ulterior Phantom - Tier II","74 Ulterior Phantom - Tier III", "74 Ulterior Phantom - Tier IV","74 Ulterior Phantom - Tier V",],
        "image_path": ["assets/weapons/ak74u.png","assets/weapons/ak74u_1.png","assets/weapons/ak74u_2.png","assets/weapons/ak74u_3.png","assets/weapons/ak74u_4.png","assets/weapons/ak74u_5.png",],
        "bullet_color": [(255, 255, 239),  (255, 255, 0), (255, 0, 222), (255, 20, 0),  (0,244,255),  (255, 255,255), ],
        "bullet_size": (4, 4),
        "scale_size": (95, 55),
        "bullet_speed": 35,
        "damage": 26,
        "control_method": "single/auto" ,
        "fire_rate":155,
        "clip_size": 30,     
        "stock_ammo": 90, 
        "reload_time": 1800,
    },
    {   #COMPELTE
        "name": ["Mini-Uzi","Pocket Pulverizer - Tier I", "Pocket Pulverizer - Tier II","Pocket Pulverizer - Tier III", "Pocket Pulverizer - Tier IV","Pocket Pulverizer - Tier V",],
        "image_path": ["assets/weapons/miniuzi.png","assets/weapons/g36c_1.png","assets/weapons/g36c_2.png","assets/weapons/g36c_3.png","assets/weapons/g36c_4.png","assets/weapons/g36c_5.png",],
        "bullet_color": [(255, 255, 239),  (255, 23,255), (255, 23,255), (255, 23,255),  (0, 205, 12) ,(255, 0,253) ],
        "bullet_size": (3,3),
        "scale_size": (60, 41),
        "bullet_speed": 55,
        "damage": 21,
        "control_method": "single/auto" ,
        "fire_rate":104,
        "clip_size": 30,     
        "stock_ammo": 120, 
        "reload_time": 2200,
    },

    {   #COMPELTE
        "name": ["MSMC","Mystic Mauler - Tier I", "Mystic Mauler - Tier II","Mystic Mauler - Tier III", "Mystic Mauler - Tier IV","Mystic Mauler - Tier V",],
        "image_path": ["assets/weapons/msmc.png","assets/weapons/ak74u_1.png","assets/weapons/ak74u_2.png","assets/weapons/ak74u_3.png","assets/weapons/ak74u_4.png","assets/weapons/ak74u_5.png",],
        "bullet_color": [(255, 255, 239),  (255, 123, 255), (158, 34, 222), (242, 20, 220),  (0,244,21),  (0, 255,5), ],
        "bullet_size": (4.5, 4.5),
        "scale_size": (65, 35),
        "bullet_speed": 36,
        "damage": 28,
        "control_method": "single/auto" ,
        "fire_rate":155,
        "clip_size": 30,     
        "stock_ammo": 90, 
        "reload_time": 1800,
    },
    {   #COMPELTE
        "name": ["Mac-10","Mystic Mach-5 - Tier I", "Mystic Mach-5 - Tier II","Mystic Mach-5 - Tier III", "Mystic Mach-5 - Tier IV","Mystic Mach-5 - Tier V",],
        "image_path": ["assets/weapons/mac10.png","assets/weapons/mac10_1.png","assets/weapons/mac10_2.png","assets/weapons/mac10_3.png","assets/weapons/mac10_4.png","assets/weapons/mac10_5.png",],
        "bullet_color": [(255, 255, 239),  (255, 255,255), (0, 255,0), (255, 0,255), (255, 0,255), (0, 210,253) ],
        "bullet_size": (4,4),
        "scale_size": (80, 51),
        "bullet_speed": 45,
        "damage": 20,
        "control_method": "single/auto" ,
        "fire_rate":98,
        "clip_size": 25,     
        "stock_ammo": 125, 
        "reload_time": 1950,
    },

    {   #COMPELTE
        "name": ["Groza","Grizzly Goliath - Tier I", "Grizzly Goliath - Tier II","Grizzly Goliath - Tier III", "Grizzly Goliath - Tier IV","Grizzly Goliath - Tier V",],
        "image_path": ["assets/weapons/groza.png","assets/weapons/groza_1.png","assets/weapons/groza_2.png","assets/weapons/groza_3.png","assets/weapons/groza_4.png","assets/weapons/groza_5.png",],
        "bullet_color": [(255, 255, 239),  (255, 123, 255), (158, 34, 222), (0, 220, 22),  (0,244,21),  (245, 0,235), ],
        "bullet_size": (4.5, 4.5),
        "scale_size": (70, 41),
        "bullet_speed": 42,
        "damage": 26,
        "control_method": "single/auto" ,
        "fire_rate":143,
        "clip_size": 40,     
        "stock_ammo": 160, 
        "reload_time": 2000,
    },
    {   #COMPELTE
        "name": ["FAL","One Punch- Tier I", "One Punch - Tier II","One Punch - Tier III", "One Punch - Tier IV","One Punch - Tier V",],
        "image_path": ["assets/weapons/fal.png","assets/weapons/fal_1.png","assets/weapons/fal_2.png","assets/weapons/fal_3.png","assets/weapons/fal_4.png","assets/weapons/fal_5.png",],
        "bullet_color": [(255, 255, 239),  (0, 234, 255), (0, 234, 222), (0, 220, 22),  (0,244,0),  (245, 0,235), ],
        "bullet_size": (7,7),
        "scale_size": (80, 51),
        "bullet_speed": 55,
        "damage": 48,
        "control_method": "single/auto" ,
        "fire_rate":330,
        "clip_size": 20,     
        "stock_ammo": 100, 
        "reload_time": 1950,
    },

    {   #COMPELTE
        "name": ["M93 Raffica","Neapolitan Gust  - Tier I", "Neapolitan Gust  - Tier II","Neapolitan Gust  - Tier III", "Neapolitan Gust  - Tier IV","Neapolitan Gust  - Tier V",],
        "image_path": ["assets/weapons/m93.png","assets/weapons/m93_1.png","assets/weapons/m93_2.png","assets/weapons/m93_3.png","assets/weapons/m93_4.png","assets/weapons/m93_5.png",],
        "bullet_color": [(255, 255, 239),  (165, 34, 240), (165, 34, 240), (222, 220, 22),  (0,244,240),  (0, 240,0), ],
        "bullet_size": (4.5, 4.5),
        "scale_size": (50, 31),
        "bullet_speed": 49,
        "damage": 24,
        "control_method": "burst" ,
        "fire_rate":143,
        "clip_size": 15,     
        "stock_ammo": 120, 
        "reload_time": 2100,
    },
    {   #COMPELTE
        "name": ["Kar98K","The Armageddon - Tier I", "The Armageddon - Tier II","The Armageddon - Tier III", "The Armageddon - Tier IV","The Armageddon - Tier V",],
        "image_path": ["assets/weapons/kar98k.png","assets/weapons/kar98k_1.png","assets/weapons/kar98k_2.png","assets/weapons/kar98k_3.png","assets/weapons/kar98k_4.png","assets/weapons/kar98k_5.png"],
        "bullet_color": [(255, 213, 178),(255, 0, 0),(255, 0, 2),(255, 255, 178),(255, 255, 228),(0, 120, 216),],
        "bullet_size": (8, 8),
        "scale_size": (95, 45),
        "bullet_speed": 88,
        "damage": 100,
        "control_method": "single/auto" ,
        "fire_rate":650,
        "clip_size": 6,     
        "stock_ammo": 36, 
        "reload_time": 2900,
    },
    {   #COMPELTE
        "name": ["Intervention","Exploitation - Tier I", "Exploitation - Tier II","Exploitation - Tier III", "Exploitation - Tier IV","Exploitation - Tier V",],
        "image_path": ["assets/weapons/intervention.png","assets/weapons/intervention_1.png","assets/weapons/intervention_2.png","assets/weapons/intervention_3.png","assets/weapons/intervention_4.png","assets/weapons/intervention_5.png"],
        "bullet_color": [(255, 213, 178),(131, 32, 229),(32, 108, 222),(235, 8, 212),(0, 250, 1),(188, 114, 230),],
        "bullet_size": (8, 8),
        "scale_size": (95, 45),
        "bullet_speed": 79,
        "damage": 90,
        "control_method": "single/auto" ,
        "fire_rate":750,
        "clip_size": 7,     
        "stock_ammo": 42, 
        "reload_time": 2000,
    },
    {   #COMPELTE
        "name": ["DSR 50","DoomSight Recon 50 - Tier I", "DoomSight Recon 50 - Tier II","DoomSight Recon 50 - Tier III", "DoomSight Recon 50 - Tier IV","DoomSight Recon 50 - Tier V",],
        "image_path": ["assets/weapons/dsr50.png","assets/weapons/dsr50_1.png","assets/weapons/dsr50_2.png","assets/weapons/dsr50_3.png","assets/weapons/dsr50_4.png","assets/weapons/dsr50_5.png"],
        "bullet_color": [(255, 213, 178),(0, 233, 9),(3, 238, 2),(188, 123, 212),(255, 0, 1),(255, 1, 243),],
        "bullet_size": (8, 8),
        "scale_size": (95, 45),
        "bullet_speed": 79,
        "damage": 105,
        "control_method": "single/auto" ,
        "fire_rate":750,
        "clip_size": 5,     
        "stock_ammo": 25, 
        "reload_time": 2400,
    },
    {   #COMPELTE
        "name": ["Ballista","Old Man's Rifle - Tier I", "Old Man's Rifle - Tier II","Old Man's Rifle - Tier III", "Old Man's Rifle - Tier IV","Old Man's Rifle - Tier V",],
        "image_path": ["assets/weapons/ballista.png","assets/weapons/ballista_1.png","assets/weapons/ballista_2.png","assets/weapons/ballista_3.png","assets/weapons/ballista_4.png","assets/weapons/ballista_5.png"],
        "bullet_color": [(255, 213, 178),(131, 32, 229),(32, 108, 222),(235, 8, 212),(0, 250, 1),(188, 114, 230),],
        "bullet_size": (8, 8),
        "scale_size": (115, 38),
        "bullet_speed": 71,
        "damage": 88,
        "control_method": "single/auto" ,
        "fire_rate":700,
        "clip_size": 7,     
        "stock_ammo": 42, 
        "reload_time": 2100,
    },
    {   #COMPELTE
        "name": ["AS-50","Atherscope - Tier I", "Atherscope - Tier II","Atherscope - Tier III", "Atherscope - Tier IV","Atherscope - Tier V",],
        "image_path": ["assets/weapons/as50.png","assets/weapons/as50_1.png","assets/weapons/as50_2.png","assets/weapons/as50_3.png","assets/weapons/as50_4.png","assets/weapons/as50_5.png"],
        "bullet_color": [(187, 78, 255),(187, 78, 255),(255, 2, 214),(188, 123, 212),(0, 255, 1),(0, 255, 243),],
        "bullet_size": (8, 8),
        "scale_size": (105, 54),
        "bullet_speed": 74,
        "damage": 80,
        "control_method": "single/auto" ,
        "fire_rate":600,
        "clip_size": 8,     
        "stock_ammo": 40, 
        "reload_time": 1900,
    },
    {   #COMPLETE 
        "name": ["AA-12", "Ectoplasmic Eradicator - Tier I", "Ectoplasmic Eradicator - Tier II", "Ectoplasmic Eradicator - Tier III", "Ectoplasmic Eradicator - Tier IV","Ectoplasmic Eradicator - Tier V"],
        "image_path": ["assets/weapons/aa12.png","assets/weapons/aa12_1.png","assets/weapons/aa12_2.png","assets/weapons/aa12_3.png","assets/weapons/aa12_4.png","assets/weapons/aa12_5.png",],
        "bullet_color": [(255,255,255), (243, 0, 255),(0, 240, 255), (243, 0, 255),(250, 0, 5),(233, 0, 255),],
        "bullet_size": (5, 5),
        "scale_size": (90, 45),
        "bullet_speed": 20,
        "damage": 51,
        "control_method": "shotgun",
        "fire_rate":400,
        "clip_size": 8,     
        "stock_ammo": 48, 
        "reload_time": 3000
    },
    {   #COMPLETE 
        "name": ["Striker", "Pandemonium Pummeler - Tier I", "Pandemonium Pummeler - Tier II", "Pandemonium Pummeler - Tier III", "Pandemonium Pummeler - Tier IV","Pandemonium Pummeler - Tier V"],
        "image_path": ["assets/weapons/striker.png","assets/weapons/striker_1.png","assets/weapons/striker_2.png","assets/weapons/striker_3.png","assets/weapons/striker_4.png","assets/weapons/striker_5.png",],
        "bullet_color": [(255,255,255),(255, 255, 255), (143, 200, 255),(243, 0, 255),(110, 255, 135),(243, 0, 255),],
        "bullet_size": (5, 5),
        "scale_size": (90, 49),
        "bullet_speed": 20,
        "damage": 48,
        "control_method": "shotgun",
        "fire_rate":400,
        "clip_size": 8,     
        "stock_ammo": 48, 
        "reload_time": 9000
    },
    {   #COMPLETE 
        "name": ["Model 1887", "Winchester M2064- Tier I", "Winchester M2064 - Tier II", "Winchester M2064 - Tier III", "Winchester M2064 - Tier IV","Winchester M2064 - Tier V"],
        "image_path": ["assets/weapons/model.png","assets/weapons/model_1.png","assets/weapons/model_2.png","assets/weapons/model_3.png","assets/weapons/model_4.png","assets/weapons/model_5.png",],
        "bullet_color": [(255,255,255), (28, 145, 23),(12, 220, 45), (243, 255, 255),(246, 110, 35),(73, 160, 255),],
        "bullet_size": (5, 5),
        "scale_size": (90, 45),
        "bullet_speed": 20,
        "damage": 50,
        "control_method": "shotgun",
        "fire_rate":700,
        "clip_size": 6,     
        "stock_ammo": 36, 
        "reload_time": 4500
    },
    {   #COMPLETE 
        "name": ["KSG", "Killoiath - Tier I", "Killoiath - Tier II", "Killoiath - Tier III", "Killoiath - Tier IV","Killoiath - Tier V"],
        "image_path": ["assets/weapons/ksg.png","assets/weapons/ksg_1.png","assets/weapons/ksg_2.png","assets/weapons/ksg_3.png","assets/weapons/ksg_4.png","assets/weapons/ksg_5.png",],
        "bullet_color": [(255,255,255),(74, 95, 255), (255, 0, 235),(0, 255, 5),(255, 5, 215),(0, 250, 245),],
        "bullet_size": (8.5, 8.5),
        "scale_size": (90, 49),
        "bullet_speed": 35,
        "damage": 90,
        "control_method": "single/auto",
        "fire_rate":550,
        "clip_size": 8,     
        "stock_ammo": 48, 
        "reload_time": 6000
    },
    {   #COMPLETE
        "name": ["Ray Gun","Porter's X2 Ray Gun - Tier I","Porter's X2 Ray Gun - Tier II","Porter's X2 Ray Gun - Tier III","Porter's X2 Ray Gun - Tier IV","Porter's X2 Ray Gun - Tier V",],
        "image_path": ["assets/weapons/raygun.png","assets/weapons/raygun_1.png","assets/weapons/raygun_2.png","assets/weapons/raygun_3.png","assets/weapons/raygun_4.png","assets/weapons/raygun_5.png",],
        "bullet_color": [(0, 255, 0),  (254, 9, 2),(248, 9, 5), (228, 9, 2), (238, 9, 2), (1, 255, 255), ],
        "bullet_size": (7, 7),
        "scale_size": (78, 55),
        "bullet_speed": 60,
        "damage": 82,
        "control_method": "single/auto",
        "fire_rate":450,
        "clip_size": 20,     
        "stock_ammo": 100, 
        "reload_time": 2300
    },
    {   #COMPLETE 
        "name": ["Ray Gun Mark III", "Porter's X3 Atom Bomb - Tier I", "Porter's X3 Atom Bomb - Tier II", "Porter's X3 Atom Bomb - Tier III", "Porter's X3 Atom Bomb - Tier IV","Porter's X3 Atom Bomb - Tier V"],
        "image_path": ["assets/weapons/raygun3.png","assets/weapons/raygun3_1.png","assets/weapons/raygun3_2.png","assets/weapons/raygun3_3.png","assets/weapons/raygun3_4.png","assets/weapons/raygun3_5.png",],
        "bullet_color": [(0, 255, 0), (198, 9, 255), (198, 9, 255), (198, 9, 255), (198, 9, 255), (255, 0, 0), ],
        "bullet_size": (5, 5),
        "scale_size": (90, 45),
        "bullet_speed": 40,
        "damage": 67,
        "control_method": "shotgun",
        "fire_rate":450,
        "clip_size": 21,     
        "stock_ammo": 84, 
        "reload_time": 3000
    },
    {   #COMPLETE 
        "name": ["Olympia", "Winchester M2064- Tier I", "Winchester M2064 - Tier II", "Winchester M2064 - Tier III", "Winchester M2064 - Tier IV","Winchester M2064 - Tier V"],
        "image_path": ["assets/weapons/olympia.png","assets/weapons/olympia_1.png","assets/weapons/olympia_2.png","assets/weapons/olympia_3.png","assets/weapons/olympia_4.png","assets/weapons/olympia_5.png",],
        "bullet_color": [(255,255,255),(255,0,1), (255,0,1), (255,0,1), (2,255,178), (0,255,251), ],
        "bullet_size": (5, 5),
        "scale_size": (100, 55),
        "bullet_speed": 43,
        "damage": 71,
        "control_method": "shotgun",
        "fire_rate":700,
        "clip_size": 2,     
        "stock_ammo": 24, 
        "reload_time": 3000
    },
    {   #COMPLETE 
        "name": ["Blundergat", "Acidgat - Tier I", "Thundergat - Tier II", "Novagat - Tier III", "Bloodygat - Tier IV","Quantumgat - Tier V"],
        "image_path": ["assets/weapons/blundergatt.png","assets/weapons/blundergatt_1.png","assets/weapons/blundergatt_2.png","assets/weapons/blundergatt_3.png","assets/weapons/blundergatt_4.png","assets/weapons/blundergatt_5.png",],
        "bullet_color": [(255,1,2),(7, 255, 5), (2, 255, 179),(0, 255, 255),(165, 5, 175),(255, 0, 162),],
        "bullet_size": (8.5, 8.5),
        "scale_size": (95, 55),
        "bullet_speed": 65,
        "damage": 114,
        "control_method": "shotgun",
        "fire_rate":50,
        "clip_size": 2,     
        "stock_ammo": 12, 
        "reload_time": 1000
    },
    {   #COMPLETE 
        "name": ["Nexus Hand Cannon", "Diplomatic Bazooka - Tier I", "Diplomatic Bazooka - Tier II", "Diplomatic Bazooka - Tier III", "Diplomatic Bazooka - Tier IV","Diplomatic Bazooka - Tier V"],
        "image_path": ["assets/weapons/handcanon.png","assets/weapons/handcanon_1.png","assets/weapons/handcanon_2.png","assets/weapons/handcanon_3.png","assets/weapons/handcanon_4.png","assets/weapons/handcanon_5.png",],
        "bullet_color": [(255,255,255),(255,0,1), (0,85,251), (0,85,251), (2,255,178), (245,0,161), ],
        "bullet_size": (7, 7),
        "scale_size": (90, 55),
        "bullet_speed": 63,
        "damage": 78,
        "control_method": "shotgun",
        "fire_rate":400,
        "clip_size": 6,     
        "stock_ammo": 36, 
        "reload_time": 3300
    },
    {   #COMPLETE 
        "name": ["Neon Nexus Rifle", "Diplomatic Blister Rifle - Tier I", "Diplomatic Blister Rifle - Tier II", "Diplomatic Blister Rifle - Tier III", "Diplomatic Blister Rifle - Tier IV","Diplomatic Blister Rifle - Tier V"],
        "image_path": ["assets/weapons/rifle.png","assets/weapons/rifle_1.png","assets/weapons/rifle_2.png","assets/weapons/rifle_3.png","assets/weapons/rifle_4.png","assets/weapons/rifle_5.png",],
        "bullet_color": [(255,1,2),(255, 5, 5), (255, 5, 0),(0, 255, 11),(222, 5, 255),(51, 115, 255),],
        "bullet_size": (5.5, 5.5),
        "scale_size": (95, 55),
        "bullet_speed": 65,
        "damage": 39,
        "control_method": "single/auto",
        "fire_rate":90,
        "clip_size": 25,     
        "stock_ammo": 125, 
        "reload_time": 2000
    },
    {   #COMPLETE 
        "name": ["Quantum Raptor MG", "Chrono Catalyst - Tier I", "Chrono Catalyst - Tier II", "Chrono Catalyst - Tier III", "Chrono Catalyst - Tier IV","Chrono Catalyst - Tier V"],
        "image_path": ["assets/weapons/raptor.png","assets/weapons/raptor_1.png","assets/weapons/raptor_2.png","assets/weapons/raptor_3.png","assets/weapons/raptor_4.png","assets/weapons/raptor_5.png",],
        "bullet_color": [(255,255,255),(255,190,1), (255,0,1), (255,0,1), (2,255,178), (0,255,251), ],
        "bullet_size": (4, 4),
        "scale_size": (95, 51),
        "bullet_speed": 20,
        "damage": 20,
        "control_method": "shotgun",
        "fire_rate":100,
        "clip_size": 20,     
        "stock_ammo": 140, 
        "reload_time": 6000
    },
    {   #COMPLETE 
        "name": ["R.A.I. K-84", "Discordian Disruptor - Tier I", "Discordian Disruptor - Tier II", "Discordian Disruptor - Tier III", "Discordian Disruptor - Tier IV","Discordian Disruptor - Tier V"],
        "image_path": ["assets/weapons/raik.png","assets/weapons/raik_1.png","assets/weapons/raik_2.png","assets/weapons/raik_3.png","assets/weapons/raik_4.png","assets/weapons/raik_5.png",],
        "bullet_color": [(255,1,2),(177, 1, 255), (177, 1, 255),(244, 0, 255),(177, 1, 255),(255, 0, 0),],
        "bullet_size": (5.5, 5.5),
        "scale_size": (90, 45),
        "bullet_speed": 50,
        "damage": 40,
        "control_method": "single/auto",
        "fire_rate":140,
        "clip_size": 30,     
        "stock_ammo": 90, 
        "reload_time": 1900
    },
    {   #COMPELTE
        "name": ["Stoner63","Bifrost Friction - Tier I", " Bifrost Friction - Tier II","Bifrost Friction - Tier III", "Bifrost Friction - Tier IV","Bifrost Friction - Tier V",],
        "image_path": ["assets/weapons/stoner.png","assets/weapons/stoner_1.png","assets/weapons/stoner_2.png","assets/weapons/stoner_3.png","assets/weapons/stoner_4.png","assets/weapons/stoner_5.png"],
        "bullet_color": [(255, 244, 199),  (196, 56, 255),  (167, 120, 120),  (56, 78, 255),   (12,0,0),  (0, 245,255),  (0, 255,7), ],
        "bullet_size": (6, 6),
        "scale_size": (95, 35),
        "bullet_speed": 55,
        "damage": 32,
        "control_method": "single/auto" ,
        "fire_rate":160,
        "clip_size": 60,     
        "stock_ammo": 180, 
        "reload_time": 3100,
    },
    {   #COMPELTE
        "name": ["RPD","Realistic Punishing Device  - Tier I", "Realistic Punishing Device - Tier II","Realistic Punishing Device - Tier III", "Realistic Punishing Device - Tier IV","Realistic Punishing Device - Tier V",],
        "image_path": ["assets/weapons/rpd.png","assets/weapons/rpd_1.png","assets/weapons/rpd_2.png","assets/weapons/rpd_3.png","assets/weapons/rpd_4.png","assets/weapons/rpd_5.png"],
        "bullet_color": [(255, 244, 199),  (222, 1, 5),  (255, 0, 0),  (200,0,0),  (0, 244,230),  (5, 250,247), ],
        "bullet_size": (6, 6),
        "scale_size": (95, 35),
        "bullet_speed": 35,
        "damage": 31,
        "control_method": "single/auto" ,
        "fire_rate":120,
        "clip_size": 80,     
        "stock_ammo": 240, 
        "reload_time": 7000,
    },
    {   #COMPELTE
        "name": ["HAMR","STRM BRKR - Tier I", "STRM BRKR - Tier II","STRM BRKR - Tier III", "STRM BRKR - Tier IV","STRM BRKR - Tier V",],
        "image_path": ["assets/weapons/hamr.png","assets/weapons/hamr_1.png","assets/weapons/hamr_2.png","assets/weapons/hamr_3.png","assets/weapons/hamr_4.png","assets/weapons/hamr_5.png"],
        "bullet_color": [(255, 244, 199),  (222, 5, 5),  (199, 0, 0),  (0, 255, 6),  (7, 244,230),  (1, 230,255), ],
        "bullet_size": (7, 7),
        "scale_size": (115, 48),
        "bullet_speed": 45,
        "damage": 33,
        "control_method": "single/auto" ,
        "fire_rate":140,
        "clip_size": 70,     
        "stock_ammo": 210, 
        "reload_time": 2900,
    },
    {   #COMPELTE
        "name": ["Colt 1911","Mustang - Tier I", "Mustang - Tier II","Mustang - Tier III", "Mustang - Tier IV","Mustang - Tier V",],
        "image_path": ["assets/weapons/m1911.png","assets/weapons/m1911_1.png","assets/weapons/m1911_2.png","assets/weapons/m1911_3.png","assets/weapons/m1911_4.png","assets/weapons/m1911_5.png",],
        "bullet_color": [(213, 213, 178), (77,2,255), (229,1,4), (77,2,255), (148,6,215),(3,43,219),  ],
        "bullet_size": (5, 5),
        "scale_size": (45, 45),
        "bullet_speed": 37,
        "damage": 21,
        "control_method": "single/auto" ,
        "fire_rate":400,
        "clip_size": 9,     
        "stock_ammo": 36, 
        "reload_time": 1800,
    },
]