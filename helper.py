import random
from constants import *
from player import *
from plant import *
import time

def predator_fight(strength_one, strength_two):
    first = strength_one * (0.1 * random.randint(1,10))
    second = strength_two * (0.1 * random.randint(1,10))
    if first > second:
        return 0
    else:
        return 1

def display_text(text, position):
    text_surface = font.render(text, True, (255, 255, 255))
    screen.blit(text_surface, position)

def get_distance(obj_one, obj_two):
    return abs(obj_one.x - obj_two.x) + abs(obj_one.y - obj_two.y)

def calculate_reward(player, food_added):
    reward = 0

    if food_added > -0.5:
        reward += food_added * 3 # 1 - 100
    else:
        reward -= 10
 
    return reward
    