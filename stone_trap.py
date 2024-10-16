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
        frame_delay = 5000
        if now - self.timeout > frame_delay and self.check_trap is False and self.check_trap_max is False:
            self.check_trap = True
            self.timeout = now

        if self.check_trap:
            self.stone_trap_y -= 2


        rect_trap = self.stone_trap_rect()

        for platform in platforms[current_location]:
            if rect_trap.colliderect(platform):
                self.check_trap = False
                self.check_trap_max = True

        if rect_trap.top < self.screen_height - 35 and self.check_trap_max:
            self.stone_trap_y += 2
            self.timeout = now

        if rect_trap.top > self.screen_height - 35:
            self.check_trap_max = False
            self.check_trap = False
            # self.timeout = now
        # elif rect_trap.top > self.screen_height - 35 and self.check_trap_max:



        # for platform in platforms[current_location]:
        #     if (character_rect.colliderect(platform)) and \
        #             (self.vertical_velocity >= 0) and \
        #             (character_rect.bottom <= platform.top + 10) and \
        #             (platform.bottom > character_rect.bottom) and \
        #             (character_rect.bottom > platform.top):  # Проверка, что персонаж сверху платформы
        #
        #         self.dwarf_y = platform.top - self.dwarf_image[
        #             self.current_frame].get_height()  # Корректируем положение на платформе
        #         self.dwarf_is_jumping = False  # Завершаем прыжок
        #         self.vertical_velocity = 0  # Останавливаем вертикальную скорость
        #         break


        # print('тут')
        # if timeout - self.timeout > 10 and current_location == 0:
        #     pass
        # else:
        #     self.timeout = time.time()
        #     self.stone_trap_y -= 2
        #     self.timeout = time.time()

