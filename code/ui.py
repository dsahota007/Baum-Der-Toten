
import pygame 
import random
import math
class UI:
    def __init__(self, screen):
        self.screen = screen
        self.health_bar = pygame.image.load('assets/interface/health_bar.png').convert_alpha()
        self.scaled_health_bar = pygame.transform.scale(self.health_bar, (400, 115))
        self.health_rect = pygame.Rect(80, 50, 295, 14)
        self.current_health = 100
        self.max_health = 100

        # Load the blood images
        self.blood_images = [
            pygame.image.load('assets/interface/blood6.png').convert_alpha(),
            pygame.image.load('assets/interface/blood5.png').convert_alpha(),
            pygame.image.load('assets/interface/blood4.png').convert_alpha(),
            pygame.image.load('assets/interface/blood3.png').convert_alpha(),
            pygame.image.load('assets/interface/blood2.png').convert_alpha(),
        ]
        self.scaled_blood_images = [pygame.transform.scale(img, (1400, 800)) for img in self.blood_images]

    def draw_health_bar(self):
        self.screen.blit(self.scaled_health_bar, (0, 0))
        current_width = int(self.health_rect.width * (self.current_health / self.max_health))
        current_health_rect = pygame.Rect(self.health_rect.left, self.health_rect.top, current_width, self.health_rect.height)
        pygame.draw.rect(self.screen, (155, 0, 0), current_health_rect)

    def draw_blood_effect(self):
        if self.current_health >= 150:  # No blood effect if health is 150 or above
            return

        if 0 < self.health_rect.width <= (30):  # Adjusted for 20% health
            self.screen.blit(self.scaled_blood_images[0], (0, 0))
        elif self.health_rect.width <= (60):  # Adjusted for 40% health
            self.screen.blit(self.scaled_blood_images[1], (0, 0))
        elif self.health_rect.width <= (90):  # Adjusted for 60% health
            self.screen.blit(self.scaled_blood_images[2], (0, 0))
        elif self.health_rect.width <= (120):  # Adjusted for 80% health
            self.screen.blit(self.scaled_blood_images[3], (0, 0))
    
    def update(self, last_player_hit_time, has_quickrevive):
        self.draw_blood_effect()
        self.draw_health_bar()

        current_time = pygame.time.get_ticks()
        time_since_last_hit = current_time - last_player_hit_time
        regen_interval = 2000 if has_quickrevive else 5000

        if time_since_last_hit >= regen_interval:
            self.health_regen()

    def health_regen(self):
        recovery_rate = 1
        self.health_rect.width += recovery_rate
        if self.health_rect.width > 295:
            self.health_rect.width = 295
