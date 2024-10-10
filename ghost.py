import asyncio
import pygame
import os


class Ghost:
    """Призрак 0 LVL"""
    def __init__(self, screen_height, screen_width):
        self.ghost_image = None
        self.ghost_image = None

        # Начальная позиция персонажа
        self.ghost_x = screen_width * 0.7 # Положение слева
        self.ghost_y = screen_height * 0.05 # Вычисляем высоту пола


    def ghost_characteristics(self):
        # Загрузка спрайта злодея
        evil_dwarf = pygame.image.load("media/image_main/ghost.png").convert_alpha()

        # Задание нового размера персонажа (например, 100x100 пикселей)
        self.ghost_image = pygame.transform.scale(evil_dwarf, (100, 100))

        data = {
            'ghost_image': self.ghost_image,
            'ghost_x': self.ghost_x,
            'ghost_y': self.ghost_y
        }

        return data

    def actions_ghost(self, ghost, size):
        """Перемещение ghost"""

        # if self.evil_dwarf_x != 100 and self.evil_check_x is True:
        #     self.evil_dwarf_x = evil_dwarf.actions_evil_dwarf_LEFT(self.evil_dwarf_x, self.evil_check_x)
        # else:
        #     if self.evil_dwarf_x == size[0] - 100:
        #         self.evil_check_x = True
        #         return self.evil_dwarf_x
        #
        #     self.evil_check_x = False
        #     self.evil_dwarf_x = evil_dwarf.actions_evil_dwarf_RIGHT(self.evil_dwarf_x, self.evil_check_x)
        #
        #
        # return self.evil_dwarf_x

    # def actions_evil_dwarf_LEFT(self, evil_dwarf_x, evil_check_x):
    #     self.evil_dwarf_x = evil_dwarf_x
    #     self.evil_dwarf_x -= 0.5
    #
    #     return self.evil_dwarf_x
    #
    # def actions_evil_dwarf_RIGHT(self, evil_dwarf_x, evil_check_x):
    #     self.evil_dwarf_x = evil_dwarf_x
    #     self.evil_dwarf_x += 0.5
    #
    #     return self.evil_dwarf_x


