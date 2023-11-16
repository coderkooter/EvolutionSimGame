import pygame
from player import Player
from plant import Plant
from constants import *
from hunter import Hunter
import random
from helper import *
import time
import pygame.font

pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Arial', 24)

# Create the original display surface
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create the scaled display surface
scaled_screen = pygame.Surface((SCREEN_WIDTH_SCALED, SCREEN_HEIGHT_SCALED))

player_obj = pygame.Rect((100, 100, PLAY_WIDTH, PLAY_HEIGHT))

player_class = Player(5, 60, player_obj, 60)

plant_list = []
for i in range(0,random.randint(5,PLANT_NR)):
    plant_list.append(Plant(random.randint(1,100)))

hunter_list = []
for i in range(0, random.randint(2,HUNTER_NR)):
    hunter_list.append(Hunter(random.randint(1,10), random.randint(1,100)))
run = True
last_target_time = time.time()
last_new_cycle_time = time.time()
seek_target = 0
while run:
    text_surface = font.render("food: " + str(int(player_class.get_food())), True, (0, 255, 0))
    screen.blit(text_surface, (100,100))
    pygame.display.update()

    current_time = time.time()
    if current_time - last_target_time >= TARGET_INTERVAL:
        for i in range(0,random.randint(0,20)):
            plant_list.append(Plant(random.randint(1,100)))
        for i in range(0, random.randint(0,5)):
            hunter_list.append(Hunter(random.randint(1,10), random.randint(1,100)))
        last_new_cycle_time = time.time()

    scaled_screen.fill((0, 0, 0))

    pygame.draw.rect(scaled_screen, player_class.get_color(), player_obj)

    for hunter in hunter_list:
        pygame.draw.rect(scaled_screen, (255, 0, 0), hunter.get_obj())
    for plant in plant_list:
        pygame.draw.rect(scaled_screen, (0, 255, 0), plant.get_obj())

    key = pygame.key.get_pressed()

    for hunterID in range(-1, len(hunter_list) - 1):
        if player_obj.colliderect(hunter_list[hunterID].get_obj()):

            winner = predator_fight(player_class.get_strength(), hunter_list[hunterID].get_strength())
            if winner == 0:
                player_class.add_food(hunter_list[hunterID].get_strength() * 1.5)
                hunter_list.pop(hunterID)
            if winner == 1:
                player_class._food = 0
    
    for plantID in range(0, len(plant_list) - 1):
        if player_obj.colliderect(plant_list[plantID].get_obj()):
            player_class.add_food(plant_list[plantID].get_points())
            plant_list.pop(plantID)

    key_pressed = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT:
                player_class.set_speed()

    if key[pygame.K_a]:
        key_pressed = "a"
    elif key[pygame.K_d]:
        key_pressed = "d"
    elif key[pygame.K_w]:
        key_pressed = "w"
    elif key[pygame.K_s]:
        key_pressed = "s"

    if key_pressed != 0:
        player_class.movement(key_pressed)

    current_time = time.time()
    for hunter in hunter_list:
        if current_time - last_target_time >= TARGET_INTERVAL or seek_target == 1:
            if not hunter.is_on_target():
                hunter.seek_target(player_obj, player_class)
            seek_target = 1
            last_target_time = current_time
        hunter.movement(player_obj)
    seek_target = 0

    # Scale the surface to the original dimensions and blit it onto the screen
    pygame.transform.scale(scaled_screen, (SCREEN_WIDTH, SCREEN_HEIGHT), screen)

    pygame.display.update()

pygame.quit()