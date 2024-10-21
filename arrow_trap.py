import asyncio
import pygame
import os
import time
import random
import math


class ArrowTrap:
    """Ловушка со стрелой и плитой"""
    def __init__(self, screen_height, screen_width):
        self.screen_height = screen_height
        self.screen_width = screen_width

        self.time_arrow_trap_location = time.time()
        self.last_move_time = time.time() # Время последнего движения

        # Позиция плиты
        self.stove_trap_x = screen_width * 0.5 # Положение слева
        self.stove_trap_y = screen_height * 0.949 # Вычисляем высоту пола

        # Начальная позиция стрелы
        self.arrow_x = screen_width # Положение слева
        self.arrow_y = screen_height * 0.9 # Вычисляем высоту пола

        self._pressure_stove = False # Нажатие на плиту
        self.arrow_image = None

    def screen_stove_trap_0_lvl(self, current_location, screen):
        """Отображение плиты"""
        if current_location == 0:
            black_square = pygame.Surface((self.screen_width * 0.1, self.screen_height * 0.01))

            # Задаем цвет поверхности (черный)
            black_square.fill((0, 0, 0)) # RGB (0, 0, 0) – черный цвет
            screen.blit(black_square, (self.stove_trap_x, self.stove_trap_y))

    def screen_arrow_trap_0_lvl(self, current_location, screen):
        """Отображение стрелы"""
        if current_location == 0:
            image = pygame.image.load('media/image_main/Стрела-1.png')
            self.arrow_image = pygame.transform.scale(image, (self.screen_width * 0.1, self.screen_height * 0.01))

            screen.blit(self.arrow_image, (self.arrow_x, self.arrow_y))

    def stove_trap_rect(self):
        """Rect плиты"""
        black_square = pygame.Surface((self.screen_width * 0.1, self.screen_height * 0.01))
        stove_trap_rect = pygame.Rect(self.stove_trap_x, self.stove_trap_y, black_square.get_width(), black_square.get_height())
        return stove_trap_rect

    def arrow_rect(self):
        """Rect стрелы"""
        black_square = pygame.Surface((self.screen_width * 0.1, self.screen_height * 0.01))
        arrow_trap_rect = pygame.Rect(self.arrow_x, self.arrow_y, black_square.get_width(), black_square.get_height())
        return arrow_trap_rect

    def checking_pressure_stove(self, current_location, dwarf_rect):
        """Проверка нажатия персонажа на плиту"""
        stove_rect = self.stove_trap_rect()
        if current_location == 0:
            if dwarf_rect.colliderect(stove_rect):
                return True

    def move_arrow(self, check_stove):
        """Движение стрелы"""
        if check_stove:
            self._pressure_stove = True

        if self._pressure_stove:
            self.arrow_x -= 5

        # Проверяем, вышла ли стрела за границу экрана
        if self.arrow_x < 0:
            self._pressure_stove = False  # Сбрасываем флаг давления
            self.arrow_x = self.screen_width  # Возвращаем стрелу в исходное положение