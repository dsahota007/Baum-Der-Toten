import pygame

class Juggernog:
    def __init__(self, x, y, width, height, image_path):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.font_path = 'assets/interface/WesternBangBang-Regular.ttf'  
        self.font_size = 32

    def draw(self, screen, camera):
        screen.blit(self.image, (self.rect.x + camera.camera_rect.x, self.rect.y + camera.camera_rect.y))

    def display_prompt(self, screen, player_rect, camera, player_has_juggernog):  # Note the additional parameter
        if not player_has_juggernog:  # Only display the prompt if the player doesn't have Juggernog
            if player_rect.colliderect(self.rect):
                prompt_position = (self.rect.x + camera.camera_rect.x - 120, self.rect.y + camera.camera_rect.y - 30)  # Adjust position as needed
                self._display_interaction_prompt(screen, prompt_position)

    def _display_interaction_prompt(self, screen, position):
        font = pygame.font.Font(self.font_path, self.font_size) if self.font_path else pygame.font.SysFont(None, self.font_size)
        prompt_text = "Press E to buy Juggernog! ($2500)"  # You can change this to your preferred text
        text_surface = font.render(prompt_text, True, (239, 44, 44))
        screen.blit(text_surface, position)
        
class QuickRevive:
    def __init__(self, x, y, width, height, image_path):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.font_path = 'assets/interface/WesternBangBang-Regular.ttf' 
        self.font_size = 32

    def draw(self, screen, camera):
        screen.blit(self.image, (self.rect.x + camera.camera_rect.x, self.rect.y + camera.camera_rect.y))

    def display_prompt(self, screen, player_rect, camera, player_has_quickrevive):  # Note the additional parameter
        if not player_has_quickrevive:  # Only display the prompt if the player doesn't have Juggernog
            if player_rect.colliderect(self.rect):
                prompt_position = (self.rect.x + camera.camera_rect.x - 120, self.rect.y + camera.camera_rect.y - 30)  # Adjust position as needed
                self._display_interaction_prompt(screen, prompt_position)

    def _display_interaction_prompt(self, screen, position):
        font = pygame.font.Font(self.font_path, self.font_size) if self.font_path else pygame.font.SysFont(None, self.font_size)
        prompt_text = "Press E to buy Quick Revive! ($3000)"  # You can change this to your preferred text
        text_surface = font.render(prompt_text, True, (44, 213, 239))
        screen.blit(text_surface, position)
        
        
class StaminUp:
    def __init__(self, x, y, width, height, image_path):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.font_path = 'assets/interface/WesternBangBang-Regular.ttf' 
        self.font_size = 32

    def draw(self, screen, camera):
        screen.blit(self.image, (self.rect.x + camera.camera_rect.x, self.rect.y + camera.camera_rect.y))

    def display_prompt(self, screen, player_rect, camera, player_has_staminup):  # Note the additional parameter
        if not player_has_staminup:  # Only display the prompt if the player doesn't have Juggernog
            if player_rect.colliderect(self.rect):
                prompt_position = (self.rect.x + camera.camera_rect.x - 120, self.rect.y + camera.camera_rect.y - 30)  # Adjust position as needed
                self._display_interaction_prompt(screen, prompt_position)

    def _display_interaction_prompt(self, screen, position):
        font = pygame.font.Font(self.font_path, self.font_size) if self.font_path else pygame.font.SysFont(None, self.font_size)
        prompt_text = "Press E to buy Stamin Up! ($2000)"  # You can change this to your preferred text
        text_surface = font.render(prompt_text, True, (243, 184, 46))
        screen.blit(text_surface, position)
        
class SpeedCola:
    def __init__(self, x, y, width, height, image_path):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.font_path = 'assets/interface/WesternBangBang-Regular.ttf' 
        self.font_size = 32

    def draw(self, screen, camera):
        screen.blit(self.image, (self.rect.x + camera.camera_rect.x, self.rect.y + camera.camera_rect.y))

    def display_prompt(self, screen, player_rect, camera, player_has_speedcola):  # Note the additional parameter
        if not player_has_speedcola:  # Only display the prompt if the player doesn't have Juggernog
            if player_rect.colliderect(self.rect):
                prompt_position = (self.rect.x + camera.camera_rect.x - 120, self.rect.y + camera.camera_rect.y - 30)  # Adjust position as needed
                self._display_interaction_prompt(screen, prompt_position)

    def _display_interaction_prompt(self, screen, position):
        font = pygame.font.Font(self.font_path, self.font_size) if self.font_path else pygame.font.SysFont(None, self.font_size)
        prompt_text = "Press E to buy Speed Cola! ($3000)"  # You can change this to your preferred text
        text_surface = font.render(prompt_text, True, (25, 229, 10))
        screen.blit(text_surface, position)
        
class DoubleTap:
    def __init__(self, x, y, width, height, image_path):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.font_path = 'assets/interface/WesternBangBang-Regular.ttf' 
        self.font_size = 32

    def draw(self, screen, camera):
        screen.blit(self.image, (self.rect.x + camera.camera_rect.x, self.rect.y + camera.camera_rect.y))

    def display_prompt(self, screen, player_rect, camera, player_has_doubletap):  # Note the additional parameter
        if not player_has_doubletap:  # Only display the prompt if the player doesn't have Juggernog
            if player_rect.colliderect(self.rect):
                prompt_position = (self.rect.x + camera.camera_rect.x - 120, self.rect.y + camera.camera_rect.y - 30)  # Adjust position as needed
                self._display_interaction_prompt(screen, prompt_position)

    def _display_interaction_prompt(self, screen, position):
        font = pygame.font.Font(self.font_path, self.font_size) if self.font_path else pygame.font.SysFont(None, self.font_size)
        prompt_text = "Press E to buy Double Tap! ($4000)"  # You can change this to your preferred text
        text_surface = font.render(prompt_text, True, (222, 123, 36))
        screen.blit(text_surface, position)
        

