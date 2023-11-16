import pygame
from player import Player
from plant import Plant
from constants import *
from hunter import Hunter
import random
from helper import *
import time
import pygame.font
import gym
from gym import spaces
import numpy as np
import copy
import cv2

class Gym_Game(gym.Env):
    def __init__(self):
        super(Gym_Game, self).__init__() 

        # Set game text   
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 24)

        # Set screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # Scale settings
        # self.scaled_screen = pygame.Surface((SCREEN_WIDTH_SCALED, SCREEN_HEIGHT_SCALED))

        # RL model
        self.action_space = spaces.Discrete(4)  # Define the number of actions
        # self.observation_space = spaces.Box(low=0, high=255, shape=(6 + HUNTER_OBSERVATIONS + PLANT_OBSERVATIONS,), dtype=np.uint8)

        # observation_shapes = {
        #     'player': (2,),
        #     # 'plants': (3 * PLANT_NR,),
        #     'plants': (9,),
        #     # 'hunters': (2 * HUNTER_NR,),
        #     # 'hunters': (2,),
        # }

        # # Create the observation space as a Dict space
        # self.observation_space = spaces.Dict({
        #     key: spaces.Box(low=-1.0, high=1.0, shape=shape, dtype=float)
        #     for key, shape in observation_shapes.items()
        # })
        self.observation_space = spaces.Box(low=0, high=255, shape=(11,), dtype=np.uint8)


        # Create player
        self.player_class = Player(PLAYER_SPEED, 70, 60)

        # Create plants and hunters
        self.plant_list = []
        for i in range(0,random.randint(5,PLANT_NR)):
            self.plant_list.append(Plant(random.randint(20,200)))

        self.hunter_list = []
        for i in range(0, random.randint(2,HUNTER_NR)):
            self.hunter_list.append(Hunter(random.randint(1,1), random.randint(1,1)))

        self.steps_taken = 0
        self.last_target_time = time.time()
        self.last_new_cycle_time = time.time()
        self.plant_index = {}

    def step(self, action):
        # Check quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.player_class.kill()

        cur_food = self.player_class.get_food()

        # if not self.player_class.target:
        #     self.find_target()
        #     self.player_class.dis_to_goal = get_distance(self.player_class.get_obj(), self.player_class.target.get_obj())

        # print(self.player_class.dis_to_goal)
        # Move player
        key = "x"
        if action == 0:
            self.player_class.movement("a")
            key = "a"
        elif action == 1:
            self.player_class.movement("d")
            key = "d"
        elif action == 2:
            self.player_class.movement("w")
            key = "w"
        elif action == 3:
            self.player_class.movement("s")
            key = "s"
        elif action == 4:
            self.player_class.set_speed()

        # Perform game actions
        self.game_moves()

        food_added = self.player_class.get_food() - cur_food

        pygame.display.update()

        # Target was just hit.
        # if not self.player_class.target:
        #     reward = 1000
        #     self.find_target()
        #     self.player_class.dis_to_goal = get_distance(self.player_class.get_obj(), self.player_class.target.get_obj())
        # else:
        #     reward = calculate_reward(self.player_class, food_added, self.player_class.target.get_obj())
        # print(self.player_class.get_obj().x, self.player_class.get_obj().y)

        
        plant_positions = self.get_plant_positions()
        # hunter_positions = self.get_hunter_positions()

        # observation = {
        #     'player' : list(self.player_class.get_obj().topleft),
        #     'plants' : plant_positions
        #     # 'hunters' : hunter_positions
        # }

        observation = list(self.player_class.get_obj().topleft) + plant_positions

        reward = calculate_reward(self.player_class, food_added)

        done = self.player_class.is_dead()

        self.steps_taken += 1

        if self.steps_taken == 15000:
            done = True

        self.prev_distances = copy.copy(self.player_class.plant_distances)

        # print(observation)
        # print(reward)

        return observation, reward, done, {}

    def get_plant_positions(self):
        positions = []
        plant_item = []
        plant_food = {}

        for plant in self.plant_list:
            plant_item = plant.get_obj().topleft
            plant_food[plant_item] = plant.get_points()
            positions.append(plant_item)

        positions = self.order_coordinates(positions, self.player_class.get_obj().topleft)
        # positions = [coord for sublist in positions for coord in sublist]

        position_with_food = []

        for position in positions:
            position_with_food.append(plant_food[position] * 100)
            position_with_food.append(position[0])
            position_with_food.append(position[1])

        position_with_food = position_with_food

        # position_with_food = [coord for sublist in position_with_food for coord in sublist]

        while len(position_with_food) != PLANT_NR * 3:
            position_with_food = position_with_food + [0,0,0]

        # print(positions)

        return position_with_food[:9]


    def get_hunter_positions(self):
        positions = []
        hunter_item = []

        for hunter in self.hunter_list:
            hunter_item = list(hunter.get_obj().topleft)
            # hunter_item.append(hunter.get_strength())
            positions.append(hunter_item)

        positions = self.order_coordinates(positions, self.player_class.get_obj().topleft)
        positions = [coord for sublist in positions for coord in sublist]

        while len(positions) != HUNTER_NR * 2:
            positions = positions + [0,0]

        return positions[:2]

    def order_coordinates(self, coordinates, target_coordinate):
        target = np.array(target_coordinate)
        distances = [np.linalg.norm(np.array(coord) - target) for coord in coordinates]
        sorted_indices = np.argsort(distances)
        sorted_coordinates = [coordinates[i] for i in sorted_indices]
        return sorted_coordinates
    
    def find_target(self):
        closest_plant = "x"
        closest_distance = 10000

        for plant in self.plant_list:
            distance = get_distance(self.player_class.get_obj(), plant.get_obj())
            if distance < closest_distance:
                closest_plant = plant
                closest_distance = distance

        # print(closest_distance)
        self.player_class.target = closest_plant

    def check_collisions(self):
        # Collide with a hunter
        for hunter in self.hunter_list.copy():
            if self.player_class.get_obj().colliderect(hunter.get_obj()):
                winner = predator_fight(self.player_class.get_strength(), hunter.get_strength())
                if winner == 0:
                    self.player_class.add_food(hunter.get_strength() * 1.5)
                    self.hunter_list.remove(hunter)
                else:
                    self.player_class.kill()

        # Collide with a plant
        for plant in self.plant_list.copy():
            if self.player_class.get_obj().colliderect(plant.get_obj()):
                self.player_class.add_food(plant.get_points())
                self.plant_list.remove(plant)
                if plant in self.plant_index:
                    self.player_class.plant_distances[self.plant_index[plant]] = 0
                if plant == self.player_class.target:
                    self.player_class.target = False

    def respawn_cycle(self):
        current_time = time.time()
        if current_time - self.last_new_cycle_time >= TARGET_INTERVAL:
            for i in range(0,random.randint(5,20)):
                self.plant_list.append(Plant(random.randint(1,100)))
            for i in range(0, random.randint(2,5)):
                self.hunter_list.append(Hunter(random.randint(1,2), random.randint(1,2)))
            self.last_new_cycle_time = time.time()
        return

    def move_hunters(self):
        for hunter in self.hunter_list:
            if not hunter.is_on_target():
                hunter.seek_target(self.player_class.get_obj(), self.player_class)

    def get_dis_to_plants(self):
        for plant in self.plant_list:
            dis_to_plant = get_distance(self.player_class.get_obj(), plant.get_obj())
            if plant in self.plant_index:
                self.player_class.plant_distances[self.plant_index[plant]] = dis_to_plant
            else:
                for plantID in range(0,len(self.plant_list)):
                    if self.player_class.plant_distances[plantID] == 0:
                        self.player_class.plant_distances[plantID] = dis_to_plant
                        self.plant_index[plant] = plantID
                        break

    def game_moves(self):
        self.check_collisions()
        current_time = time.time()
        if current_time - self.last_target_time >= TARGET_INTERVAL:
            self.move_hunters()
            self.last_target_time = current_time
        for hunter in self.hunter_list:
            if hunter.is_on_target():
                hunter.movement(self.player_class.get_obj())
        self.respawn_cycle()
        self.get_dis_to_plants()

    def reset(self):
        # Reset timers
        self.last_target_time = time.time()
        self.last_new_cycle_time = time.time()

        # Reset plants and hunters
        self.plant_list = []
        for i in range(0,random.randint(5,PLANT_NR)):
            self.plant_list.append(Plant(random.randint(20,200)))

        self.hunter_list = []
        for i in range(0, random.randint(2,HUNTER_NR)):
            self.hunter_list.append(Hunter(random.randint(1,10), random.randint(1,100)))

        # Reset player
        self.player_class = Player(PLAYER_SPEED, 70, 60)

        self.player_class.plant_distances = [0] * 1000

        # plant_positions = [0, 0, 0] * PLANT_NR
        # hunter_positions = [0,0]  * HUNTER_NR
        plant_positions = [0, 0, 0] * 3
        hunter_positions = [0,0]  * 1

        # observation = {
        #     'player' : list(self.player_class.get_obj().topleft),
        #     'plants' : plant_positions
        #     # 'hunters' : hunter_positions
        # }

        observation = list(self.player_class.get_obj().topleft) + plant_positions

        self.plant_index = {}
        self.steps_taken = 0
        self.prev_distances = []

        # print("resetting")

        return observation

    def render(self, mode='human'):
        self.screen.fill((0, 0, 0))

        # Update player position
        player_position = self.player_class.get_position()
        self.player_class.get_obj().topleft = player_position

        # Render game objects
        pygame.draw.rect(self.screen, self.player_class.get_color(), self.player_class.get_obj())

        # Draw all plants and hunters
        for hunter in self.hunter_list:
            pygame.draw.rect(self.screen, (255, 0, 0), hunter.get_obj())
        for plant in self.plant_list:
            pygame.draw.rect(self.screen, (0, 255, 0), plant.get_obj())

        # Render additional elements (e.g., score, text)
        text_surface = self.font.render("food: " + str(int(self.player_class.get_food())), True, (0, 255, 0))
        self.screen.blit(text_surface, (100, 100))

        # Scale the surface to the original dimensions and blit it onto the screen
        pygame.transform.scale(self.screen, (SCREEN_WIDTH, SCREEN_HEIGHT), self.screen)

        # Update the display
        pygame.display.update()

    def close(self):
        pygame.quit()

gym.register(id='MyGameEnv-v0', entry_point='gym_game:Gym_Game')