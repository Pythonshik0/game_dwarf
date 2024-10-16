import asyncio
import pygame
import os
import time
import random
import math


class StoneTrap:
    """Каменная ловушка из под текстуры"""
    def __init__(self, screen_height, screen_width):
        self.stone_trap_image = None

        self.screen_height = screen_height
        self.screen_width = screen_width

        # Начальная позиция персонажа
        self.stone_trap_x = screen_width * 0.3 # Положение слева
        self.stone_trap_y = screen_height * 0.96 # Вычисляем высоту пола
        self.check_trap = False
        self.check_trap_max = False # Переменная запускающая закрытие ловушки внизу
        self.timeout = 0.5

        # Размер ловушки
        self.trap_width = self.screen_width * 0.1
        self.trap_height = self.screen_height * 0.7

    def stone_trap_rect(self):
        rect = pygame.Rect(self.stone_trap_x, self.stone_trap_y, self.trap_width, self.trap_height)
        return rect

    def screen_stone_trap(self, screen):
        trap = pygame.Surface((self.trap_width, self.trap_height))

        # Задаем цвет поверхности (черный)
        trap.fill((0, 0, 0))  # RGB (0, 0, 0) – черный цвет
        screen.blit(trap, (self.stone_trap_x, self.stone_trap_y)) # Отображаем платформы

    def move(self, current_location, now, platforms):
        # Timeout срабатывания ловушки
        frame_delay = 5000
        if now - self.timeout > frame_delay and self.check_trap is False and self.check_trap_max is False:
            self.check_trap = True
            self.timeout = now

        # Ловушка поднимается
        if self.check_trap:
            self.stone_trap_y -= 4

        # Ловушка наверху останавливается
        rect_trap = self.stone_trap_rect()
        for platform in platforms[current_location]:
            if rect_trap.colliderect(platform):
                self.check_trap = False
                self.check_trap_max = True

        # Ловушка опускается
        if rect_trap.top < self.screen_height - 35 and self.check_trap_max:
            self.stone_trap_y += 4
            self.timeout = now

        # Ловушка внизу останавливается
        if rect_trap.top > self.screen_height - 35:
            self.check_trap_max = False
            self.check_trap = False

    def contact_hero(self, rect_dwarf):
        """Функция контакта с гл героем"""
        rect_trap = self.stone_trap_rect()

        if rect_dwarf.colliderect(rect_trap):
            # Проверка, вошел ли персонаж в ловушку с левой стороны
            if rect_dwarf.right > rect_trap.left and rect_dwarf.centerx < rect_trap.centerx:
                # Отталкиваем персонажа влево
                rect_dwarf.x = rect_trap.left - rect_dwarf.width  # Перемещаем персонажа влево от ловушки

            # Проверка, вошел ли персонаж в ловушку с правой стороны
            elif rect_dwarf.left < rect_trap.right and rect_dwarf.centerx > rect_trap.centerx:
                # Отталкиваем персонажа вправо
                rect_dwarf.x = rect_trap.right  # Перемещаем персонажа вправо от ловушки

        return rect_dwarf.x, rect_dwarf.y