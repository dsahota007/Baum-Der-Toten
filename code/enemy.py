
import pygame, sys
import math
import pytmx
from level import scale_factor, Box
from pytmx.util_pygame import load_pygame
import random

all_blood_effects = []

class Enemy:
    def __init__(self, screen, x, y, ui, max_health=100):
        self.screen = screen
        self.default_image_width = 54
        self.default_image_height = 59
        self.image = pygame.image.load('assets/zombie/right_side/right_idle/idle1.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.default_image_width, self.default_image_height))  #instead of an x and y value i threw these in 
        self.enemy_rect = self.image.get_rect(center=(x, y))
        self.possible_speeds = [1.60, 1.65, 1.7, 1.75,1.8,1.9,2.2,2.5,2.6]
        self.speed = random.choice(self.possible_speeds)
        self.original_speed = self.speed
        self.direction = 1  # 1 for right, -1 for left
        self.vertical_speed = 0  # Vertical speed (used for gravity)
        self.gravity = 0.3
        self.tmx_data = load_pygame('assets/maps/platform2.tmx')
        
        self.walk_right_frames = [self.scale_image(pygame.image.load(f'assets/zombie/right_side/right_run/run{i}.png')) for i in range(1, 8)]
        self.walk_left_frames = [self.scale_image(pygame.image.load(f'assets/zombie/left_side/left_run/run{i}.png')) for i in range(1, 8)]
        self.idle_right_frames = [self.scale_image(pygame.image.load(f'assets/zombie/right_side/right_idle/idle{i}.png')) for i in range(1, 8)]
        self.idle_left_frames = [self.scale_image(pygame.image.load(f'assets/zombie/left_side/left_idle/idle{i}.png')) for i in range(1, 8)]
        self.attack_frames = [self.scale_image(pygame.image.load(f'assets/zombie/right_side/right_attack/attack{i}.png')) for i in range(1, 6)]
        self.attack_left_frames = [self.scale_image(pygame.image.load(f'assets/zombie/left_side/left_attack/attack{i}.png')) for i in range(1, 6)]
        self.death_right_frames = [self.scale_image(pygame.image.load(f'assets/zombie/right_side/right_death/death{i}.png')) for i in range(1, 6)]
        self.death_left_frames = [self.scale_image(pygame.image.load(f'assets/zombie/left_side/left_death/death{i}.png')) for i in range(1, 6)]
        self.active_frames = self.idle_right_frames  # Default to idle frames
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        # Initialize animation attributes
        
        self.animation_speed = 100
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.last_collision_time = 0
        self.is_attacking = False
        
        #health
        self.ui = ui
        self.last_health_recovery_time = pygame.time.get_ticks()
        self.box = Box(self.enemy_rect.x, self.enemy_rect.y, self.default_image_width, self.default_image_height)

        self.health = max_health        
        self.blood_effects = []
        
    def add_blood_effect(self, x_offset, y_offset):
        folder_number = random.randint(1, 2)
        blood_sprites = [pygame.image.load(f"assets/animation/zombie_blood/{folder_number}/{i}.png") for i in range(1, 28)]
        
        effect = BloodEffect(self, x_offset, y_offset, blood_sprites)
        all_blood_effects.append(effect)
    def reset_speed(self):
        self.speed = self.original_speed
                
    def scale_image(self, image, width=None, height=None):
        if width is None:
            width = self.default_image_width
        if height is None:
            height = self.default_image_height
        return pygame.transform.scale(image, (width, height))

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.active_frames)
            self.image = self.active_frames[self.current_frame]

    def enemy_movement(self, player_x, player_rect):  # Note: added player_rect parameter
        # Move towards the player
        if self.enemy_rect.x < player_x:
            self.enemy_rect.x += self.speed
        elif self.enemy_rect.x > player_x:
            self.enemy_rect.x -= self.speed

        # Apply gravity to the vertical speed
        self.vertical_speed += self.gravity
        self.enemy_rect.y += self.vertical_speed

        # Check for collision after vertical movement
        collision = self.check_enemy_collision(tmx_data=self.tmx_data)
        if collision:
            #print("Collision Detected!")
            # Binary search for optimization
            low, high = 0, self.vertical_speed
            while low <= high:
                mid = (low + high) // 2
                self.enemy_rect.y -= mid
                if self.check_enemy_collision(tmx_data=self.tmx_data):
                    low = mid + 1
                else:
                    high = mid - 1
                self.enemy_rect.y += mid  # Reset position after checking

            self.enemy_rect.y -= low  # Correct the position using the final "low" value
            self.vertical_speed = 0
        self.box.rect.topleft = self.enemy_rect.topleft
            # You can add additional logic here for game over or other responses.

    def check_enemy_collision(self, tmx_data):
        for layer in tmx_data.layers:
            if isinstance(layer, pytmx.TiledObjectGroup) and layer.name == "Object Layer 1":
                for obj in layer:
                    # Scale the collision object
                    scaled_rect = pygame.Rect(int(obj.x * scale_factor), int(obj.y * scale_factor), int(obj.width * scale_factor), int(obj.height * scale_factor))
                    if self.enemy_rect.colliderect(scaled_rect):
                        return True
        return False
        
    def check_collision_with_player(self, player):
        if self.enemy_rect.colliderect(player.player_rect):
            damage_multiplier = 0.50001000001 if player.has_juggernog else 2
            self.ui.health_rect.width -= damage_multiplier
            
            if self.ui.health_rect.width <= 0:
                
                if player.has_selfmed:
                    player.is_downed = True 
                    player.downs += 1
                    self.ui.health_rect.width = 295  
                    player.selfmed_uses += 1
                    player.has_juggernog = False
                    player.has_quickrevive = False
                    player.has_staminup = False
                    player.has_speedcola = False
                    player.has_doubletap = False
                    player.has_blunderbullet = False
                    player.has_electriccherry = False
                    player.has_selfmed = False
                    player.has_flashstepmastery = False
                else:
                    player.is_dead = True
                
            return True
        return False

    def chase(self, player, tmx_data):
        # Store the original position
        original_x = self.enemy_rect.x
        
        # Get the horizontal direction vector
        dx = player.player_rect.x - self.enemy_rect.x

        # Move the enemy horizontally towards the player
        if dx > 0:  # Player is to the right
            self.enemy_rect.x += self.speed
            self.active_frames = self.walk_right_frames
            self.direction = 1
        elif dx < 0:  # Player is to the left
            self.enemy_rect.x -= self.speed
            self.active_frames = self.walk_left_frames
            self.direction = -1

        # Check for horizontal collision after movement
        if self.check_enemy_collision(tmx_data):
            # If collided horizontally, revert back to the original x position
            self.enemy_rect.x = original_x

        # Gravity application
        self.enemy_rect.y += self.vertical_speed
        if self.check_enemy_collision(tmx_data):
            self.vertical_speed = 0  # If there's a collision, stop vertical movement
        else:
            self.vertical_speed += self.gravity

        # Animate the enemy
        self.animate()

        # Check for collision with the player
        if self.check_collision_with_player(player):
            self.is_attacking = True
            if self.direction == 1:  # If enemy was previously facing right
                self.active_frames = self.attack_frames
            else:                    # If enemy was previously facing left
                self.active_frames = self.attack_left_frames
        elif not self.is_attacking: 
            # If the enemy was previously in an attack state but is no longer colliding with the player, 
            # it goes back to idle or walking based on its last direction
            if self.direction == 1:   # If enemy was previously moving right
                self.active_frames = self.idle_right_frames
            else:                     # If enemy was previously moving left
                self.active_frames = self.idle_left_frames

        # If the enemy has finished its attack animation, reset the is_attacking flag
        if self.is_attacking and self.current_frame == len(self.active_frames) - 1:
            self.is_attacking = False
                
    def draw(self, camera):
        self.screen.blit(self.image, self.enemy_rect)
        #pygame.draw.rect(self.screen, (0, 0, 255), self.enemy_rect, 2)
        self.box.draw(self.screen, camera)
        for effect in self.blood_effects:
            effect.draw(self.screen)
            effect.animate()

            # Optional: remove blood effect after it completes its animation
            if effect.current_image == len(effect.images) - 1:
                self.blood_effects.remove(effect)
        
