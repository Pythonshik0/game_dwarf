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

        self.speed_move = 2 # Скорость передвижение
        self.move_part = False # Сторона движения
        self.attack = False # Атака

        self.images = {
            'worth': [
                pygame.image.load("media/image_main/грибочек-1.1.png").convert_alpha(),
                pygame.image.load("media/image_main/грибочек-1.2.png").convert_alpha(),
                pygame.image.load("media/image_main/грибочек.png").convert_alpha(),
            ],
            'hit': [
                pygame.image.load('media/image_main/грибочек-атата.png').convert_alpha(),
            ]
        }
        self.last_update = pygame.time.get_ticks()
        self.current_frame = 0
        # self.time_ghost_location = time.time()
        # self.last_move_time = time.time() # Время последнего движения
        # self.direction = None

        # self.ghost_speed = 4 # Скорость ghost
        # self.ghost_bullets = [] # Выстрелы злодея
        # self.timer_shot_ghost = 0.5

        # Начальная позиция персонажа
        self.mushroom_x = screen_width * 0.7 # Положение слева
        self.mushroom_y = screen_height * 0.58 # Вычисляем высоту пола

        # Размер перса
        self.mushroom_height = screen_height * 0.05
        self.mushroom_width = screen_width * 0.03

        # self.mushroom = self.images['worth'][0]
        # self.mushroom_image = pygame.transform.scale(self.mushroom, (self.mushroom_width, self.mushroom_height)) # Задание нового размера персонажа (например, 100x100 пикселей)

        self.mushroom_images = [pygame.transform.scale(img, (self.mushroom_width, self.mushroom_height)) for img in self.images['worth']]
        # self.hit_image = pygame.transform.scale(self.images['hit'][0], (self.screen_width * 0.07, self.screen_height * 0.06))
        self.hit_image = [pygame.transform.scale(img, (self.screen_width * 0.08, self.screen_height * 0.06)) for img in self.images['hit']]

    def screen_mushroom_0_lvl(self, current_location, screen):
        if current_location == 0:
            if not self.attack:
                screen.blit(self.mushroom_images[self.current_frame], (self.mushroom_x, self.mushroom_y))
            else:
                screen.blit(self.hit_image[0], (self.mushroom_x, self.mushroom_y))

    def rect_mushroom(self):
        """Возвращает прямоугольник гриба для коллизий."""
        if not self.attack:
            return pygame.Rect(self.mushroom_x, self.mushroom_y,
                               self.mushroom_images[self.current_frame].get_width(),
                               self.mushroom_images[self.current_frame].get_height())
        else:
            return pygame.Rect(self.mushroom_x, self.mushroom_y,
                               self.hit_image[0].get_width(),
                               self.hit_image[0].get_height())

    def gif_dwarf(self, now):
        """Создание движения картинки."""
        frame_delay = 500
        if now - self.last_update > frame_delay:
            self.current_frame = (self.current_frame + 1) % len(self.mushroom_images)  # Переход к следующему кадру
            self.last_update = now  # Обновляем время последнего обновления

    def move_mushroom(self, current_location):
        """Функция движений грибочка в зависимости от локации"""
        if self.attack is False:
            self.mushroom_image = [pygame.transform.scale(img, (self.mushroom_width, self.mushroom_height)) for img in self.images['worth']]

        # if not self.move_part:
        #     self.mushroom_x -= self.speed_move
        # else:
        #     self.mushroom_x += self.speed_move
        #
        # rect_platforms = platforms(self.screen_width, self.screen_height)[current_location]
        # rect_mushroom = self.rect_mushroom()
        # for platform_rect in rect_platforms:
        #     if platform_rect.left == rect_mushroom.left:
        #         self.move_part = True
        #
        #     elif platform_rect.right == rect_mushroom.right:
        #         self.move_part = False

    def hit_mushroom(self, current_location, dwarf_rect):
        rect_mushroom = self.rect_mushroom()
        if current_location == 0:  # Для 0 уровня
            # Проверка попадания в радиус атаки
            conflict = dwarf_rect.colliderect(rect_mushroom)
            if conflict:
                self.attack = True
                self.mushroom_y = self.screen_height * 0.57  # Высота после атаки
                self.mushroom_x = self.screen_width * 0.675 # Горизонтальное расположение
            else:
                self.attack = False
                self.mushroom_x = self.screen_width * 0.7
                self.mushroom_y = self.screen_height * 0.58  # Обычная высота







