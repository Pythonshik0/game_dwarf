import asyncio
import pygame
import os


class TheEvilDwarf:
    """ЗЛОЙ ГНОМ 0 LVL"""
    def __init__(self, screen_height):
        self.evil_dwarf_image = None
        self.dwarf_image = None
        # Начальная позиция персонажа
        self.evil_dwarf_x = 600 # Положение слева
        self.evil_dwarf_y = 200 # Вычисляем высоту пола

        self.evil_check_x = True # Переменная для отслеживания перемещения вправо или влево

    def evil_dwarf_characteristics(self):
        # Загрузка спрайта злодея
        evil_dwarf = pygame.image.load("media/image_main/Злой гном-0lvl.png").convert_alpha()

        # Задание нового размера персонажа (например, 100x100 пикселей)
        self.evil_dwarf_image = pygame.transform.scale(evil_dwarf, (100, 100))

        data = {
            'evil_dwarf_image': self.evil_dwarf_image,
            'evil_dwarf_x': self.evil_dwarf_x,
            'evil_dwarf_y': self.evil_dwarf_y
        }

        return data

    def actions_evil_dwarf(self, evil_dwarf, size):
        """Перемещение EVIL DWARF"""
        if self.evil_dwarf_x != 100 and self.evil_check_x is True:
            self.evil_dwarf_x = evil_dwarf.actions_evil_dwarf_LEFT(self.evil_dwarf_x, self.evil_check_x)
        else:
            if self.evil_dwarf_x == size[0] - 100:
                self.evil_check_x = True
                return self.evil_dwarf_x

            self.evil_check_x = False
            self.evil_dwarf_x = evil_dwarf.actions_evil_dwarf_RIGHT(self.evil_dwarf_x, self.evil_check_x)


        return self.evil_dwarf_x

    def actions_evil_dwarf_LEFT(self, evil_dwarf_x, evil_check_x):
        self.evil_dwarf_x = evil_dwarf_x
        self.evil_dwarf_x -= 0.5

        return self.evil_dwarf_x

    def actions_evil_dwarf_RIGHT(self, evil_dwarf_x, evil_check_x):
        self.evil_dwarf_x = evil_dwarf_x
        self.evil_dwarf_x += 0.5

        return self.evil_dwarf_x