class BlunderBullet:
    def __init__(self, x, y, width, height, image_path):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.font_path = 'assets/interface/WesternBangBang-Regular.ttf' 
        self.font_size = 32

    def draw(self, screen, camera):
        screen.blit(self.image, (self.rect.x + camera.camera_rect.x, self.rect.y + camera.camera_rect.y))

    def display_prompt(self, screen, player_rect, camera, player_has_blunderbullet):  # Note the additional parameter
        if not player_has_blunderbullet:  # Only display the prompt if the player doesn't have Juggernog
            if player_rect.colliderect(self.rect):
                prompt_position = (self.rect.x + camera.camera_rect.x - 120, self.rect.y + camera.camera_rect.y - 30)  # Adjust position as needed
                self._display_interaction_prompt(screen, prompt_position)

    def _display_interaction_prompt(self, screen, position):
        font = pygame.font.Font(self.font_path, self.font_size) if self.font_path else pygame.font.SysFont(None, self.font_size)
        prompt_text = "Press E to buy Blunder Bullet! ($4000)"  # You can change this to your preferred text
        text_surface = font.render(prompt_text, True, (232, 73, 200))
        screen.blit(text_surface, position)
        
        
        
class ElectricCherry:
    def __init__(self, x, y, width, height, image_path):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.font_path = 'assets/interface/WesternBangBang-Regular.ttf' 
        self.font_size = 32

    def draw(self, screen, camera):
        screen.blit(self.image, (self.rect.x + camera.camera_rect.x, self.rect.y + camera.camera_rect.y))

    def display_prompt(self, screen, player_rect, camera, player_has_electriccherry):  # Note the additional parameter
        if not player_has_electriccherry:  # Only display the prompt if the player doesn't have Juggernog
            if player_rect.colliderect(self.rect):
                prompt_position = (self.rect.x + camera.camera_rect.x - 170, self.rect.y + camera.camera_rect.y - 30)  # Adjust position as needed
                self._display_interaction_prompt(screen, prompt_position)

    def _display_interaction_prompt(self, screen, position):
        font = pygame.font.Font(self.font_path, self.font_size) if self.font_path else pygame.font.SysFont(None, self.font_size)
        prompt_text = "Press E to buy Electric Cherry! ($2000)"  # You can change this to your preferred text
        text_surface = font.render(prompt_text, True, (1, 255, 232))
        screen.blit(text_surface, position)

class SelfMedication:
    def __init__(self, x, y, width, height, image_path):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.font_path = 'assets/interface/WesternBangBang-Regular.ttf' 
        self.font_size = 32
        self.visible = True
        self.is_disappearing = False
        self.disappearing_speed = 5 
        self.angle = 0  # used for the sine/cosine calculations
        self.bobbing_amplitude = 15  # controls the "distance" of the bobbing
        self.bobbing_speed = 1000  # controls how "fast" the machine bobs
        self.original_x = x
        self.original_y = y

    def draw(self, screen, camera):
        if not self.visible:
            return
        screen.blit(self.image, (self.rect.x + camera.camera_rect.x, self.rect.y + camera.camera_rect.y))

    def display_prompt(self, screen, player_rect, camera, player_has_selfmed):  # Note the additional parameter
        if not self.visible:
            return
        if not player_has_selfmed:  # Only display the prompt if the player doesn't have Juggernog
            if player_rect.colliderect(self.rect):
                prompt_position = (self.rect.x + camera.camera_rect.x - 120, self.rect.y + camera.camera_rect.y - 30)  # Adjust position as needed
                self._display_interaction_prompt(screen, prompt_position)

    def _display_interaction_prompt(self, screen, position):
        font = pygame.font.Font(self.font_path, self.font_size) if self.font_path else pygame.font.SysFont(None, self.font_size)
        prompt_text = "Press E to buy Self Medication! ($1500)"  # You can change this to your preferred text
        text_surface = font.render(prompt_text, True, (243, 42, 82))
        screen.blit(text_surface, position)
        
    def hide(self):
        self.visible = False
        
    def reset(self):
        self.visible = True
        self.is_disappearing = False
        self.angle = 0
        self.rect.x = self.original_x
        self.rect.y = self.original_y

class FlashstepMastery:
    def __init__(self, x, y, width, height, image_path):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.font_path = 'assets/interface/WesternBangBang-Regular.ttf' 
        self.font_size = 32

    def draw(self, screen, camera):
        screen.blit(self.image, (self.rect.x + camera.camera_rect.x, self.rect.y + camera.camera_rect.y))

    def display_prompt(self, screen, player_rect, camera, player_has_flashstepmastery):  # Note the additional parameter
        if not player_has_flashstepmastery:  # Only display the prompt if the player doesn't have Juggernog
            if player_rect.colliderect(self.rect):
                prompt_position = (self.rect.x + camera.camera_rect.x - 150, self.rect.y + camera.camera_rect.y - 30)  # Adjust position as needed
                self._display_interaction_prompt(screen, prompt_position)

    def _display_interaction_prompt(self, screen, position):
        font = pygame.font.Font(self.font_path, self.font_size) if self.font_path else pygame.font.SysFont(None, self.font_size)
        prompt_text = "Press E to buy Flashstep Mastery! ($5000)"  # You can change this to your preferred text
        text_surface = font.render(prompt_text, True, (218, 130, 214))
        screen.blit(text_surface, position)
        
        
        
        
        
        
        
        
        
        