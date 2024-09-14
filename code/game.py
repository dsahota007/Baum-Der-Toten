import pygame
from pytmx.util_pygame import load_pygame
from player import *
import pytmx
from level import draw_tiled_map, scale_factor, Box
import math
import os 
import random
from enemy import Enemy, RoundSystem, FlyingEnemy, all_blood_effects
from ui import UI, Score, Crosshair, WeaponInfoDisplay, RoundCounter ,ReloadingDisplay
from weapon import Weapon
from machine import MysteryBox, weapons_list, PackAPunch, UPGRADE_COSTS, AmmoBox
from perk import *

def main():
    pygame.init()

    SCREEN_WIDTH = 1400
    SCREEN_HEIGHT = 800
    FPS = 60

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Baum der Toten")
    
    #map loading
    tmx_data = load_pygame('assets/maps/platform2.tmx')
    background = pygame.image.load(os.path.join("assets", "maps", "bg.png")).convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    background_width = background.get_width()

    #background moving
    scroll = 0
    tiles = math.ceil(SCREEN_WIDTH / background_width) + 1
    
    #player spawn + camera
    zomb_spawn_x, zomb_spawn_y = 2900, 0
    flying_enemy_spawn_x, flying_enemy_spawn_y = 2900,0
    spawn_x, spawn_y = 2700, 1600
    
    player = Player(screen, spawn_x, spawn_y)
    camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
    
    #music
    # pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    # pygame.mixer.music.load('assets/music/menu.wav')
    # pygame.mixer.music.play(-1)
    
    
    #UI + enemies
    game_ui = UI(screen)
    enemies = []
    game_score = Score(screen, 45, 475)
    #dash ui
    dash_bar = pygame.image.load('assets/interface/dash_bar.png').convert_alpha()
    dash_bar = pygame.transform.scale(dash_bar, (130, 375))
    
    #gun GUI
    weapon_bar = pygame.image.load('assets/interface/gun_display.png').convert_alpha()
    weapon_bar = pygame.transform.scale(weapon_bar, (500, 105))
    
    
    # new_flying_enemy = FlyingEnemy(screen, flying_enemy_spawn_x, flying_enemy_spawn_y, game_ui)
    # enemies.append(new_flying_enemy)
    
    # Instantiate the mystery_box first
    mystery_box = MysteryBox(3695, 1330, 100, 80, "assets/machines/mystery_box_closed.png", "assets/machines/mystery_box_open.png", cost=950)
    #mystery_box = MysteryBox(2550, 1660, 100, 80, "assets/machines/mystery_box_closed.png", "assets/machines/mystery_box_open.png", cost=950)
    
    #pack a punch instantiate 
    pack_a_punch = PackAPunch(400, 400, 85, 70, "assets/machines/pack_a_punch.png") # Use actual path of your pack_a_punch image
    #pack_a_punch = PackAPunch(2370, 1660, 85, 70, "assets/machines/pack_a_punch.png") # Use actual path of your pack_a_punch image

    
    #ammmo box
    ammo_box_machine = AmmoBox(300, 1690, 70, 40, "assets/machines/ammo_box.png")
    
    juggernog_icon = pygame.image.load('assets/interface/perk_icons/juggernog_icon.png').convert_alpha()
    blunderbullet_icon = pygame.image.load('assets/interface/perk_icons/blunder_bullet_icon.png').convert_alpha()
    doubletap_icon = pygame.image.load('assets/interface/perk_icons/double_tap_icon.png').convert_alpha()
    electriccherry_icon = pygame.image.load('assets/interface/perk_icons/electric_cherry_icon.png').convert_alpha()
    quickrevive_icon = pygame.image.load('assets/interface/perk_icons/quick_revive_icon.png').convert_alpha()
    selfmed_icon = pygame.image.load('assets/interface/perk_icons/selfmed_icon.png').convert_alpha()
    speedcola_icon = pygame.image.load('assets/interface/perk_icons/speed_cola_icon.png').convert_alpha()
    stamin_up_icon = pygame.image.load('assets/interface/perk_icons/stamin_up_icon.png').convert_alpha()
    flashstep_mastery_icon = pygame.image.load('assets/interface/perk_icons/flashstep_mastery_icon.png').convert_alpha()
    
    perk_icon_size = (60,70)
    juggernog_icon = pygame.transform.scale(juggernog_icon, perk_icon_size)
    quickrevive_icon = pygame.transform.scale(quickrevive_icon, perk_icon_size)
    stamin_up_icon = pygame.transform.scale(stamin_up_icon, perk_icon_size)
    blunderbullet_icon = pygame.transform.scale(blunderbullet_icon, perk_icon_size)
    doubletap_icon = pygame.transform.scale(doubletap_icon, perk_icon_size)
    electriccherry_icon = pygame.transform.scale(electriccherry_icon, perk_icon_size)
    selfmed_icon = pygame.transform.scale(selfmed_icon, perk_icon_size)
    speedcola_icon = pygame.transform.scale(speedcola_icon, perk_icon_size)
    flashstep_mastery_icon = pygame.transform.scale(flashstep_mastery_icon, perk_icon_size)
            
    def draw_active_perk_icons(screen):
        x_position = 170  # Starting x position for the first icon
        y_position = 685  # Starting y position
        spacing = 65  # Spacing between icons

        # Create a copy of the list to iterate over. This avoids issues when modifying the list during iteration.
        active_perks_copy = player.active_perks[:]

        for perk in active_perks_copy:
            if perk == 'juggernog' and not player.has_juggernog:
                player.active_perks.remove(perk)
                continue
            elif perk == 'quickrevive' and not player.has_quickrevive:
                player.active_perks.remove(perk)
                continue
            elif perk == 'staminup' and not player.has_staminup:
                player.active_perks.remove(perk)
                continue
            elif perk == 'speedcola' and not player.has_speedcola:
                player.active_perks.remove(perk)
                continue
            elif perk == 'doubletap' and not player.has_doubletap:
                player.active_perks.remove(perk)
                continue
            elif perk == 'blunderbullet' and not player.has_blunderbullet:
                player.active_perks.remove(perk)
                continue
            elif perk == 'electriccherry' and not player.has_electriccherry:
                player.active_perks.remove(perk)
                continue
            elif perk == 'selfmed' and not player.has_selfmed:
                player.active_perks.remove(perk)
                continue
            elif perk == 'flashstep' and not player.has_flashstepmastery:
                player.active_perks.remove(perk)
                continue

            # Now for drawing the icons
            if perk == 'juggernog':
                screen.blit(juggernog_icon, (x_position, y_position))
            elif perk == 'quickrevive':
                screen.blit(quickrevive_icon, (x_position, y_position))
            elif perk == 'staminup':
                screen.blit(stamin_up_icon, (x_position, y_position))
            elif perk == 'speedcola':
                screen.blit(speedcola_icon, (x_position, y_position))
            elif perk == 'doubletap':
                screen.blit(doubletap_icon, (x_position, y_position))
            elif perk == 'blunderbullet':
                screen.blit(blunderbullet_icon, (x_position, y_position))
            elif perk == 'electriccherry':
                screen.blit(electriccherry_icon, (x_position, y_position))
            elif perk == 'selfmed':
                screen.blit(selfmed_icon, (x_position, y_position))
            elif perk == 'flashstep':
                screen.blit(flashstep_mastery_icon, (x_position, y_position))
            
            x_position += spacing

    #perk machines
    juggernog_machine = Juggernog(2960, 429, 35, 105, "assets/perks/juggernog.png")  # Modify the parameters accordingly
    quickrevive_machine = QuickRevive(3900, 796, 50, 75, "assets/perks/quick_revive.png")  
    staminup_machine = StaminUp(1745, 910, 60, 105, "assets/perks/stamin_up.png") 
    speedcola_machine = SpeedCola(3600, 1625, 60, 105, "assets/perks/speed_cola.png")  
    doubletap_machine = DoubleTap(2440, 1385, 60, 105, "assets/perks/double_tap.png")  
    blunderbullet_machine = BlunderBullet(365, 1300, 30, 95, "assets/perks/blunder_bullet.png")
    electriccherry_machine = ElectricCherry(1650, 1660, 50, 75, "assets/perks/electric_cherry.png")
    selfmed_machine = SelfMedication(2500, 810, 60, 105, "assets/perks/selfmed.png")
    flashstepmastery = FlashstepMastery(3305, 190, 60, 105, "assets/perks/flashstep_mastery.png")
    
    
    #starting weapon m1911 classic
    #weapon = Weapon("assets/weapons/m1911.png", screen, camera, game_score, 10, 20, "single")
    m1911_config = next((w for w in weapons_list if "M1911" in w["name"]), None)
    p90_config = next((w for w in weapons_list if "Colt 1911" in w["name"]), None)

    # List of weapons the player has
    player_weapons = [
        Weapon(
            name=m1911_config["name"],
            image_path=m1911_config["image_path"], 
            screen=screen, 
            camera=camera, 
            score=game_score, 
            bullet_speed=m1911_config["bullet_speed"], 
            damage=m1911_config["damage"], 
            control_method=m1911_config["control_method"],
            clip_size=m1911_config["clip_size"],
            stock_ammo=m1911_config["stock_ammo"],
            scale_size=m1911_config.get("scale_size", (35, 35)),
            fire_rate=m1911_config.get("fire_rate", 200),
            reload_time=m1911_config.get("reload_time", 1500),
            bullet_color=m1911_config["bullet_color"],
            bullet_size=m1911_config["bullet_size"],
        ),
        Weapon(
            name=p90_config["name"],
            image_path=p90_config["image_path"], 
            screen=screen, 
            camera=camera, 
            score=game_score, 
            bullet_speed=p90_config["bullet_speed"], 
            damage=p90_config["damage"], 
            control_method=p90_config["control_method"],
            clip_size=p90_config["clip_size"],
            stock_ammo=p90_config["stock_ammo"],
            scale_size=p90_config.get("scale_size", (35, 35)),
            fire_rate=p90_config.get("fire_rate", 200),
            reload_time=p90_config.get("reload_time", 1500),
            bullet_color=p90_config["bullet_color"],
            bullet_size=p90_config["bullet_size"],
        )
    ]

    # Index to keep track of which weapon is currently active
    current_weapon_index = 0
    active_weapon = player_weapons[current_weapon_index]
    # Now you can interact with the mystery_box
    new_weapon = mystery_box.interact(player.player_rect, weapons_list, screen, camera, game_score)
    player.set_weapon(active_weapon)

    #bullet collisions (x, y , width, height)
    boxes = [
        Box(0, 1735, 5400, 50),
        Box(2950, 1650, 400, 75),
        Box(0, 1400, 1230, 140),
        Box(1840,1250,350,170),
        Box(2385, 960, 495,130),
        Box(2565, 530, 495,100),
        Box(342,500,340,70),
        Box(3550,880, 380,70),
        Box(3430,430, 400,10)
    ]
    
    #spawn 
    last_player_hit_time = 0
    
    last_zombie_spawn_time = pygame.time.get_ticks()
    zombie_spawn_interval = 3000  # 3 seconds

    last_bat_spawn_time = pygame.time.get_ticks()
    bat_spawn_interval = 4000
    
    #round + round counter + crosshair + ui for gun reloading
    round_system = RoundSystem()  # Initialize the RoundSystem
    round_system.start_new_round()
    round_counter = RoundCounter(screen, 55, 570) 
    crosshair = Crosshair(screen, 'assets/interface/crosshair.png')
    weapon_info_display = WeaponInfoDisplay(screen, 875, 690, 1200, 690)
    reloading_display = ReloadingDisplay(screen, "assets/interface/WesternBangBang-Regular.ttf", (900, 640))
    
    
    clock = pygame.time.Clock()
    e_key_released = True 
    menu_title = pygame.image.load("assets/main_menu/main_title.png")
    menu_title_rect = menu_title.get_rect()
    
    font = pygame.font.Font("assets/interface/WesternBangBang-Regular.ttf", 36)
    play_text = font.render("Press [1] To Start The Game", True, (255, 255, 255))
    play_rect = play_text.get_rect(center=(400, 300))
    
    name_text = font.render("Created By Diljot Sahota", True, (255, 255, 255))
    name_rect = play_text.get_rect(center=(400, 300))
    
    menu_title_x = 370
    menu_title_y = 100
    play_text_x = 555
    play_text_y = 500
    name_text_x = 580
    name_text_y = 440

    state = "menu" 
    current_weapon_index = 0
    active_weapon = player_weapons[current_weapon_index]
    def reset_game(enemies, game_ui, mystery_box, round_system, player_weapons, camera, active_weapon, game_score):
        global state, current_weapon_index, scroll

        state = "menu"
        enemies.clear()
        game_ui.current_health = 100
        game_ui.points = 0  # Resetting the score as well
        
        game_ui.health_rect.width = 295    #THIS IS THE NEW LINE OF CODE I ADDED TO RESET HEALTH 

        # Directly reset attributes of round_system
        round_system.current_round = 0
        round_system.zombies_spawned = 0
        round_system.flying_enemies_spawned = 0
        round_system.enemies_killed = 0
        round_system.round_number = 1  # Important: reset the round number
        round_system.base_enemy_health += round_system.health_increment_per_round

        # Reset mystery box
        mystery_box.image = mystery_box.closed_image
        mystery_box.is_interacting = False
        mystery_box.opened_time = None
        mystery_box.selected_weapon_image = None
        mystery_box.bobbing_time = 0
        mystery_box.selected_weapon_config = None
        mystery_box.animation_image = None
        mystery_box.animation_frame_counter = 1
        player.set_weapon(active_weapon)
        player.kills = 0
        player.downs = 0
        player.selfmed_uses = 0  # Resetting the player's self med uses
        selfmed_machine.reset()
        game_score.reset() 
        m1911_config = next((w for w in weapons_list if "M1911" in w["name"]), None)
        p90_config = next((w for w in weapons_list if "Colt 1911" in w["name"]), None)

        player_weapons.clear()
        player_weapons.extend([
            Weapon(
                name=m1911_config["name"],
                image_path=m1911_config["image_path"], 
                screen=screen, 
                camera=camera, 
                score=game_score, 
                bullet_speed=m1911_config["bullet_speed"], 
                damage=m1911_config["damage"], 
                control_method=m1911_config["control_method"],
                clip_size=m1911_config["clip_size"],
                stock_ammo=m1911_config["stock_ammo"],
                scale_size=m1911_config.get("scale_size", (35, 35)),
                fire_rate=m1911_config.get("fire_rate", 200),
                reload_time=m1911_config.get("reload_time", 1500),
                bullet_color=m1911_config["bullet_color"],
                bullet_size=m1911_config["bullet_size"],
            ),
            Weapon(
                name=p90_config["name"],
                image_path=p90_config["image_path"], 
                screen=screen, 
                camera=camera, 
                score=game_score, 
                bullet_speed=p90_config["bullet_speed"], 
                damage=p90_config["damage"], 
                control_method=p90_config["control_method"],
                clip_size=p90_config["clip_size"],
                stock_ammo=p90_config["stock_ammo"],
                scale_size=p90_config.get("scale_size", (35, 35)),
                fire_rate=p90_config.get("fire_rate", 200),
                reload_time=p90_config.get("reload_time", 1500),
                bullet_color=p90_config["bullet_color"],
                bullet_size=p90_config["bullet_size"],
            )
        ])

        # Reset weapon index
        current_weapon_index = 0
        active_weapon = player_weapons[current_weapon_index]
        player.set_weapon(active_weapon) 

        # Reset the camera and scrolling background
        #camera.reset()
        scroll = 0
        round_system.reset()
        return Player(screen, spawn_x, spawn_y), active_weapon
    
    pause_text = font.render("Game Paused - Press [P] to Resume", True, (255, 255, 255))
    pause_rect = pause_text.get_rect(center=(400, 300))


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif state == "menu" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    state = "playing"
            elif state == "playing" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    state = "pause"
            elif state == "pause" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    state = "playing"
            elif state == "death" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    state = "menu"
                    player.is_dead = False
                    player, active_weapon = reset_game(
                        enemies, game_ui, mystery_box, round_system,
                        player_weapons, camera, active_weapon, game_score
                    )
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    current_weapon_index = (current_weapon_index - 1) % len(player_weapons)
                elif event.button == 5:
                    current_weapon_index = (current_weapon_index + 1) % len(player_weapons)
                active_weapon = player_weapons[current_weapon_index]
            elif event.type == pygame.USEREVENT + 1:
                for enemy in enemies:
                    if hasattr(enemy, "blunder_affected"):
                        delattr(enemy, "blunder_affected")
                        enemy.speed = enemy.original_speed

        # Check if left mouse button is being held down
        mouse_button_down = pygame.mouse.get_pressed()[0]
        if mouse_button_down and state == "playing":
            mouse_position = pygame.mouse.get_pos()
            active_weapon.fire(mouse_position)
            
        if player.is_dead:
            state = "death"

        if state == "menu":
            for i in range(0, tiles):
                screen.blit(background, (i * background_width + scroll, 0))
            scroll -= 0.43
            if abs(scroll) > background_width:
                scroll = 0

            menu_title_rect.topleft = (menu_title_x, menu_title_y)
            play_rect.topleft = (play_text_x, play_text_y)
            name_rect.topleft = (name_text_x, name_text_y)

            screen.blit(menu_title, menu_title_rect)
            screen.blit(play_text, play_rect)
            screen.blit(name_text, name_rect)
        
            pygame.display.flip()
            continue  # Skip the rest of the game loop

        elif state == "death":
            # screen.fill((0,0,0))
            for i in range(0, tiles):
                screen.blit(background, (i * background_width + scroll, 0))
            scroll -= 0.43
            if abs(scroll) > background_width:
                scroll = 0
            
            
            death_text = font.render("You have died.", True, (255, 40, 40))
            survived_text = font.render(f"You Survived {round_system.current_round} Rounds.", True, (255, 255, 255))
            
            # Display the number of kills and downs
            kills_text = font.render(f"Total Kills: {player.kills}", True, (255, 255, 255))
            downs_text = font.render(f"Resurections: {player.downs}", True, (255, 255, 255))
            
            instruction_text = font.render("Press [M] to return to the menu.", True, (255, 255, 255))
            
            # Positioning the texts
            screen.blit(death_text, (700 - death_text.get_width() // 2, 250))
            screen.blit(survived_text, (700 - survived_text.get_width() // 2, 290))
            screen.blit(kills_text, (700 - kills_text.get_width() // 2, 340))
            screen.blit(downs_text, (700 - downs_text.get_width() // 2, 370))
            screen.blit(instruction_text, (700 - instruction_text.get_width() // 2, 410))
            pygame.display.flip()
            continue
        
        elif state == "pause":
            pause_text = font.render("Game Paused. Press 'P' to resume", True, (255, 255, 255))
            pause_rect = pause_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            for i in range(0, tiles):
                screen.blit(background, (i * background_width + scroll, 0))
            scroll -= 0.43
            if abs(scroll) > background_width:
                scroll = 0
            screen.blit(pause_text, pause_rect)

            pygame.display.flip()
            continue 

            
        #moving background
        for i in range(0, tiles):
            screen.blit(background, (i * background_width + scroll, 0))
        scroll -= 0.43
        if abs(scroll) > background_width:
            scroll = 0
            


        #controls + camera
        player.controls(tmx_data, active_weapon)
        player.update_reload_animation()
        camera.update(player, tmx_data, scale_factor)
        
        draw_tiled_map(screen, tmx_data, camera)
        pack_a_punch.draw(screen, camera)
        mystery_box.draw(screen, camera, player.player_rect)
        pack_a_punch.display_prompt(screen, player.player_rect, camera, active_weapon)
        player_surface = player.draw()
        
        #PERKS machines
        juggernog_machine.draw(screen, camera)
        juggernog_machine.display_prompt(screen, player.player_rect, camera, player.has_juggernog)
        
        quickrevive_machine.draw(screen, camera)
        quickrevive_machine.display_prompt(screen, player.player_rect, camera, player.has_quickrevive)
        
        staminup_machine.draw(screen, camera)
        staminup_machine.display_prompt(screen, player.player_rect, camera, player.has_staminup)
        
        speedcola_machine.draw(screen, camera)
        speedcola_machine.display_prompt(screen, player.player_rect, camera, player.has_speedcola)
        
        doubletap_machine.draw(screen, camera)
        doubletap_machine.display_prompt(screen, player.player_rect, camera, player.has_doubletap)

        blunderbullet_machine.draw(screen, camera)
        blunderbullet_machine.display_prompt(screen, player.player_rect, camera, player.has_blunderbullet)
        
        electriccherry_machine.draw(screen, camera)
        electriccherry_machine.display_prompt(screen, player.player_rect, camera, player.has_electriccherry)
        
        flashstepmastery.draw(screen, camera)
        flashstepmastery.display_prompt(screen, player.player_rect, camera, player.has_flashstepmastery)
        
        selfmed_machine.draw(screen, camera)
        selfmed_machine.display_prompt(screen, player.player_rect, camera, player.has_selfmed)
    
        if selfmed_machine.visible:
            selfmed_machine.draw(screen, camera)
            selfmed_machine.display_prompt(screen, player.player_rect, camera, player.has_selfmed)    
            
        #ammo box
        ammo_box_machine.draw(screen, camera)
        ammo_box_machine.display_prompt(screen, player.player_rect, camera, active_weapon)
                        
                                    
        image_offset_x = (player.player_size - player.hitbox_width) // 2
        screen.blit(player_surface, (player.player_rect.x + camera.camera_rect.x - image_offset_x, player.player_rect.y + camera.camera_rect.y - player.upper_padding))

        # all the new variables for zombies
        for enemy in enemies:
            screen.blit(enemy.image, (enemy.enemy_rect.x + camera.camera_rect.x, enemy.enemy_rect.y + camera.camera_rect.y))
            enemy.chase(player, tmx_data)
            player_position = player.get_position()
            enemy.enemy_movement(player_position, player.player_rect)
            enemy.draw(camera)

            collision_detected = active_weapon.check_collision_with_enemy(enemy, player, player.has_blunderbullet)
            if collision_detected:
                enemies.remove(enemy)
                round_system.enemy_killed()

                
                if player.has_blunderbullet:
                    enemy.speed *= 0.90
                    enemy.blunder_affected = True
                    pygame.time.set_timer(pygame.USEREVENT+1, 500)
            
            if enemy.check_collision_with_player(player):
                last_player_hit_time = pygame.time.get_ticks()
                
        game_ui.update(last_player_hit_time, player.has_quickrevive)

        # Draw the weapon
        mouse_position = pygame.mouse.get_pos()
        active_weapon.aim(player.player_rect, camera.camera_rect, mouse_position)
        active_weapon.update_bullets(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        #bullet collision
        for box in boxes:
            active_weapon.check_collision_with_box(box, camera)

        for box in boxes:
            box.draw(screen, camera, visible=False)
            
        # Spawn logic
        current_time = pygame.time.get_ticks()
        current_enemy_count = len(enemies)

        # Spawn Zombies
        if current_time - last_zombie_spawn_time >= zombie_spawn_interval and round_system.zombies_spawned < (3 * round_system.current_round):
            new_enemy = Enemy(screen, zomb_spawn_x, zomb_spawn_y, game_ui, max_health=round_system.base_enemy_health)
            enemies.append(new_enemy)
            round_system.zombies_spawned += 1
            last_zombie_spawn_time = current_time

        # Spawn Bats
        if current_time - last_bat_spawn_time >= bat_spawn_interval and round_system.flying_enemies_spawned < round_system.current_round:
            chosen_bat_color = random.choice(["black", "green", "red","blue"])
            new_flying_enemy = FlyingEnemy(screen, flying_enemy_spawn_x, flying_enemy_spawn_y, game_ui, bat_color=chosen_bat_color)
            enemies.append(new_flying_enemy)
            round_system.flying_enemies_spawned += 1
            last_bat_spawn_time = current_time

        # Check if the round is over
        if round_system.is_round_over(len(enemies)):
            round_counter.start_blinking()
            round_system.start_new_round()

        round_counter.display(round_system.current_round)
                
        #mystery box interaction open close and grab weapon
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e] and mystery_box.is_player_nearby(player.player_rect) and not mystery_box.is_interacting:
            if game_score.score >= 950:  # Check if the player has enough score
                mystery_box.set_open(game_score)  # Deduct 950 points and open the box
                mystery_box.select_weapon()  
                mystery_box.draw(screen, camera, player.player_rect)

        elif keys[pygame.K_q] and mystery_box.is_player_nearby(player.player_rect) and mystery_box.is_interacting and mystery_box.selected_weapon_config: # Add condition to ensure box is interacting
            new_weapon = mystery_box.provide_weapon(player.player_rect, weapons_list, screen, camera, game_score)
            if new_weapon:
                active_weapon = new_weapon
                player_weapons[current_weapon_index] = new_weapon
            mystery_box.set_closed()
            mystery_box.draw(screen, camera, player.player_rect)
            mystery_box.is_interacting = False

        elif keys[pygame.K_n]:
            mystery_box.set_closed()
            mystery_box.reset_weapon()  # Reset the weapon choice when closing the box without picking up
            mystery_box.draw(screen, camera, player.player_rect)
            mystery_box.is_interacting = False
                    
        if mystery_box.opened_time and current_time - mystery_box.opened_time >= 25000 and not keys[pygame.K_y]:   # this is the time of when it is staying open 
            mystery_box.set_closed()
            mystery_box.reset_weapon()  # Reset the weapon choice after set time
            mystery_box.opened_time = None
            
            
        #point system + crosshair
        game_score.display()
        crosshair.update()
        crosshair.draw()

        #ui for wepaon
        weapon_info_display.display_name(active_weapon.name, active_weapon.tier)
        weapon_info_display.display_ammo(active_weapon.clip_ammo, active_weapon.stock_ammo)
        
        #reload wepaon
        if active_weapon.reload_end_time and pygame.time.get_ticks() >= active_weapon.reload_end_time:
            active_weapon.reload_end_time = 0  # Reset it so that it doesn't trigger again
            active_weapon.is_reloading = False
            active_weapon.complete_reload() 
            
        if active_weapon.is_reloading:
            reloading_display.display()
                    
                    
        #pack a punch
        if pygame.key.get_pressed()[pygame.K_e] and e_key_released:
            if player.player_rect.colliderect(pack_a_punch.rect):  # Check if the player is near the Pack-a-Punch machine
                if active_weapon.tier < 5:  # Check if the gun isn't already at max tier
                    cost_to_upgrade = UPGRADE_COSTS[active_weapon.tier]  # Get cost based on current tier

                    if game_score.score >= cost_to_upgrade:  # Ensure player has enough score for the upgrade
                        game_score.score -= cost_to_upgrade  # Deduct the cost from player's score
                        active_weapon.damage *= 2  # Double the damage of the active weapon
                        active_weapon.tier += 1  # Increase the weapon's tier
                        player.is_pack_a_punching = True  # Trigger the Pack-a-Punch animation
                        player.pack_a_punch_current_frame = 0

                        # Call the upgrade method to double the clip_size and stock_ammo
                        active_weapon.upgrade()
            
            e_key_released = False  # Ensure 'E' key input is registered only once
        elif not pygame.key.get_pressed()[pygame.K_e]:
            e_key_released = True
            
        #PaP animaiton 
        if player.is_pack_a_punching:
            now = pygame.time.get_ticks()
            if now - player.pack_a_punch_last_update > player.pack_a_punch_anim_speed:
                player.pack_a_punch_last_update = now
                player.pack_a_punch_current_frame += 1
                if player.pack_a_punch_current_frame >= len(player.pack_a_punch_frames):
                    player.pack_a_punch_current_frame = 0
                    player.is_pack_a_punching = False
                    
            
        #perks
        #juggernog 
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e] and juggernog_machine.rect.colliderect(player.player_rect):
            if not player.has_juggernog:  # Check if the player doesn't have Juggernog
                if game_score.score >= 2500:
                    player.has_juggernog = True  # Player now has Juggernog
                    game_score.score -= 2500 
                    player.active_perks.append('juggernog')
                    player.is_drinking = True
                    player.drink_current_frame = 0
                    player.has_finished_drinking_animation = False
        #quick revive            
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e] and quickrevive_machine.rect.colliderect(player.player_rect):
            if not player.has_quickrevive:  
                if game_score.score >= 3000:
                    player.has_quickrevive = True  
                    game_score.score -= 3000 
                    player.active_perks.append('quickrevive')
                    player.is_drinking = True
                    player.drink_current_frame = 0
                    player.has_finished_drinking_animation = False
        #staminup
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e] and staminup_machine.rect.colliderect(player.player_rect):
            if not player.has_staminup:  
                if game_score.score >= 2000:
                    player.has_staminup = True  
                    player.player_speed = 6.9  
                    game_score.score -= 2000
                    player.active_perks.append('staminup')
                    player.is_drinking = True
                    player.drink_current_frame = 0
                    player.has_finished_drinking_animation = False
                            
        #speed cola           
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e] and speedcola_machine.rect.colliderect(player.player_rect):
            if not player.has_speedcola: 
                if game_score.score >= 3000:
                    player.has_speedcola = True  
                    game_score.score -= 3000 
                    player.active_perks.append('speedcola')
                    player.is_drinking = True
                    player.drink_current_frame = 0
                    player.has_finished_drinking_animation = False
                    
        #double tap           
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e] and doubletap_machine.rect.colliderect(player.player_rect):
            if not player.has_doubletap:  
                if game_score.score >= 4000:
                    player.has_doubletap = True  
                    game_score.score -= 4000 
                    player.active_perks.append('doubletap')
                    player.is_drinking = True
                    player.drink_current_frame = 0
                    player.has_finished_drinking_animation = False
                    for weapon in player_weapons:
                        if weapon.recently_fired:
                            weapon.apply_powerup()  # apply the powerup to the weapon that was recently fired
                            break
        #blunderbullet
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e] and blunderbullet_machine.rect.colliderect(player.player_rect):
            if not player.has_blunderbullet: 
                if game_score.score >= 4000:
                    player.has_blunderbullet = True  
                    game_score.score -= 4000 
                    player.active_perks.append('blunderbullet')
                    player.is_drinking = True
                    player.drink_current_frame = 0
                    player.has_finished_drinking_animation = False
        #electric cherrye
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e] and electriccherry_machine.rect.colliderect(player.player_rect):
            if not player.has_electriccherry: 
                if game_score.score >= 2000:
                    player.has_electriccherry = True  
                    game_score.score -= 2000 
                    player.active_perks.append('electriccherry')
                    player.is_drinking = True
                    player.drink_current_frame = 0
                    player.has_finished_drinking_animation = False
                    
        #flashstepmastery
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e] and flashstepmastery.rect.colliderect(player.player_rect):
            if not player.has_flashstepmastery:  
                if game_score.score >= 5000:
                    player.has_flashstepmastery = True  
                    player.dash_speed = 27
                    player.dash_cooldown = 1000 
                    game_score.score -= 5000
                    player.active_perks.append('flashstep')
                    player.is_drinking = True
                    player.drink_current_frame = 0
                    player.has_finished_drinking_animation = False
                    
        #self medication
        if keys[pygame.K_e] and selfmed_machine.rect.colliderect(player.player_rect):
            if not player.has_selfmed and player.selfmed_uses < 3: 
                if game_score.score >= 1500:
                    player.has_selfmed = True  
                    game_score.score -= 1500
                    player.active_perks.append('selfmed')
                    player.is_drinking = True
                    player.drink_current_frame = 0
                    player.has_finished_drinking_animation = False

                    # Reset the downed animation variables
                    player.is_downed = False
                    player.downed_current_frame = 0
                    player.has_finished_downed_animation = False

            elif player.selfmed_uses >= 3 and not selfmed_machine.is_disappearing:
                selfmed_machine.is_disappearing = True

        # SelfMed Machine Disappearing Logic
        if selfmed_machine.is_disappearing:
            selfmed_machine.rect.y -= selfmed_machine.disappearing_speed + selfmed_machine.bobbing_amplitude * math.sin(selfmed_machine.angle)
            selfmed_machine.rect.x = selfmed_machine.original_x + selfmed_machine.bobbing_amplitude * math.cos(selfmed_machine.angle)
            selfmed_machine.angle += selfmed_machine.bobbing_speed
            if selfmed_machine.rect.y <= 0:
                selfmed_machine.visible = False
                selfmed_machine.is_disappearing = False 

        # Animating the Player's Downed State
        current_time = pygame.time.get_ticks()
        if player.is_downed:
            if player.downed_current_frame < len(player.downed_frames) - 1:
                if current_time - player.downed_last_update > player.downed_anim_speed:
                    player.downed_current_frame += 1
                    player.downed_last_update = current_time
            else:
                player.has_finished_downed_animation = True

        # Resetting the Downed Animation
        if player.has_selfmed:
            player.is_downed = False
            player.downed_current_frame = 0
            
        if player.is_drinking:
            if player.drink_current_frame < len(player.drink_frames) - 1:
                if current_time - player.drink_last_update > player.drink_anim_speed:
                    player.drink_current_frame += 1
                    player.drink_last_update = current_time
            else:
                player.has_finished_drinking_animation = True
                player.is_drinking = False

        draw_active_perk_icons(screen)
        
        #ammo Box           
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e] and not e_key_pressed:
            e_key_pressed = True
            if ammo_box_machine.rect.colliderect(player.player_rect):
                ammo_box_machine.refill_ammo(active_weapon, game_score)
        elif not keys[pygame.K_e]:
            e_key_pressed = False
        if player.is_downed:
            player.deactivate_flashstep()
            player.deactivate_staminup()

        #dash ui
        screen.blit(dash_bar, (1245, 283))
        screen.blit(weapon_bar, (860, 683))
        #the blue rect bar for energy 
        player.draw_dash_recharge_bar(screen)
        
        player.update_fireball_animations()
        player.draw_fireball_lives(screen)
        
        #blood effect post death (they kept disspearing)
        for effect in all_blood_effects:
            effect.draw(screen)
            effect.animate()
            
            # Optional: remove blood effect after it completes its animation
            if effect.current_image == len(effect.images) - 1:
                all_blood_effects.remove(effect)
        
        #print("Player's x:", player.player_rect.x)
        #print("Player's y:", player.player_rect.y)
        
        game_score.add_periodic_score() 

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
    
    
