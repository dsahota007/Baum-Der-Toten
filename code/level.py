
import pygame
import pytmx
import pygame.surfarray as surfarray
import numpy as np

#zooming
scale_factor = 3

def draw_tiled_map(screen, tmx_data, camera):
    for layer in tmx_data.layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid, in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    # Scale the tile
                    tile = pygame.transform.scale(tile, (int(tmx_data.tilewidth * scale_factor), int(tmx_data.tileheight * scale_factor)))
                    screen.blit(tile, (x * tmx_data.tilewidth * scale_factor + camera.camera_rect.x, y * tmx_data.tileheight * scale_factor + camera.camera_rect.y))

def check_collision(player_rect, tmx_data):
    for layer in tmx_data.layers:
        if isinstance(layer, pytmx.TiledObjectGroup) and layer.name == "Object Layer 1":
            for obj in layer:
                # Scale the collision object
                scaled_rect = pygame.Rect(int(obj.x * scale_factor), int(obj.y * scale_factor), int(obj.width * scale_factor), int(obj.height * scale_factor))
                if player_rect.colliderect(scaled_rect):
                    return True
    return False

#pre suer i can delete this 
def adjust_brightness(img, factor):
    arr = surfarray.array3d(img)
    arr = np.clip(arr * factor, 0, 255)
    return surfarray.make_surface(arr)


#bullet collision with enemy and ground

class Box:
    def __init__(self, x, y, width, height, color=(255, 0, 0)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen, camera, visible=True):
        if not visible:
            # print("Box draw called but not visible.")    add this print statement
            return


