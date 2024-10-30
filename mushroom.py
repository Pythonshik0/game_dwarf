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
                pygame.image.load('media/image_main/грибочек-атата-1.png').convert_alpha(),
                pygame.image.load('media/image_main/грибочек-атата-2.png').convert_alpha(),
                pygame.image.load('media/image_main/грибочек-атата-3.png').convert_alpha(),
                pygame.image.load('media/image_main/грибочек-атата-4.png').convert_alpha(),
                pygame.image.load('media/image_main/грибочек-атата.png').convert_alpha(),
            ]
        }
        self.last_update = pygame.time.get_ticks()
        self.current_frame = 0 # Для гифки стоя на месте
        self.current_attack = 0 # Для гифки атаки

        # Начальная позиция персонажа
        self.mushroom_x = screen_width * 0.7 # Положение слева
        self.mushroom_y = screen_height * 0.58 # Вычисляем высоту пола

        # Размер перса
        self.mushroom_height = screen_height * 0.05
        self.mushroom_width = screen_width * 0.03

        self.mushroom_images = [pygame.transform.scale(img, (self.mushroom_width, self.mushroom_height)) for img in self.images['worth']]
        self.hit_image = [pygame.transform.scale(img, (self.screen_width * 0.08, self.screen_height * 0.06)) for img in self.images['hit']]

    def screen_mushroom_0_lvl(self, current_location, screen):
        if current_location == 0:
            if not self.attack:
                screen.blit(self.mushroom_images[self.current_frame], (self.mushroom_x, self.mushroom_y))
            else:
                attack_image = self.hit_image[self.current_attack]
                screen.blit(attack_image, (self.mushroom_x - (self.screen_width * 0.025), self.mushroom_y - (self.screen_height * 0.01)))

        # # Отображаем центры персонажа и гриба для визуального контроля
        # pygame.draw.circle(screen, (255, 0, 0), self.rect_mushroom().center, 5)  # Центр персонажа (красный)

    def rect_mushroom(self):
        """Возвращает прямоугольник гриба для коллизий."""
        if not self.attack:
            return pygame.Rect(self.mushroom_x, self.mushroom_y, self.mushroom_images[self.current_frame].get_width(), self.mushroom_images[self.current_frame].get_height())
        else:
            return pygame.Rect(self.mushroom_x - (self.screen_width * 0.025), self.mushroom_y - (self.screen_height * 0.01), self.hit_image[self.current_attack].get_width(), self.hit_image[self.current_attack].get_height())

    def gif_dwarf(self, now):
        """Создание движения картинки."""

        # Если атаки нет
        if not self.attack:
            frame_delay = 500
            if now - self.last_update > frame_delay:
                self.current_frame = (self.current_frame + 1) % len(self.mushroom_images)  # Переход к следующему кадру
                self.last_update = now  # Обновляем время последнего обновления
        else:
            # Если идет атака
            frame_delay = 100
            if now - self.last_update > frame_delay:
                self.current_attack = (self.current_attack + 1) % len(self.hit_image) # Переход к следующему кадру
                self.last_update = now  # Обновляем время последнего обновления

    def move_mushroom(self, current_location, dwarf_rect, screen):
        """Функция движений грибочка в зависимости от локации"""
        rect_mushroom = self.rect_mushroom()

        if abs(dwarf_rect.bottom - rect_mushroom.bottom) < 100:
            if dwarf_rect.centerx >= rect_mushroom.centerx:
                self.mushroom_x += 1
            else:
                self.mushroom_x -= 1


    def hit_mushroom(self, current_location, dwarf_rect):
        rect_mushroom = self.rect_mushroom()
        if current_location == 0:  # Для 0 уровня
            # Проверка попадания в радиус атаки
            conflict = dwarf_rect.colliderect(rect_mushroom)
            if conflict:
                self.attack = True
            else:
                self.attack = False







