from constants import *
import pygame

class Player:

    def __init__(self, max_speed, strength, camouflage):
        self._speed = max_speed / 2
        self._sprint = max_speed
        self._strength = strength
        self._food = FOOD_START
        self._sprinting = 0
        self._camouflage = camouflage
        self._keep_cam = camouflage
        self._is_dead = 0
        self._on_border = False
        self.plant_distances = [0] * 1000
        self._player_obj = pygame.Rect((PLAYER_START[0], PLAYER_START[1], PLAY_WIDTH, PLAY_HEIGHT))
        self.target = None
        self.dis_to_goal = 0
    
    def get_obj(self):
        return self._player_obj

    def get_position(self):
        return self._player_obj.topleft

    def get_food(self):
        return self._food

    def get_camouflage(self):
        return self._camouflage

    def get_speed(self):
        return self._speed

    def get_strength(self):
        return self._strength

    def set_speed(self):
        if self._sprinting == 1:
            self._speed = self._sprint / 2
            self._sprinting = 0
            self._camouflage = self._keep_cam
        else:
            self._speed = self._sprint
            self._sprinting = 1
            self._camouflage = self._camouflage * 0.5

    def kill(self):
        self._is_dead = 1

    def is_dead(self):
        if self._is_dead == 1:
            return True
        else:
            return False

    def get_color(self):
        white = (255, 255, 255)

        gray_level = 1 - self._camouflage * 0.01 
        if gray_level < 0.2:
            gray_level = 0.2

        gray = (
            int(white[0] * gray_level),
            int(white[1] * gray_level),
            int(white[2] * gray_level)
        )

        return gray

    def update_food(self):
        if self._sprinting == 1:
            self._food -= 1
        else:
            self._food -= 0.5
    
    def add_food(self, food):
        self._food += food

    def movement(self, key_pressed):
        if self._food > 0:
            if key_pressed == "a":
                self._player_obj.move_ip(-self._speed, 0)
                if self._player_obj.x < 0:
                    self._player_obj.x = 0
                    self._on_border = True
                else:
                    self._on_border = False
            elif key_pressed == "d":
                self._player_obj.move_ip(self._speed, 0)
                if self._player_obj.x > SCREEN_WIDTH_SCALED - PLAY_WIDTH:
                    self._player_obj.x = SCREEN_WIDTH_SCALED - PLAY_WIDTH
                    self._on_border = True
                else:
                    self._on_border = False
            elif key_pressed == "w":
                self._player_obj.move_ip(0, -self._speed)
                if self._player_obj.y < 0:
                    self._player_obj.y = 0
                    self._on_border = True
                else:
                    self._on_border = False
            elif key_pressed == "s":
                self._player_obj.move_ip(0, self._speed)
                if self._player_obj.y > SCREEN_HEIGHT_SCALED - PLAY_HEIGHT:
                    self._player_obj.y = SCREEN_HEIGHT_SCALED - PLAY_HEIGHT
                    self._on_border = True
                else:
                    self._on_border = False
        else:
            self.kill()
        
        self.update_food()


