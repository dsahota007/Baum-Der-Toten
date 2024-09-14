
import pygame
from pygame.locals import *
from level import check_collision
from weapon import Weapon
from machine import weapons_list

class Player:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.player_size = 130
        self.player_image = pygame.image.load('assets/player/right_side/idle1.png').convert_alpha()
        self.player_image = pygame.transform.scale(self.player_image, (self.player_size, self.player_size))
        self.hitbox_size = 25  # Let's say you want the hitbox to be 25x25              moree hitbox 
        self.player_rect = pygame.Rect(x, y, self.hitbox_size, self.hitbox_size)
        self.player_speed = 4.5
        self.original_player_speed = 4.5
        self.jump_speed = 10  # Speed at which the player jumps
        self.gravity = 0.3  # Gravity effect on the player
        self.vertical_speed = 0  # Vertical speed (used for jumping and gravity)
        self.is_jumping = False
        self.player_color = (232, 155, 54)
        self.player_rect = pygame.Rect(x, y, self.player_size, self.player_size)
        self.max_jumps = 2  # Maximum jumps the player can perform consecutively
        self.jump_count = 0  # Number of consecutive jumps performed
        self.jump_key_released = True
        #hitbox   --- ^ theres more 
        self.hitbox_width = 20  # Custom width for the hitbox
        self.upper_padding = 50  # Padding at the top of the hitbox
        self.lower_padding = 50  # Padding at the bottom of the hitbox
        self.hitbox_height = self.player_size - self.upper_padding - self.lower_padding  # Compute hitbox height
        self.player_rect = pygame.Rect(x, y + self.upper_padding, self.hitbox_width, self.hitbox_height)            
        #animations
        self.animation_speed = 100
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.idle_frames = [pygame.image.load(f'assets/player/right_side/idle{i}.png') for i in range(1, 4)]
        self.idle_left_frames = [pygame.image.load(f'assets/player/left_side/idle{i} _left.png') for i in range(1, 4)]
        self.run_right_frames = [pygame.image.load(f'assets/player/right_side/run{i}.png') for i in range(1, 10)]
        self.run_left_frames = [pygame.image.load(f'assets/player/left_side/run{i} _left.png') for i in range(1, 10)]
        self.jump_frames = [pygame.image.load(f'assets/player/right_side/jump{i}.png') for i in range(1, 10)]
        self.jump_left_frames = [pygame.image.load(f'assets/player/left_side/jump{i} _left.png') for i in range(1, 10)]
        self.active_frames = self.idle_frames
        self.facing_left = False  
        #perks
        self.has_juggernog = False
        self.has_quickrevive = False
        self.has_staminup = False
        self.has_speedcola = False
        self.has_doubletap = False
        self.has_blunderbullet = False
        self.has_electriccherry = False
        self.has_selfmed = False
        self.has_flashstepmastery = False
        self.active_perks = []
        #electric cherry animation
        self.electric_cherry_frames = [pygame.image.load(f'assets/animation/ec/{i}.png').convert_alpha() for i in range(1, 16)]  # Assuming you have 4 frames
        self.electric_cherry_anim_speed = 50
        self.electric_cherry_current_frame = 0
        self.electric_cherry_last_update = pygame.time.get_ticks()
        self.is_reloading = False
        self.selfmed_uses = 0
        #downed animation
        self.downed_frames = [pygame.image.load(f'assets/animation/health_regen/{i}.png').convert_alpha() for i in range(1, 29)]
        self.downed_anim_speed = 40  # adjust as needed
        self.downed_current_frame = 0
        self.downed_last_update = pygame.time.get_ticks()
        self.is_downed = False  
        self.has_finished_downed_animation = False
        #perk drinking animation
        self.drink_frames = [pygame.image.load(f'assets/animation/perk_effect/{i}.png').convert_alpha() for i in range(1, 28)]  # load your drinking animation images here
        self.drink_current_frame = 0
        self.drink_last_update = 0
        self.drink_anim_speed = 40  # adjust to your liking
        self.is_drinking = False
        self.has_finished_drinking_animation = False
        #PAP
        self.pack_a_punch_frames = [pygame.image.load(f'assets/animation/pack_a_punch/frame00{i}.png').convert_alpha() for i in range(1, 81)]  # Assuming you have 80 frames for this animation
        self.pack_a_punch_anim_speed = 12
        self.pack_a_punch_current_frame = 0
        self.pack_a_punch_last_update = pygame.time.get_ticks()
        self.is_pack_a_punching = False
        #dash function
        self.dash_speed = 15  # This can be twice the player_speed for a noticeable effect
        self.original_dash_speed = 15
        self.is_dashing = False
        self.dash_duration = 300  # milliseconds, i.e., dash lasts for 300ms
        self.dash_start_time = None  # to track when the dash started
        self.dash_cooldown = 3000  # milliseconds, i.e., 1 second cooldown after dashing
        self.original_dash_cooldown = 3000 
        self.last_dash_time = None
        #dash bar
        self.dash_bar_width = 20  # Adjust as needed
        self.dash_bar_height = 300  # Adjust as needed
        self.dash_bar_position = (1300, 320)  # Top-left position. Adjust as needed
        self.dash_bar_color = (0, 0, 205)  
        #self med live 
        self.fireball_animations = [pygame.image.load(f'assets/animation/selfmed_lives/{i}.png').convert_alpha() for i in range(1,60)]
        self.fireball_animations = [pygame.transform.scale(frame, (150, 150)) for frame in self.fireball_animations]
        self.fireball_current_frame = 0  # This is the corrected line
        self.fireball_last_update = pygame.time.get_ticks()
        self.fireball_anim_speed = 30
        
        self.is_dead = False
        self.kills = 0
        self.downs = 0
        
        
    def set_weapon(self, weapon):
        self.weapon = weapon
    
        
    def activate_flashstep(self):
        if self.has_flashstep:
            self.dash_speed = 27
            self.dash_cooldown = 1000

    def activate_staminup(self):
        if self.has_staminup:
            self.player_speed = 9.5
            
    def deactivate_flashstep(self):
        self.dash_speed = self.original_dash_speed
        self.dash_cooldown = self.original_dash_cooldown

    def deactivate_staminup(self):
        self.player_speed = self.original_player_speed
        
    #self med live  FUNCTION
    def draw_fireball_lives(self, screen):
        lives_left = 3 - self.selfmed_uses
        fireball_width = self.fireball_animations[0].get_width()

        spacing = -80 # Adjust this value to change spacing

        # Starting position for the leftmost fireball
        start_x_position = screen.get_width() - (lives_left * fireball_width + (lives_left - 1) * spacing)

        for i in range(lives_left):
            x_position = start_x_position + i * (fireball_width + spacing)
            y_position = -5  # 10 units from the top of the screen
            screen.blit(self.fireball_animations[self.fireball_current_frame], (x_position, y_position))
     #self med live  FUNCTION
    def update_fireball_animations(self):
        now = pygame.time.get_ticks()
        if now - self.fireball_last_update > self.fireball_anim_speed:
            self.fireball_last_update = now
            self.fireball_current_frame = (self.fireball_current_frame + 1) % len(self.fireball_animations)
            
    def draw_dash_recharge_bar(self, screen):
        elapsed_time_since_last_dash = pygame.time.get_ticks() - (self.last_dash_time if self.last_dash_time else 0)
        percentage_recharged = elapsed_time_since_last_dash / self.dash_cooldown
        percentage_recharged = min(1, percentage_recharged)  # Ensure it doesn't exceed 100%

        recharge_bar_height = int(self.dash_bar_height * percentage_recharged)
        start_y = self.dash_bar_position[1] + self.dash_bar_height - recharge_bar_height 
        pygame.draw.rect(screen, self.dash_bar_color, (self.dash_bar_position[0], start_y, self.dash_bar_width, recharge_bar_height))
        
    def update_reload_animation(self):
        if self.is_reloading:
            now = pygame.time.get_ticks()
            if now - self.electric_cherry_last_update > self.electric_cherry_anim_speed:
                self.electric_cherry_last_update = now
                self.electric_cherry_current_frame += 1
                if self.electric_cherry_current_frame >= len(self.electric_cherry_frames):
                    self.electric_cherry_current_frame = 0
                    self.is_reloading = False

    def start_reload_animation(self):
        self.is_reloading = True
        self.electric_cherry_current_frame = 0


    def get_position(self):
        return self.player_rect.x

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now  # Store the current time
            self.current_frame = (self.current_frame + 1) % len(self.active_frames)
            self.player_image = self.active_frames[self.current_frame]
            self.player_image = pygame.transform.scale(self.player_image, (self.player_size, self.player_size))
            
    def controls(self, tmx_data, weapon):
        keys = pygame.key.get_pressed()
        old_x, old_y = self.player_rect.x, self.player_rect.y

        # Dash functionality
        if keys[K_LSHIFT] and not self.is_dashing and (self.last_dash_time is None or pygame.time.get_ticks() - self.last_dash_time > self.dash_cooldown):
            self.is_dashing = True
            self.dash_start_time = pygame.time.get_ticks()
            self.dash_direction = -1 if self.facing_left else 1

        if self.is_dashing:
            self.player_rect.x += self.dash_speed * self.dash_direction
            if pygame.time.get_ticks() - self.dash_start_time > self.dash_duration:
                self.is_dashing = False
                self.last_dash_time = pygame.time.get_ticks()

        if keys[K_a] and not self.is_dashing:
            self.facing_left = True
            self.player_rect.x -= self.player_speed
            if not self.is_jumping:
                self.active_frames = self.run_left_frames
                self.animate()

        if keys[K_d] and not self.is_dashing:
            self.facing_left = False
            self.player_rect.x += self.player_speed
            if not self.is_jumping:
                self.active_frames = self.run_right_frames
                self.animate()

        if check_collision(self.player_rect, tmx_data):
            self.player_rect.x = old_x

        if keys[K_w] and self.jump_key_released and self.jump_count < self.max_jumps:
            self.is_jumping = True
            self.vertical_speed = -self.jump_speed
            self.jump_count += 1
            self.jump_key_released = False
            if self.facing_left:
                self.active_frames = self.jump_left_frames
            else:
                self.active_frames = self.jump_frames
            self.animate()

        if not keys[K_w]:
            self.jump_key_released = True

        self.player_rect.y += self.vertical_speed
        if check_collision(self.player_rect, tmx_data):
            if self.vertical_speed > 0:
                self.vertical_speed = 0
                self.is_jumping = False
                self.jump_count = 0
            self.player_rect.y = old_y

        self.vertical_speed += self.gravity             
        self.player_rect.y += self.vertical_speed

        if check_collision(self.player_rect, tmx_data):
            if self.vertical_speed > 0:
                self.vertical_speed = 0
                self.is_jumping = False
                self.jump_count = 0
            self.player_rect.y = old_y

        self.vertical_speed += self.gravity

        if self.is_jumping:
            if self.facing_left:
                self.active_frames = self.jump_left_frames
            else:
                self.active_frames = self.jump_frames
            self.animate()
        elif not (keys[K_a] or keys[K_d] or keys[K_w] or self.is_dashing):
            if self.facing_left:
                self.active_frames = self.idle_left_frames
            else:
                self.active_frames = self.idle_frames
            self.animate()
            
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 1 indicates left mouse button
                    mouse_position = pygame.mouse.get_pos()
                    weapon.fire(mouse_position)       
                    
        if keys[pygame.K_r]:  # Assuming R is the reload key
            weapon.reload(self.has_speedcola)
            self.start_reload_animation()
            
    
    def draw(self):
        player_surface = self.player_image.copy()
        
        # Handle electric cherry animation while reloading
        if self.is_reloading and self.has_electriccherry:
            frame = self.electric_cherry_frames[self.electric_cherry_current_frame]
            frame = pygame.transform.scale(frame, (100, 100))
            adjust_x = 55
            adjust_y = 45
            center_x = (self.player_rect.width // 2 - frame.get_width() // 2) + adjust_x
            center_y = (self.player_rect.height // 2 - frame.get_height() // 2) + adjust_y
            player_surface.blit(frame, (center_x, center_y))
            
        # Handle downed animation
        if self.is_downed and not self.has_finished_downed_animation:
            frame = self.downed_frames[self.downed_current_frame]
            frame = pygame.transform.scale(frame, (200, 200))
            adjust_x = 55
            adjust_y = 45
            center_x = (self.player_rect.width // 2 - frame.get_width() // 2) + adjust_x
            center_y = (self.player_rect.height // 2 - frame.get_height() // 2) + adjust_y
            player_surface.blit(frame, (center_x, center_y))
                
        if self.is_drinking and not self.has_finished_drinking_animation:
            frame = self.drink_frames[self.drink_current_frame]
            frame = pygame.transform.scale(frame, (200, 200))  # adjust size if needed
            adjust_x = 55
            adjust_y = 45
            center_x = (self.player_rect.width // 2 - frame.get_width() // 2) + adjust_x
            center_y = (self.player_rect.height // 2 - frame.get_height() // 2) + adjust_y
            player_surface.blit(frame, (center_x, center_y))
            
        if self.is_pack_a_punching:
            frame = self.pack_a_punch_frames[self.pack_a_punch_current_frame]
            frame = pygame.transform.scale(frame, (130, 130))  # Adjust size if needed
            adjust_x = 55
            adjust_y = 45
            center_x = (self.player_rect.width // 2 - frame.get_width() // 2) + adjust_x
            center_y = (self.player_rect.height // 2 - frame.get_height() // 2) + adjust_y
            player_surface.blit(frame, (center_x, center_y))

        # By this point, player_surface will have the relevant animations/frames applied to it.
        return player_surface
class Camera:
    def __init__(self, width, height):
        self.camera_rect = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def update(self, target, tmx_data, scale_factor):
        x = -target.player_rect.x + int(self.width / 2)
        y = -target.player_rect.y + int(self.height / 2)

        # Ensure the camera doesn't show beyond map boundaries.
        x = min(0, x)  # Left
        y = min(0, y)  # Top
        x = max(-(tmx_data.width * tmx_data.tilewidth * scale_factor - self.width), x)  # Right
        y = max(-(tmx_data.height * tmx_data.tileheight * scale_factor - self.height), y)  # Bottom

        self.camera_rect = pygame.Rect(x, y, self.width, self.height)  #x,y,l,w,
        