class Score:
    def __init__(self, screen, x, y, font_path="assets/interface/WesternBangBang-Regular.ttf",font_size=70, initial_score=500):
        self.screen = screen
        self.score = initial_score
        self.font = pygame.font.Font(font_path, font_size)  # Use default font
        self.x = x
        self.y = y
        self.score_effects = []
        self.last_update_time = pygame.time.get_ticks()  # Record the current time
        self.score_increment_interval = 10000
        
    def add_periodic_score(self):
        current_time = pygame.time.get_ticks()
        # Check if 5 seconds have passed
        if current_time - self.last_update_time >= self.score_increment_interval:
            self.add_score(50)  # Add 250 points
            self.last_update_time = current_time 

    def add_score(self, points):
        self.score += points
        offset_x = 35
        offset_y = random.choice([-10, -6, -2, 4, 8, 12, 16, 22])
        effect = ScoreEffect(self.x + 60, self.y - offset_y, points)
        self.score_effects.append(ScoreEffect(self.x + offset_x, self.y + offset_y, points))

    def display(self):
        score_text = self.font.render(f"{self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (self.x, self.y))
        for effect in self.score_effects[:]:
            effect.update()
            if effect.alpha == 0:
                self.score_effects.remove(effect)
            else:
                effect.draw(self.screen)
                
    def reset(self):
        self.score = 500  # Resetting score to its initial value
        self.score_effects.clear() 

class ScoreEffect:
    def __init__(self, x, y, value, font_path="assets/interface/WesternBangBang-Regular.ttf", font_size=60):
        self.x = x
        self.y = y
        self.value = value
        self.font = pygame.font.Font(font_path, font_size)
        self.alpha = 255
        self.horizontal_speed = 3  # Adjust this value for faster/slower horizontal movement

    def update(self):
        # Reduce alpha for fade effect
        self.alpha -= 4
        if self.alpha < 0:
            self.alpha = 0

        # Move the effect horizontally
        self.x += self.horizontal_speed

    def draw(self, screen):
        if self.alpha > 0:
            rendered_text = self.font.render(f"+{self.value}", True, (255, 255, 255))
            text_surface = pygame.Surface(rendered_text.get_size(), pygame.SRCALPHA)
            text_surface.blit(rendered_text, (0, 0))
            text_surface.set_alpha(self.alpha)
            screen.blit(text_surface, (self.x, self.y))
        
class Crosshair:
    def __init__(self, screen, image_path):
        self.screen = screen
        self.image = pygame.image.load("assets/interface/crosshair.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(40,40))
        self.cross_rect = self.image.get_rect()
        pygame.mouse.set_visible(False)

    def update(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.cross_rect.center = (mouse_x, mouse_y)

    def draw(self):
        self.screen.blit(self.image, self.cross_rect.topleft)
        

class RoundCounter:
    def __init__(self, screen, x, y, font_path="assets/interface/unthink.otf", font_size=75):
        self.screen = screen
        self.font = pygame.font.Font(font_path, font_size)
        self.x = x
        self.y = y
        self.original_color = (155, 0, 0)
        self.blinking = False
        self.blink_time = 0  # Used to keep track of time since blinking started
        self.fading_speed = 0.005  # Adjust this for faster/slower fades

    def start_blinking(self):
        self.blinking = True
        self.blink_time = pygame.time.get_ticks()

    def display(self, round_number):
        if self.blinking:
            elapsed_time = (pygame.time.get_ticks() - self.blink_time) * self.fading_speed
            fade_value = (math.sin(elapsed_time) + 1) / 2  # This will produce values from 0 to 1

            r = int(self.original_color[0] * (1 - fade_value) + 255 * fade_value)
            g = int(self.original_color[1] * (1 - fade_value) + 255 * fade_value)
            b = int(self.original_color[2] * (1 - fade_value) + 255 * fade_value)

            color = (r, g, b)
            round_text = self.font.render(f"{round_number}", True, color)

            # Stop blinking after 3 seconds
            if pygame.time.get_ticks() - self.blink_time > 5900:
                self.blinking = False
        else:
            round_text = self.font.render(f"{round_number}", True, self.original_color)

        self.screen.blit(round_text, (self.x, self.y))
        

class WeaponInfoDisplay:
    def __init__(self, screen, name_x, name_y, ammo_x, ammo_y, font_path="assets/interface/WesternBangBang-Regular.ttf", font_size=28, font_color=(255, 255, 255)):
        self.screen = screen
        self.name_x = name_x
        self.name_y = name_y
        self.ammo_x = ammo_x
        self.ammo_y = ammo_y
        self.font_size = font_size
        self.font_color = font_color
        self.font = pygame.font.Font(font_path, font_size)
        
    def display_name(self, weapon_name, tier=0):  # added tier parameter with default value 0
        if isinstance(weapon_name, list):
            weapon_name = weapon_name[tier] if tier < len(weapon_name) else weapon_name[-1]  # Display name according to tier
        name_surface = self.font.render(weapon_name, True, self.font_color)
        self.screen.blit(name_surface, (self.name_x, self.name_y))

    def display_ammo(self, clip_ammo, stock_ammo):
        ammo_text = f"{clip_ammo}/{stock_ammo}"
        ammo_surface = self.font.render(ammo_text, True, self.font_color)
        self.screen.blit(ammo_surface, (self.ammo_x, self.ammo_y))
        
class ReloadingDisplay:
    def __init__(self, screen, font_path, position, color=(255, 255, 255)):
        self.screen = screen
        self.font = pygame.font.Font(font_path, 20)
        self.position = position
        self.color = color

    def display(self):
        reloading_surface = self.font.render("Reloading...", True, self.color)
        self.screen.blit(reloading_surface, self.position)
        
