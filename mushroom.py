import asyncio
import pygame
import os
import time
import random
import math

from platforms import platforms


class Mushroom:
    """Грибочек 0 LVL"""
    def __init__(self, screen_height, screen_width):
        self.screen_height = screen_height
        self.screen_width = screen_width

        self.hit = pygame.image.load('media/image_main/грибочек-атата.png')
        self.hit = pygame.transform.scale(self.hit, (100, 70))  # Масштабируем изображение пули
        self.speed_move = 2 # Скорость передвижение
        self.move_part = False # Сторона движения

        # self.time_ghost_location = time.time()
        # self.last_move_time = time.time() # Время последнего движения
        # self.direction = None

        # self.ghost_speed = 4 # Скорость ghost
        # self.ghost_bullets = [] # Выстрелы злодея
        # self.timer_shot_ghost = 0.5

        # Начальная позиция персонажа
        self.mushroom_x = screen_width * 0.7 # Положение слева
        self.mushroom_y = screen_height * 0.57 # Вычисляем высоту пола

        mushroom = pygame.image.load("media/image_main/грибочек.png").convert_alpha()
        self.mushroom_image = pygame.transform.scale(mushroom, (40, 50)) # Задание нового размера персонажа (например, 100x100 пикселей)

    def screen_mushroom_0_lvl(self, current_location, screen):
        if self.mushroom_image and current_location == 0:
            screen.blit(self.mushroom_image, (self.mushroom_x, self.mushroom_y))

    def rect_mushroom(self):
        return pygame.Rect(self.mushroom_x, self.mushroom_y, self.mushroom_image.get_width(), self.mushroom_image.get_height())

    def move_mushroom(self, current_location):
        """Функция движений грибочка в зависимости от локации"""
        if not self.move_part:
            self.mushroom_x -= self.speed_move
        else:
            self.mushroom_x += self.speed_move

        rect_platforms = platforms(self.screen_width, self.screen_height)[current_location]
        rect_mushroom = self.rect_mushroom()
        for platform_rect in rect_platforms:
            if platform_rect.left == rect_mushroom.left:
                self.move_part = True

            elif platform_rect.right == rect_mushroom.right:
                self.move_part = False

    def hit_mushroom(self, current_location):
        pass

