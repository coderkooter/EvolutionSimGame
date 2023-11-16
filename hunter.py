from constants import *
import pygame
import random
import math

class Hunter:
    def __init__(self, strength, speed):
        self._strength = strength
        self._speed = speed
        self._food = FOOD_START
        self._object = pygame.Rect((random.randint(0, SCREEN_WIDTH_SCALED), random.randint(0, SCREEN_HEIGHT_SCALED), PLAY_WIDTH * (strength * 0.1), PLAY_HEIGHT * (strength * 0.1)))
        self._on_target = 0

    def get_strength(self):
        return self._strength

    def get_obj(self):
        return self._object

    def movement(self, player_obj):
        if self._on_target:
            if self._object.x < 0:
                self._object.x = 0
            elif self._object.x > SCREEN_WIDTH_SCALED:
                self._object.x = SCREEN_WIDTH_SCALED - PLAY_WIDTH
            if self._object.y < 0:
                self._object.y = 0
            elif self._object.y > SCREEN_WIDTH_SCALED:
                self._object.y = SCREEN_WIDTH_SCALED - PLAY_WIDTH

            if self._object.x == player_obj.x:
                movement_x = 0
            elif self._object.x - player_obj.x < 0:
                movement_x = self._speed
            else:
                movement_x = -self._speed
            if self._object.y == player_obj.y:
                movement_y = 0
            elif self._object.y - player_obj.y < 0:
                movement_y = self._speed
            else:
                movement_y = -self._speed
            self._object.x += movement_x
            self._object.y += movement_y

            self._food -= 1
    
    def is_on_target(self):
        if self._on_target == 1:
            return True
        else:
            return False

    def seek_target(self, player_obj, player_class):
        distance = (abs(player_obj.x - self._object.x)) + (abs(player_obj.y - self._object.y))

        distance_percent = 1 - distance / (SCREEN_HEIGHT_SCALED - PLAY_HEIGHT * 2 + SCREEN_WIDTH_SCALED - PLAY_WIDTH * 2)

        exponent = 10

        adjusted_chance = (distance_percent  ** exponent) * (1 - 0.01 * player_class.get_camouflage())

        if random.random() < adjusted_chance:
            self._on_target = 1

