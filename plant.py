import pygame
from constants import *
import random

class Plant:
    def __init__(self, points):
        self._points = points
        self._object = pygame.Rect((random.randint(0, SCREEN_WIDTH_SCALED), random.randint(0, SCREEN_HEIGHT_SCALED), PLAY_WIDTH * (points * 0.01), PLAY_HEIGHT * (points * 0.01)))

    def get_obj(self):
        return self._object

    def get_points(self):
        return self._points