import asyncio
import pygame
import os


class Dwarf:
    def __init__(self, screen_height):
        self.dwarf_image = None
        # Начальная позиция персонажа
        self.dwarf_x = 50 # Положение слева
        self.dwarf_y = screen_height - 100 # Вычисляем высоту пола
        self.dwarf_speed = 0.4  # Скорость перемещения персонажа
        self.dwarf_is_jumping = False
        self.dwarf_jump_speed = 8  # Начальная высота прыжка
        self.dwarf_bullets = [] # Список для хранения пуль

        self.dwarf_bullet_speed = 1.1 # Скорость пуль

        # Переменная для хранения направления стрельбы
        self.dwarf_shoot_direction = 1  # 1 - вправо, -1 - влево

        self.dwarf_can_shoot = True # Флаг для проверки, можно ли стрелять
        self.dwarf_space = True # Проверка на пыжок

    def dwarf_characteristics(self):
        # Загрузка спрайта персонажа
        dwarf = pygame.image.load("media/image_main/dworf.png").convert_alpha()

        # Задание нового размера персонажа (например, 100x100 пикселей)
        self.dwarf_image = pygame.transform.scale(dwarf, (100, 100))
        data = {
            'dwarf_image': self.dwarf_image, # Задание нового размера персонажа
            'dwarf_x': self.dwarf_x, # Положение слева
            'dwarf_y': self.dwarf_y, # Положение над полом
            'character_speed': self.dwarf_speed, # Скорость перемещения персонажа
            'dwarf_is_jumping': self.dwarf_is_jumping, # Проверка на нажатый пробел
            'jump_speed': self.dwarf_jump_speed, # Начальная высота прыжка
            'dwarf_bullets': self.dwarf_bullets, # Список для хранения пуль
            'dwarf_bullet_speed': self.dwarf_bullet_speed, # Скорость пуль
            'dwarf_shoot_direction': self.dwarf_shoot_direction, # Направление выстрела
            'dwarf_can_shoot': self.dwarf_can_shoot,
            'dwarf_space': self.dwarf_space,
        }
        return data

    def moving_the_dwarf_LEFT(self, character_x):
        self.dwarf_x = character_x
        self.dwarf_x -= self.dwarf_speed
        self.dwarf_shoot_direction = -1  # Устанавливаем направление стрельбы влево

        # Перемещаем гнома влево и задаем направление стрельбы
        return self.dwarf_x, self.dwarf_shoot_direction

    def moving_the_dwarf_RIGHT(self, character_x):
        self.dwarf_x = character_x
        self.dwarf_x += self.dwarf_speed
        self.dwarf_shoot_direction = 1  # Устанавливаем направление стрельбы влево

        # Перемещаем гнома вправо и задаем направление стрельбы
        return self.dwarf_x, self.dwarf_shoot_direction


    def dwarf_is_jumping_K_UP(self, keys, vertical_velocity):
        if keys[pygame.K_UP] and self.dwarf_is_jumping is False:
            self.dwarf_is_jumping = True
            vertical_velocity -= self.dwarf_jump_speed
            self.dwarf_space = True

            return self.dwarf_is_jumping, self.dwarf_space, vertical_velocity

    async def dwarf_gravity(self, vertical_velocity, gravity, max_fall_speed):
        if self.dwarf_is_jumping:
            self.dwarf_y += vertical_velocity  # Перемещение по оси Y (430 + -8)
            vertical_velocity += gravity  # Применение гравитации (ускорение вниз)

            # Ограничение вертикальной скорости (падение не быстрее максимума)
            if vertical_velocity > max_fall_speed:
                vertical_velocity = max_fall_speed

            return self.dwarf_y, vertical_velocity