class FlyingEnemy(Enemy):
    def __init__(self, screen, x, y, ui,bat_color="black", max_health=100):
        # Call the parent's initializer
        super().__init__(screen, x, y, ui, max_health)
        self.possible_speeds = [1,9, 2.2,2.3,2.4,2.7,3.3,3.4]        
        self.walk_right_frames = [self.scale_image(pygame.image.load(f'assets/bats/{bat_color}_bat/right_flying/fly{i}.png')) for i in range(1, 4)]
        self.walk_left_frames = [self.scale_image(pygame.image.load(f'assets/bats/{bat_color}_bat/left_flying/fly{i}.png')) for i in range(1, 4)]
    
        self.active_frames = self.walk_right_frames  # Default to right frames
        self.gravity = 0
        
    def enemy_movement(self, player_x, player_rect):
        # Keep horizontal movement as is from the parent class
        super().enemy_movement(player_x, player_rect)
        
        # Adjust vertical movement based on player's vertical position
        if self.enemy_rect.y < player_rect.y:
            self.enemy_rect.y += self.speed
        elif self.enemy_rect.y > player_rect.y:
            self.enemy_rect.y -= self.speed
            
    def chase(self, player, tmx_data):
        original_x = self.enemy_rect.x
        dx = player.player_rect.x - self.enemy_rect.x
        if dx > 0:  # Player is to the right
            self.enemy_rect.x += self.speed
            self.active_frames = self.walk_right_frames
            self.direction = 1
        elif dx < 0:  # Player is to the left
            self.enemy_rect.x -= self.speed
            self.active_frames = self.walk_left_frames
            self.direction = -1
        if self.check_enemy_collision(tmx_data):
            self.enemy_rect.x = original_x
        self.enemy_rect.y += self.vertical_speed
        if self.check_enemy_collision(tmx_data):
            self.vertical_speed = 0  
        else:
            self.vertical_speed += self.gravity
        # Animate the enemy
        self.animate()
        if self.direction == 1:   # If enemy was previously moving right
            self.active_frames = self.walk_left_frames
        else:                     # If enemy was previously moving left
            self.active_frames = self.walk_right_frames
        if self.is_attacking and self.current_frame == len(self.active_frames) - 1:
            self.is_attacking = False
            
    def check_enemy_collision(self, tmx_data):
        pass
            

