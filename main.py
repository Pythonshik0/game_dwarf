import pygame
import os
from PIL import Image
import time
import random
import math

from ghost import *
from dwarf import Dwarf
from utils import screen_ghost_shot
from platforms import platforms, background_images, ladders, StaticObject, bounding_box_ghost



shot_delay = 0.5


class GameDwarf:
    def __init__(self, dwarf, ghost):
        # Инициализация игры
        self.runGame = True

        self.dwarf_image = dwarf.dwarf_image # Изображение персонажа

        # Общие переменные
        self.current_location = 0  # Текущая локация

        # Дверь на следующий уровень
        door_image = pygame.image.load('media/image_main/дверь-закрытая.png').convert_alpha()
        image_size = 100, 150
        self.door = StaticObject(door_image, (1250, 80), image_size) # Создаем наш объект

        # Точка spawn
        home_image = pygame.image.load('media/image_main/Save.png').convert_alpha()
        image_size = 250, 250
        self.home_image = StaticObject(home_image, (0, 511), image_size) # Создаем наш объект

    def handle_events(self):
        # Обработка событий (закрытие окна)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.runGame = False  # Завершаем игру, если закрыли окно

    def dwarf(self, keys, floor_y, size):
        """Управление движениями/стрельбой/прыжками и тд. персонажа (ГЕРОЯ)"""
        ghost_rect = ghost.rect_ghost()
        ghost_bullets = ghost.ghost_bullets
        ghost_image = ghost.ghost_image

        if self.dwarf_image:
            dwarf.move_ladders(ladders, keys, self.current_location) # Движение по лестнице
            dwarf.moving_the_dwarf_LEFT(keys) # Движение влево
            dwarf.moving_the_dwarf_RIGHT(keys) # Движение вправо
            dwarf.dwarf_is_jumping_K_UP(keys) # Прыжок dwarf
            dwarf.dwarf_apply_gravity(floor_y, self.current_location, platforms) # Гравитация и движение персонажа на карте
            dwarf.dwarf_check_boundaries(size, self.current_location) # Проверка выхода за границы экрана и смена уровня
            dwarf.collision_platform(self.current_location, platforms, ghost_rect) # Удаление пулек при попадании в платформу
            dwarf.shoot(keys, ghost_image, ghost_bullets) # Стрельба с учетом времени задержки между выстрелами
            dwarf.update_bullets(size) # Обновление положения пуль и удаление пуль, которые вышли за экран
            dwarf.door_next_level(self.door) # Переход на след уровень (Дверь)

    def ghost(self):
        """Управление движениями / стрельбой / прыжками и тд. персонажа (ПРИЗРАКА)"""
        ghost.move_ghost(self.current_location) # Функция движений призрака в зависимости от локации
        dwarf_x, dwarf_y = dwarf.dwarf_x, dwarf.dwarf_y
        ghost.shot_ghost(dwarf_x, dwarf_y, self.current_location, dwarf, size) # Функция выстрелов в гл героя

    def draw(self, screen):
        # Отрисовка элементов игры
        screen.blit(background_images[self.current_location], [0, 0])  # Отображаем фон

        self.home_image.draw(screen) # Отображаем место spawn
        self.door.draw(screen) # Отображаем переход на след уровень

        # Отображение платформ
        # for platform in platforms[self.current_location]:
        #     black_square = pygame.Surface((platform.width, platform.height))
        #
        #     # Задаем цвет поверхности (черный)
        #     black_square.fill((0, 0, 0))  # RGB (0, 0, 0) – черный цвет
        #     screen.blit(black_square, (platform.x, platform.y)) # Отображаем платформы
        #
        # for bounding in bounding_box_ghost[self.current_location]:
        #     black_square = pygame.Surface((bounding.width, bounding.height))
        #
        #     # Задаем цвет поверхности (черный)
        #     black_square.fill((0, 0, 0))  # RGB (0, 0, 0) – черный цвет
        #     screen.blit(black_square, (bounding.x, bounding.y)) # Отображаем платформы

        # Отображаем лестницу на 0 уровне
        # for ladder in ladders[self.current_location]:
        #     black_square = pygame.Surface((ladder.width, ladder.height))
        #
        #     # Задаем цвет поверхности (черный)
        #     black_square.fill((0, 0, 0))  # RGB (0, 0, 0) – черный цвет
        #     screen.blit(black_square, (ladder.x, ladder.y)) # Отображаем платформы

        # Отображение персонажа
        dwarf.dwarf_screen(screen)

        # Отображаем ghost на 0 уровне
        ghost.screen_ghost_0_lvl(self.current_location, screen)

        # Отображение пуль dwarf
        dwarf_bullets = dwarf.dwarf_bullets
        bullet_image = dwarf.bullet_image
        screen_ghost_shot(bullet_image, dwarf_bullets, screen)

        # Отображение пуль ghost
        ghost_bullets = ghost.ghost_bullets
        bullet_image = ghost.bullet_image
        screen_ghost_shot(bullet_image, ghost_bullets, screen)

        # # Создаем полупрозрачный черный слой
        # dark_overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        # dark_overlay.fill((0, 0, 0, 220))  # Черный цвет с прозрачностью 200
        #
        # # Вырезаем круг вокруг персонажа (с радиусом 100 пикселей)
        # mask_radius = 200
        # mask_center = (self.dwarf_x + self.dwarf_image.get_width() // 2,
        #                self.dwarf_y + self.dwarf_image.get_height() // 2)
        #
        # pygame.draw.circle(dark_overlay, (0, 0, 0, 0), mask_center, mask_radius)  # Прозрачный круг
        #
        # # Наносим маску поверх экрана
        # screen.blit(dark_overlay, (0, 0))

        pygame.display.flip()  # Обновляем экран

    def main(self, size, floor_y):
        while self.runGame:
            self.handle_events()
            keys = pygame.key.get_pressed()
            self.dwarf(keys, floor_y, size) # Функция работы гл героя
            self.ghost() # Призрак
            self.draw(screen)

        pygame.quit()


def initialize_game():
    pygame.init()
    os.environ['SDL_VIDEO_WINDOW_POS'] = "100,100"

    screen_info = pygame.display.Info()
    screen_width = 1400
    screen_height = 800

    size = (screen_width, screen_height)
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)
    pygame.display.set_caption("DWARF")

    floor_y = screen_height - 40
    platforms_list = platforms(screen_width, screen_height)
    background_images_list = background_images(size)

    bounding_box_ghost_list = bounding_box_ghost(screen_width, screen_height) # Ограничивающий прямоугольник для призрака, чтобы он не выходил из него

    ladders_list = ladders(screen_width, screen_height)

    return size, screen, floor_y, platforms_list, background_images_list, ladders_list, bounding_box_ghost_list


if __name__ == "__main__":
    size, screen, floor_y, platforms, background_images, ladders, bounding_box_ghost = initialize_game()

    """Гл персы"""
    dwarf = Dwarf(screen.get_height(), platforms) # Гл. перс 0 lvl

    """Противники"""
    ghost = Ghost(screen.get_height(), screen.get_width()) # Противник 0 lvl

    game_dwarf = GameDwarf(dwarf, ghost)
    game_dwarf.main(size, floor_y)
