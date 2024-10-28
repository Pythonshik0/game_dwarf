import asyncio
import pygame
import os
import time
import random
import math

from platforms import bounding_box_ghost as bounding_box_ghost_0_lvl
from platforms import platforms


class Ghost:
    """Призрак 0 LVL"""
    def __init__(self, screen_height, screen_width):
        self.ghost_image = None

        self.screen_height = screen_height
        self.screen_width = screen_width

        self.bullet_image = pygame.image.load('media/image_main/Сфера-1-lvl.png')
        self.bullet_image = pygame.transform.scale(self.bullet_image, (30, 30))  # Масштабируем изображение пули
        self.time_ghost_location = time.time()
        self.last_move_time = time.time() # Время последнего движения
        self.direction = None
        self.check = False
        self.ghost_speed = 4 # Скорость ghost
        self.ghost_bullets = [] # Выстрелы злодея
        self.timer_shot_ghost = 0.5

        # Начальная позиция персонажа
        self.ghost_x = screen_width * 0.7 # Положение слева
        self.ghost_y = screen_height * 0.05 # Вычисляем высоту пола

        evil_dwarf = pygame.image.load("media/image_main/ghost.png").convert_alpha()
        self.ghost_image = pygame.transform.scale(evil_dwarf, (100, 100)) # Задание нового размера персонажа (например, 100x100 пикселей)

    def screen_ghost_0_lvl(self, current_location, screen):
        if self.ghost_image and current_location == 0:
            screen.blit(self.ghost_image, (self.ghost_x, self.ghost_y))

    def rect_ghost(self):
        return pygame.Rect(self.ghost_x, self.ghost_y, self.ghost_image.get_width(), self.ghost_image.get_height())  # Создаем прямоугольник для призрака

    def move_ghost(self, current_location):
        """Функция движений призрака в зависимости от локации"""
        bounding_box = bounding_box_ghost_0_lvl(self.screen_width, self.screen_height) # Зоны перемещения призрака на 0 lvl
        current_time = time.time()  # Получаем текущее время
        ghost_rect = self.rect_ghost()

        if current_location == 0: # Поведение в bounding_box на 0 уровне, на разных уровнях поведение отличается
            # Если прошло меньше 6 секунд, перемещаем призрака в первой bounding box
            if current_time - self.time_ghost_location < 6:
                bounding_box = bounding_box[current_location][0]
                if ghost_rect.top > bounding_box.top and self.check is True:
                    self.ghost_y -= 1
                else:
                    self.check = False  # Переключаем направление движения

            # Если прошло от 6 до 12 секунд, перемещаем призрака во второй bounding box
            elif 6 <= current_time - self.time_ghost_location < 12:
                bounding_box = bounding_box[current_location][1]
                if ghost_rect.bottom < bounding_box.bottom and self.check is False:
                    self.ghost_y += 1
                else:
                    self.check = True  # Снова переключаем направление движения

            # Если прошло больше 12 секунд, обновляем таймер и возвращаем в первую bounding box
            elif current_time - self.time_ghost_location >= 12:
                bounding_box = bounding_box[current_location][0]
                self.time_ghost_location = current_time  # Сбрасываем таймер
                self.check = True  # Готовим к движению в следующем цикле

            # Если прошло достаточно времени, выбираем новое направление
            if time.time() - self.last_move_time > 0.4:  # например, 0.5 секунды
                self.direction = random.choice(['up', 'down', 'left', 'right'])
                self.last_move_time = time.time()  # Обновляем время последнего выбора направления

        elif current_location == 1: # Поведение в bounding_box на 1 уровне
            pass

        # Перемещаем призрака в случайном направлении, если он не выходит за границы bounding box
        if self.direction == 'up' and self.ghost_y > bounding_box.top:
            self.ghost_y -= self.ghost_speed
        elif self.direction == 'down' and self.ghost_y < bounding_box.bottom - self.ghost_image.get_height():
            self.ghost_y += self.ghost_speed
        elif self.direction == 'left' and self.ghost_x > bounding_box.left:
            self.ghost_x -= self.ghost_speed
        elif self.direction == 'right' and self.ghost_x < bounding_box.right - self.ghost_image.get_width():
            self.ghost_x += self.ghost_speed

    def shot_ghost(self, dwarf_x, dwarf_y, current_location, dwarf, size):
        """Функция выстрелов в гл героя"""
        distance_x = dwarf_x - self.ghost_x
        distance_y = dwarf_y - self.ghost_y

        shot_timer = time.time()  # Текущее время в секундах

        if current_location == 0 and self.ghost_image and abs(distance_x) < 1000 and abs(distance_y) < 100 and (shot_timer - self.timer_shot_ghost > 0.5):
            # Создаем пулю на уровне призрака
            distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
            """
            Формула с возведением в квадрат необходима для расчета евклидова расстояния между двумя точками на плоскости. 
            Это стандартная формула для вычисления расстояния между точками в пространстве с двумя координатами (x и y):
            distance = кв. корень (x2 - x1)**2 + (y2 - y1)**2
            (x2 - x1) - это self.dwarf_x - self.ghost_x
            (y2 - y1) - это self.dwarf_y - self.ghost_y
            """
            EVIL_bullet_rect = pygame.Rect(self.ghost_x + self.ghost_image.get_width() // 2,
                                           self.ghost_y + self.ghost_image.get_height() // 2,
                                           self.bullet_image.get_width(),
                                           self.bullet_image.get_height())  # Прямоугольник для пули

            # Вычисляем направления полета пули
            direction_x = distance_x / distance # Как пример получается 0.7 (по оси x перемешаем на 0.7)
            direction_y = distance_y / distance # Как пример получается 0.9 (по оси x перемешаем на 0.9)

            # Добавляем пулю в список с её скоростью и направлением
            self.ghost_bullets.append((EVIL_bullet_rect, direction_x, direction_y))
            self.timer_shot_ghost = shot_timer

        # Стрельба в гл. героя
        dwarf_rect = dwarf.dwarf_rect()
        ghost_bullet_rects = [bullet for bullet, _, _ in self.ghost_bullets]

        # Пули исчезаю, когда сталкиваются с гл. героем
        collided_indices_ghost = dwarf_rect.collidelistall(ghost_bullet_rects)
        if collided_indices_ghost:
            for index in collided_indices_ghost: # Удаляем все столкнувшиеся пули
                del self.ghost_bullets[index]

        # Пули исчезаю, когда сталкиваются со платформами
        rect_platforms = platforms(size[0], size[1])[current_location]
        for platform_rect in rect_platforms:
            collided_indices_platforms = platform_rect.collidelistall(ghost_bullet_rects)
            if collided_indices_platforms:
                # Обработка столкновения
                for index in collided_indices_platforms:
                    del self.ghost_bullets[index]

        # Обновление положения пуль злого призрака
        updated_bullets = []
        for bullet, direction_x, direction_y in self.ghost_bullets:
            bullet_speed = 2  # Скорость пули

            # Обновляем координаты пули на основе её направления и скорости
            bullet.x += direction_x * bullet_speed
            bullet.y += direction_y * bullet_speed

            # Удаляем пули, которые вышли за экран
            if 0 < bullet.x < size[0] and 0 < bullet.y < size[1]:
                updated_bullets.append((bullet, direction_x, direction_y))

            # Обновляем список пуль
            self.ghost_bullets = updated_bullets