class RoundSystem:
    def __init__(self):
        self.current_round = 0
        self.zombies_spawned = 0
        self.flying_enemies_spawned = 0
        self.enemies_killed = 0
        self.base_enemy_health = 100
        self.health_increment_per_round = 30   #HEALTH INCREASE PER ROUND !!!!!!!!!
        self.round_number = 1


    def start_new_round(self):
        self.current_round += 1
        self.enemies_left_to_spawn = self.current_round * 3  # Adjust the multiplication factor as per your game's design
        self.flying_enemies_left_to_spawn = self.current_round  # Or any other logic you want for the number of flying enemies
        self.spawn_new_enemies = True
        self.zombies_spawned = 0
        self.flying_enemies_spawned = 0
        self.base_enemy_health += self.health_increment_per_round
        self.round_number += 1


    def spawn_enemy(self):
        if self.enemies_left_to_spawn > 0:
            self.enemies_left_to_spawn -= 1
            if self.enemies_left_to_spawn == 0 and self.flying_enemies_left_to_spawn == 0:
                self.spawn_new_enemies = False
            return True
        return False

    def spawn_flying_enemy(self):
        if self.flying_enemies_left_to_spawn > 0:
            self.flying_enemies_left_to_spawn -= 1
            if self.enemies_left_to_spawn == 0 and self.flying_enemies_left_to_spawn == 0:
                self.spawn_new_enemies = False
            return True
        return False

    def can_spawn_enemy(self, current_enemy_count):
        # Only spawn if no enemies are currently alive
        if current_enemy_count == 0:
            return True
        return False

    def enemy_killed(self):
        self.enemies_killed += 1

    def is_round_over(self, current_enemy_count):
        total_zombies_for_round = 3 * self.current_round
        total_flying_enemies_for_round = self.current_round

        # Check if all enemies for the round have been spawned 
        all_enemies_spawned = (self.zombies_spawned == total_zombies_for_round) and (self.flying_enemies_spawned == total_flying_enemies_for_round)

        # Return true only if all enemies have been spawned and none are alive
        return all_enemies_spawned and current_enemy_count == 0
    
    def reset(self):
        self.current_round = 0
        self.zombies_spawned = 0
        self.flying_enemies_spawned = 0
        self.enemies_killed = 0
        self.base_enemy_health = 100
        self.round_number = 1
    
    
    
class BloodEffect:
    def __init__(self, enemy, x_offset, y_offset, images, width=None, height=None):
        self.enemy = enemy
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.width = 200
        self.height = 200
        self.images = [pygame.transform.scale(img, (self.width, self.height)) for img in images] if self.width and self.height else images
        self.current_image = 0
        self.last_updated = pygame.time.get_ticks()
        self.animation_speed = 20  
        
    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_updated > self.animation_speed:
            self.last_updated = now
            self.current_image = (self.current_image + 1) % len(self.images)
            
    def draw(self, screen):
        x = self.enemy.enemy_rect.x + self.x_offset
        y = self.enemy.enemy_rect.y + self.y_offset
        screen.blit(self.images[self.current_image], (x, y))