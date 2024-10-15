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
        self.stone_trap_y = screen_height * 0.95 # Вычисляем высоту пола
        self.check_trap = False
        self.timeout = 0.5


    def screen_stone_trap(self, screen):
        trap = pygame.Surface((self.screen_width * 0.1, self.screen_height * 0.7))

        # Задаем цвет поверхности (черный)
        trap.fill((0, 0, 0))  # RGB (0, 0, 0) – черный цвет
        screen.blit(trap, (self.stone_trap_x, self.stone_trap_y)) # Отображаем платформы

    def move(self, current_location, now):
        frame_delay = 5000
        if now - self.timeout > frame_delay and self.check_trap is False:
            self.check_trap = True
            self.timeout = now

        rect_trap =
        if self.check_trap:
            self.stone_trap_y -= 2
            self.timeout = time.time()


        # print('тут')
        # if timeout - self.timeout > 10 and current_location == 0:
        #     pass
        # else:
        #     self.timeout = time.time()
        #     self.stone_trap_y -= 2
        #     self.timeout = time.time()

