
import pygame
import math

class Weapon:
    def __init__(self, reload_time, name, image_path, screen, camera, score, bullet_speed, damage, bullet_color, bullet_size, control_method, clip_size, stock_ammo, scale_size=(35, 35), fire_rate = 200):
        self.screen = screen
        self.image_path = image_path
        self.image_index = 0  # to keep track of which image/tier we are on
        self.original_image = pygame.image.load(self.image_path[self.image_index]).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, scale_size)
        self.initial_scale = self.original_image.get_size()
        self.image = self.original_image.copy()
        
        self.x_offset = -2  # We will center the offset on initialization
        self.y_offset = 4
        self.bobbing_magnitude = 3.5  # Controls the "height" of the bobbing, change as needed
        self.bobbing_speed = 0.2   # Controls the "speed" of the bobbing, change as needed
        self.time = 0

        self.bullets = []
        self.weapon_pos = (0, 0)
        self.camera = camera
        self.score = score
        
        #gun attributes in weapon list 
        self.bullet_speed = bullet_speed
        self.damage = damage
        self.control_method = control_method
        self.last_fired_time = 0 
        self.bullets_fired = 0
        self.burst_cooldown = 0
        self.fire_rate = fire_rate
        self.burst_delay = 50
        self.burst_shot_count = 0
        self.clip_size = clip_size
        self.clip_ammo = clip_size  # Assuming a full clip on weapon instantiation
        self.stock_ammo = stock_ammo
        self.name = name
        self.reload_time = reload_time  # New attribute
        self.reload_end_time = 0
        self.is_reloading = False
        self.tier = 0 
        self.factor = 0.97 # Example value, adjust as needed
        self.fire_rate *= self.factor
        self.recently_fired = False
        self.bullet_colors_list = bullet_color
        self.bullet_color = self.bullet_colors_list[self.image_index]
        self.current_bullet_color = self.bullet_colors_list[self.image_index]
        self.bullet_size = bullet_size
        self.shooting_bobbing_offset = 0
        self.shooting_bobbing_magnitude = 5  # Controls the "distance" of the horizontal bobbing
        self.shooting_bobbing_speed = 1.0   # Controls the "speed" of the horizontal bobbing
        self.shooting_bobbing_time = 0
        self.burst_interval = 500 

       
        self.original_stock_ammo = stock_ammo 
        
    def load_and_scale_image(self, path):
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, self.initial_scale)
            
    def apply_shooting_bobbing(self):
        self.shooting_bobbing_offset = math.sin(self.shooting_bobbing_time) * self.shooting_bobbing_magnitude
        self.shooting_bobbing_time += self.shooting_bobbing_speed
        if self.shooting_bobbing_time > 3 * math.pi:  # Once a full cycle is complete, reset the time and offset
            self.shooting_bobbing_time = 0
            self.shooting_bobbing_offset = 0
        
    def apply_powerup(self):
        self.factor = 0.76 # For instance, doubling the firing speed
        self.fire_rate *= self.factor

    def revert_powerup(self):
        self.factor = 2.0  # Revert the previous change
        self.fire_rate *= self.factor

  
            
    def upgrade(self):   # Upgrades the weapon attributes.
        clip_ratio = self.clip_ammo / self.clip_size

        # Increase the clip size by a factor of 1.2 and round it
        self.clip_size = round(self.clip_size * 1.4)

        # Set the new clip ammo using the ratio
        self.clip_ammo = int(self.clip_size * clip_ratio)

        # Repeat the process for the stock ammo
        stock_ratio = self.stock_ammo / self.original_stock_ammo
        self.original_stock_ammo = round(self.original_stock_ammo * 1.65)
        self.stock_ammo = int(self.original_stock_ammo * stock_ratio)

        # Your other upgrade logic (fire rate, etc.) 
        self.factor = 0.9  # or whatever value you deem appropriate
        self.fire_rate *= self.factor
        if self.image_index < len(self.image_path) - 1:
            self.image_index += 1
            self.original_image = self.load_and_scale_image(self.image_path[self.image_index])
            self.current_bullet_color = self.bullet_colors_list[self.image_index]
        
    def check_collision_with_enemy(self, enemy,player, has_blunderbullet):
        for bullet in self.bullets[:]:
            x, y = self.camera.camera_rect.topleft
            bullet_world_position = bullet.bullet.move((-x, -y))
            if bullet_world_position.colliderect(enemy.box.rect):
                enemy.health -= bullet.damage
                self.score.add_score(10)
                x_offset = (bullet.bullet.x - enemy.enemy_rect.x) - 120
                y_offset = (bullet.bullet.y - enemy.enemy_rect.y) -15
                if bullet.bullet.x > enemy.enemy_rect.centerx:
                    x_offset -= 2875 
                enemy.add_blood_effect(x_offset, y_offset)
                if has_blunderbullet and not hasattr(enemy, "blunder_affected"):
                    enemy.blunder_affected = True  # mark the enemy as affected
                    enemy.original_speed = enemy.speed
                    enemy.speed *= 0.90
                    pygame.time.set_timer(pygame.USEREVENT+1, 500, True)  # use a one-time event
                if enemy.health <= 0:
                    self.score.add_score(60)
                    player.kills += 1

                    return True
                self.bullets.remove(bullet)
        return False
    
    def aim(self, player_rect, camera_rect, mouse_position):
        player_center_x = player_rect.centerx + camera_rect.x

        # Flip the image upside down if the mouse is to the left of the player's center
        if mouse_position[0] < player_center_x:
            self.image = pygame.transform.flip(self.original_image, False, True)
            self.x_offset = -14
        else:
            self.image = self.original_image.copy()
            self.x_offset = -15

        # Calculate rotation angle
        dx = mouse_position[0] - (player_rect.right + camera_rect.x)
        dy = mouse_position[1] - (player_rect.top + camera_rect.y)
        angle = math.atan2(dy, dx) * 180 / math.pi

        self.image = pygame.transform.rotate(self.image, -angle)

        # Compute the bobbing offset using the sine wave for vertical movement
        bobbing_offset = math.sin(self.time) * self.bobbing_magnitude
        self.time += self.bobbing_speed

        # Update weapon position including the horizontal shooting bobbing
        weapon_pos = (
            player_rect.x + camera_rect.x + self.x_offset + self.shooting_bobbing_offset,
            player_rect.y + camera_rect.y + self.y_offset + bobbing_offset
        )
        self.weapon_pos = weapon_pos

        self.screen.blit(self.image, weapon_pos)
            
    def spawn_shotgun_bullets(self, mouse_position):
        number_of_pellets = 3  # The number of bullets/pellets in a shotgun blast
        spread_angle = 10  # Angle in degrees, determines how much the bullets will spread out

        dx = mouse_position[0] - self.weapon_pos[0]
        dy = mouse_position[1] - self.weapon_pos[1]

        base_angle = math.atan2(dy, dx)

        # Now, for each pellet, compute the angle based on the spread
        for i in range(number_of_pellets):
            # Offset by half the total spread so that the bullets spread around the mouse position
            angle_offset = (-spread_angle/2) + (i * spread_angle / (number_of_pellets - 1))
            angle = base_angle + math.radians(angle_offset)

            dx = math.cos(angle)
            dy = math.sin(angle)
            
            bullet_starting_x = self.weapon_pos[0] + 40
            bullet_starting_y = self.weapon_pos[1] - (-10)  # Offset adjusted
            
            bullet = Bullet(bullet_starting_x, bullet_starting_y, dx, dy, self.bullet_speed, self.damage, self.current_bullet_color, self.bullet_size)
            self.bullets.append(bullet)
        
    def fire(self, mouse_position):
        current_time = pygame.time.get_ticks()

        # Check if we are currently reloading:
        if current_time < self.reload_end_time:
            return

        if self.clip_ammo <= 0:  # Check if there's ammo in the clip before firing
            return

        if self.control_method == "burst":
            if self.burst_shot_count < 3 and current_time - self.last_fired_time >= self.burst_delay:
                # Fire a single bullet of the burst
                self.spawn_bullet(mouse_position)
                self.burst_shot_count += 1
                self.last_fired_time = current_time
                self.clip_ammo -= 1  # Decrease ammo count from the clip

            elif self.burst_shot_count == 3 and current_time - self.last_fired_time >= self.burst_interval:  
                # This is the delay between entire bursts.
                self.burst_shot_count = 0

        elif self.control_method == "single/auto":
            if current_time - self.last_fired_time >= self.fire_rate:
                self.spawn_bullet(mouse_position)
                self.last_fired_time = current_time
                self.clip_ammo -= 1  # Decrease ammo count from the clip

        elif self.control_method == "shotgun" and current_time - self.last_fired_time >= self.fire_rate:
            self.spawn_shotgun_bullets(mouse_position)
            self.last_fired_time = current_time
            self.clip_ammo -= 1  # Assuming 1 shotgun shell fires multiple pellets

        if self.clip_ammo <= 0:
            # You can add sound effects or any visual cues here for empty clip
            pass

        self.recently_fired = True


    def spawn_bullet(self, mouse_position):   #this was fire but now its spawn_bullet because we made fire into fire style kinda
        dx = mouse_position[0] - self.weapon_pos[0]
        dy = mouse_position[1] - self.weapon_pos[1]

        # Normalize dx and dy to get the direction
        length = math.sqrt(dx * dx + dy * dy)
        dx /= length
        dy /= length
        
        bullet_starting_x = self.weapon_pos[0] + 20 
        bullet_starting_y = self.weapon_pos[1] - (-10)  # Decrease the y value by 5 pixels
        bullet = Bullet(bullet_starting_x, bullet_starting_y, dx, dy, self.bullet_speed, self.damage, self.current_bullet_color, self.bullet_size)
        self.bullets.append(bullet)
        
    def complete_reload(self):
        bullets_needed = self.clip_size - self.clip_ammo
        if self.stock_ammo >= bullets_needed:
            self.stock_ammo -= bullets_needed
            self.clip_ammo = self.clip_size
        else:
            self.clip_ammo += self.stock_ammo
            self.stock_ammo = 0
                    
    def reload(self, has_speedcola=False):
        current_time = pygame.time.get_ticks()
        
        if current_time < self.reload_end_time:
            return
        
        # Apply Speed Cola effect if the player has it
        reload_duration = self.reload_time * 0.6 if has_speedcola else self.reload_time

        self.reload_end_time = current_time + reload_duration
        self.is_reloading = True

    def check_collision_with_box(self, box, camera):
        for bullet in self.bullets[:]:
            x, y = self.camera.camera_rect.topleft
            bullet_world_position = bullet.bullet.move((-x, -y))  # Convert bullet's screen position to game world position
            if bullet_world_position.colliderect(box.rect):
                self.bullets.remove(bullet) 

    def update_bullets(self, screen_width, screen_height):
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.off_screen(screen_width, screen_height):
                self.bullets.remove(bullet)
            else:
                pygame.draw.rect(self.screen,  bullet.color, bullet.bullet) 
        
    def update(self, player_center, mouse_pos):
        rel_x, rel_y = mouse_pos[0] - player_center[0], mouse_pos[1] - player_center[1]
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image = pygame.transform.rotate(self.original_image, angle - 90)  # Subtract 90 degrees to align properly

    

class Bullet:
    def __init__(self, x, y, dx, dy, speed, damage,color, size):
        self.bullet = pygame.Rect(x, y, *size)  # Assuming bullets are 5x5 in size, rename rect to bullet
        self.dx = dx
        self.dy = dy
        self.speed = speed
        self.damage = damage
        self.color = color 
        
    def update(self):
        self.bullet.x += self.dx * self.speed
        self.bullet.y += self.dy * self.speed
        
    def off_screen(self, screen_width, screen_height):
        return self.bullet.left > screen_width or self.bullet.right < 0 or self.bullet.top > screen_height or self.bullet.bottom < 0
    
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.bullet)