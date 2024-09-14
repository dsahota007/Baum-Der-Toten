
import pygame

class Maxammo:
    def __init__(self, position):
        self.image = pygame.image.load('assets/drops/max_ammo_pic.png')  # Load the image
        self.rect = self.image.get_rect(center=position)  # Position where the enemy was defeated
        self.display_time = 1000  # Time in milliseconds for how long the image should be displayed
        self.creation_time = pygame.time.get_ticks()  # The time at which the image was created

    def update(self, current_time):
        # This method will be called every frame and will check if the image should still be displayed
        if current_time - self.creation_time > self.display_time:
            return False  # The image should no longer be displayed
        return True

    def draw(self, screen):
        # Draw the image to the screen
        screen.blit(self.image, self.rect)