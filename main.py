import pygame
import os
from PIL import Image
import time
import random
import math

from ghost import *
from dwarf import Dwarf
from platforms import platforms, background_images, ladders, StaticObject, bounding_box_ghost



shot_delay = 0.5


class GameDwarf:
    def __init__(self, dwarf, ghost):
        # Инициализация игры
        self.runGame = True

        # Параметры персонажа
        self.dwarf_x = None # Положение по оси X
        self.dwarf_y = None # Положение по оси Y
        self.dwarf_is_jumping = None  # Флаг прыжка
        self.dwarf_space = None  # Проверка на прыжок
        self.dwarf_image = dwarf.dwarf_characteristics()['dwarf_image'] # Изображение персонажа
        self.bullet_image = dwarf.bullet_image
        self.dwarf_bullets = None # Список пуль
        self.dwarf_can_shoot = None # Флаг возможности стрельбы
        self.dwarf_bullet_speed = None # Скорость пули

        # Стрельбы перса
        self.dwarf_can_shoot_DUBLE = True

        # Злодеи 0 lvl
        self.ghost_bullets = [] # Выстрелы злодея
        self.ghost_image = ghost.ghost_characteristics()['ghost_image']  # Изображение персонажа
        self.ghost_x = ghost.ghost_characteristics()['ghost_x']
        self.ghost_y = ghost.ghost_characteristics()['ghost_y']
        self.direction = random.choice(['up', 'down', 'left', 'right'])  # Начальное направление
        self.last_move_time = time.time() # Время последнего движения
        self.time_ghost_location = time.time()
        self.check = False
        self.change_of_location = False # Смена чек бокса для ghost
        self.time_movie_box = 0 # Чек бокс в котором перемещается ghost

        # Общие переменные
        self.current_location = 0  # Текущая локация
        # self.timer_shot = 0  # Таймер выстрела
        self.timer_shot_ghost = 0.5
        self.ghost_speed = 0.5

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
        """Управление движениями/стрельбой/прыжками и тд. персонажа (гл. героя)"""
        if self.dwarf_image:
            self.dwarf_x = dwarf.dwarf_x
            self.dwarf_y = dwarf.dwarf_y
            self.dwarf_bullets = dwarf.dwarf_bullets
            self.dwarf_bullet_speed = dwarf.dwarf_bullet_speed

            dwarf_rect = pygame.Rect(self.dwarf_x, self.dwarf_y, self.dwarf_image.get_width(), self.dwarf_image.get_height())

            dwarf.move_ladders(ladders, keys, self.current_location) # Движение по лестнице
            dwarf.moving_the_dwarf_LEFT(keys, self.dwarf_x) # Движение влево
            dwarf.moving_the_dwarf_RIGHT(keys, self.dwarf_x) # Движение вправо
            dwarf.dwarf_is_jumping_K_UP(keys)  # Прыжок dwarf
            dwarf.dwarf_apply_gravity(floor_y, self.current_location, platforms) # Гравитация и движение персонажа на карте
            dwarf.dwarf_check_boundaries(size, self.current_location) # Выхода за границы экрана и смена уровня
            dwarf.collision_platform(self.current_location, platforms) # Удаление пулек при попадании в платформу
            dwarf.shoot(keys, self.ghost_image, self.ghost_bullets) # Стрельба с учетом времени задержки между выстрелами
            dwarf.update_bullets(size) # Обновление положения пуль и удаление пуль, которые вышли за экран

            if dwarf_rect.colliderect(self.door): # ПЕРЕХОД НА СЛЕДУЮЩИЙ УРОВЕНЬ (ДВЕРЬ)
                pass

    def ghost(self):
        """Функция движений / стрельюы и тд. (Призрака)"""
        current_time = time.time() # Получаем текущее время
        ghost_rect = pygame.Rect(self.ghost_x, self.ghost_y, self.ghost_image.get_width(), self.ghost_image.get_height()) # Создаем прямоугольник для призрака

        # Если прошло меньше 6 секунд, перемещаем призрака в первой bounding box
        if current_time - self.time_ghost_location < 6:
            bounding_box = bounding_box_ghost[self.current_location][0]
            if ghost_rect.top > bounding_box.top and self.check is True:
                self.ghost_y -= 1
            else:
                self.check = False  # Переключаем направление движения

        # Если прошло от 6 до 12 секунд, перемещаем призрака во второй bounding box
        elif 6 <= current_time - self.time_ghost_location < 12:
            bounding_box = bounding_box_ghost[self.current_location][1]
            if ghost_rect.bottom < bounding_box.bottom and self.check is False:
                self.ghost_y += 1
            else:
                self.check = True  # Снова переключаем направление движения

        # Если прошло больше 12 секунд, обновляем таймер и возвращаем в первую bounding box
        elif current_time - self.time_ghost_location >= 12:
            bounding_box = bounding_box_ghost[self.current_location][0]
            self.time_ghost_location = current_time  # Сбрасываем таймер
            self.check = True  # Готовим к движению в следующем цикле

        # Если прошло достаточно времени, выбираем новое направление
        if time.time() - self.last_move_time > 0.4:  # например, 0.5 секунды
            self.direction = random.choice(['up', 'down', 'left', 'right'])
            self.last_move_time = time.time()  # Обновляем время последнего выбора направления

        # Перемещаем призрака в случайном направлении, если он не выходит за границы bounding box
        if self.direction == 'up' and self.ghost_y > bounding_box.top:
            self.ghost_y -= self.ghost_speed
        elif self.direction == 'down' and self.ghost_y < bounding_box.bottom - self.ghost_image.get_height():
            self.ghost_y += self.ghost_speed
        elif self.direction == 'left' and self.ghost_x > bounding_box.left:
            self.ghost_x -= self.ghost_speed
        elif self.direction == 'right' and self.ghost_x < bounding_box.right - self.ghost_image.get_width():
            self.ghost_x += self.ghost_speed

        # ____________ВЕДЕМ ОГОНЬ ПО ГЛ ГЕРОЮ__________________________________
        # Проверяем расстояние до главного героя
        distance_x = self.dwarf_x - self.ghost_x
        distance_y = self.dwarf_y - self.ghost_y

        shot_timer = time.time()  # Текущее время в секундах

        # Условие для стрельбы (если герой близко и прошло достаточно времени с последнего выстрела)
        if self.current_location == 0 and self.ghost_image and abs(distance_x) < 1000 and abs(distance_y) < 100 and (
                shot_timer - self.timer_shot_ghost > 0.5):
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

        # Обновление положения пуль злого призрака
        if self.current_location == 0:
            updated_bullets = []
            for bullet, direction_x, direction_y in self.ghost_bullets:
                bullet_speed = 1  # Скорость пули

                # Обновляем координаты пули на основе её направления и скорости
                bullet.x += direction_x * bullet_speed
                bullet.y += direction_y * bullet_speed

                # Удаляем пули, которые вышли за экран
                if 0 < bullet.x < size[0] and 0 < bullet.y < size[1]:
                    updated_bullets.append((bullet, direction_x, direction_y))

            # Обновляем список пуль
            self.ghost_bullets = updated_bullets
        else:
            self.ghost_bullets = []

        # ________________Стрельба в ghost______________________________
        if self.ghost_image:
            self.dwarf_bullets = dwarf.dwarf_bullets
            ghost_rect = pygame.Rect(self.ghost_x, self.ghost_y, self.ghost_image.get_width(), self.ghost_image.get_height())

            ghost_bullet_rects = [bullet for bullet, _ in self.dwarf_bullets] # Если злой гном существует, проверяем столкновения
            collided_indices = ghost_rect.collidelistall(ghost_bullet_rects)

            if collided_indices:
                # self.ghost_image = None  # Убираем злого гнома
                for index in collided_indices: # Удаляем все столкнувшиеся пули
                    del self.dwarf_bullets[index]


        # for bullet, _ in self.dwarf_bullets:
        #     if check_evil_dwarf_rect:
        #         if evil_dwarf_rect.colliderect(bullet):
        #             self.evil_dwarf_image = None  # Убираем злого гнома
        #             self.dwarf_bullets.remove((bullet, _))  # Удаляем пулю из списка
        #             break  # Прерываем цикл после попадания


        # # ________________СТРЕЛЬБА В ЗЛОГО ГНОМА______________________________
        # """Функция перемещения гнома"""
        # self.evil_dwarf_x = evil_dwarf.actions_evil_dwarf(evil_dwarf, size) # Перемещение


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
        for ladder in ladders[self.current_location]:
            black_square = pygame.Surface((ladder.width, ladder.height))

            # Задаем цвет поверхности (черный)
            black_square.fill((0, 0, 0))  # RGB (0, 0, 0) – черный цвет
            screen.blit(black_square, (ladder.x, ladder.y)) # Отображаем платформы

        # Отображение персонажа
        # if self.dwarf_image:
        #     screen.blit(self.dwarf_image, [self.dwarf_x, self.dwarf_y])
        screen.blit(self.dwarf_image, (self.dwarf_x, self.dwarf_y))
        """ОТОБРАЖЕНИЕ GHOST"""
        # Если злой гном существует, рисуем его
        if self.ghost_image and self.current_location == 0:
            screen.blit(self.ghost_image, (self.ghost_x, self.ghost_y))

        # Отображение пуль
        self.dwarf_bullets = dwarf.dwarf_bullets
        for bullet, _ in self.dwarf_bullets:
            screen.blit(self.bullet_image, (bullet.x, bullet.y))  # Отображаем пули

        for bullet, _, _ in self.ghost_bullets:
            screen.blit(self.bullet_image, (bullet.x, bullet.y))  # Отображаем пули

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
            # self.shoot(keys)
            # self.update_bullets(size)
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
    # Обработка косячной картинки
    image = Image.open("media/image_main/platform_1.png")
    image.save("media/image_main/platform_1_fixed.png", icc_profile=None)

    size, screen, floor_y, platforms, background_images, ladders, bounding_box_ghost = initialize_game()

    """Гл персы"""
    dwarf = Dwarf(screen.get_height(), platforms) # Гл. перс 0 lvl

    """Противники"""
    ghost = Ghost(screen.get_height(), screen.get_width()) # Противник 0 lvl

    game_dwarf = GameDwarf(dwarf, ghost)
    game_dwarf.main(size, floor_y)
