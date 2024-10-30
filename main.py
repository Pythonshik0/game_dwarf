import pygame
import os
from PIL import Image
import time
import random
import math

from ghost import *
from dwarf import Dwarf
from stone_trap import StoneTrap
from utils import screen_ghost_shot
from platforms import platforms, background_images, ladders, StaticObject, bounding_box_ghost
from arrow_trap import ArrowTrap
from mushroom import Mushroom

shot_delay = 0.5
clock = pygame.time.Clock()


class GameDwarf:
    def __init__(self, dwarf):
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

        self.dwarf_x_new = None # Положение dwarf при столкновении с ловушкой stone trap
        self.dwarf_y_new = None # Положение dwarf при столкновении с ловушкой stone trap

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

        now = pygame.time.get_ticks()  # Время последнего обновления кадра

        if self.dwarf_image:
            dwarf.gif_dwarf(now)
            dwarf.move_ladders(ladders, keys, self.current_location) # Движение по лестнице
            dwarf.moving_the_dwarf(keys) # Движение вправо
            dwarf.dwarf_is_jumping_K_UP(keys) # Прыжок dwarf
            dwarf.dwarf_apply_gravity(floor_y, self.current_location, platforms) # Гравитация и движение персонажа на карте
            dwarf.dwarf_check_boundaries(size, self.current_location) # Проверка выхода за границы экрана и смена уровня
            dwarf.collision_platform(self.current_location, platforms, ghost_rect) # Удаление пулек при попадании в платформу
            dwarf.shoot(keys, ghost_image, ghost_bullets) # Стрельба с учетом времени задержки между выстрелами
            dwarf.update_bullets(size) # Обновление положения пуль и удаление пуль, которые вышли за экран
            dwarf.door_next_level(self.door) # Переход на след уровень (Дверь)

    def ghost(self):
        """Управление движениями / стрельбой / прыжками и тд. персонажа (ПРИЗРАК)"""
        ghost.move_ghost(self.current_location) # Функция движений призрака в зависимости от локации
        dwarf_x, dwarf_y = dwarf.dwarf_x, dwarf.dwarf_y
        ghost.shot_ghost(dwarf_x, dwarf_y, self.current_location, dwarf, size) # Функция выстрелов в гл героя


    def mushroom(self, screen):
        mushroom.move_mushroom(self.current_location, dwarf.dwarf_rect(), screen) # Движение за гл героем
        mushroom.hit_mushroom(self.current_location, dwarf.dwarf_rect()) # Атака на гл. героя

        mushroom.gif_dwarf(pygame.time.get_ticks()) # Гифка грибочка

    def stone_trap(self):
        """Ловушки каменные"""
        now = pygame.time.get_ticks()
        stone_trap.move(self.current_location, now, platforms) # Движение ловушки

        dwarf_rect = dwarf.dwarf_rect() # Rect главного героя
        self.dwarf_x_new, self.dwarf_y_new = stone_trap.contact_hero(dwarf_rect) # Столкновение Rect trap и Rect dwarf

        dwarf.contact_trap_update_x_or_y(self.dwarf_x_new, self.dwarf_y_new) # Обновление персонажа dwarf при столкновении с stone trap

    def arrow_trap(self):
        """Ловушка со стрелой при нажатии на плиту"""
        dwarf_rect = dwarf.dwarf_rect() # Rect главного героя
        check_stove = arrow_trap.checking_pressure_stove(self.current_location, dwarf_rect) # Проверка на нажатие плиты персонажем

        arrow_trap.move_arrow(check_stove)

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

        # for bounding in bounding_box_ghost[self.current_location]:
        #     black_square = pygame.Surface((bounding.width, bounding.height))
        #
        #     # Задаем цвет поверхности (черный)
        #     black_square.fill((0, 0, 0))  # RGB (0, 0, 0) – черный цвет
        #     screen.blit(black_square, (bounding.x, bounding.y)) # Отображаем платформы
        #
        # # Отображаем лестницу на 0 уровне
        # for ladder in ladders[self.current_location]:
        #     black_square = pygame.Surface((ladder.width, ladder.height))
        #
        #     # Задаем цвет поверхности (черный)
        #     black_square.fill((0, 0, 0))  # RGB (0, 0, 0) – черный цвет
        #     screen.blit(black_square, (ladder.x, ladder.y)) # Отображаем платформы

        dwarf.dwarf_screen(screen) # Отображение персонажа
        arrow_trap.screen_stove_trap_0_lvl(self.current_location, screen) # Отображение плиты для нажатия
        arrow_trap.screen_arrow_trap_0_lvl(self.current_location, screen) # Отображение ловушки со стрелой
        ghost.screen_ghost_0_lvl(self.current_location, screen) # Отображаем ghost на 0 уровне
        mushroom.screen_mushroom_0_lvl(self.current_location, screen) # Отображаем грибочка

        # Отображение пуль dwarf
        dwarf_bullets = dwarf.dwarf_bullets
        bullet_image = dwarf.bullet_image
        screen_ghost_shot(bullet_image, dwarf_bullets, screen)

        # Отображение пуль ghost
        ghost_bullets = ghost.ghost_bullets
        bullet_image = ghost.bullet_image
        screen_ghost_shot(bullet_image, ghost_bullets, screen)

        # Отображаем ловушки
        stone_trap.screen_stone_trap(screen)

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
        clock.tick(120) # 120 ФПС
        pygame.display.flip()  # Обновляем экран

    def main(self, size, floor_y):
        while self.runGame:
            self.handle_events()
            keys = pygame.key.get_pressed()
            self.dwarf(keys, floor_y, size) # Функция работы гл героя
            self.ghost() # Призрак
            self.mushroom(screen) # Грибочек
            self.arrow_trap()
            self.stone_trap()
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
    dwarf = Dwarf(screen.get_height(), platforms, screen.get_width()) # Гл. перс 0 lvl

    """Противники"""
    ghost = Ghost(screen.get_height(), screen.get_width()) # Призрак
    mushroom = Mushroom(screen.get_height(), screen.get_width()) # Грибочек

    """Ловушки"""
    stone_trap = StoneTrap(screen.get_height(), screen.get_width()) # Ловушка каменные шипы


    # img = Image.open('media/image_main/Стрела-1.png') # Загрузка изображения
    # img.save('media/image_main/Стрела-1.png', 'PNG', icc_profile=None) # Сохранение изображения без sRGB профиля
    arrow_trap = ArrowTrap(screen.get_height(), screen.get_width()) # Ловушка со стрелой

    game_dwarf = GameDwarf(dwarf)
    game_dwarf.main(size, floor_y)
