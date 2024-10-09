import pygame
import os
from PIL import Image
import time

from main_class import TheEvilDwarf
from dwarf import Dwarf
from platforms import platforms, background_images, ladders, StaticObject

jump_speed = 16  # Начальная скорость прыжка
gravity = 0.9  # Сила гравитации (ускорение падения)
max_fall_speed = 0.9  # Максимальная скорость падения

jump_delay = 0.8  # Задержка между прыжками в секундах
shot_delay = 0.5


class GameDwarf:
    def __init__(self, dwarf, evil_dwarf):
        # Инициализация игры
        self.runGame = True

        # Параметры персонажа
        self.dwarf_x = dwarf.dwarf_characteristics()['dwarf_x']  # Положение по оси X
        self.dwarf_y = dwarf.dwarf_characteristics()['dwarf_y']  # Положение по оси Y
        self.dwarf_is_jumping = dwarf.dwarf_characteristics()['dwarf_is_jumping']  # Флаг прыжка
        self.dwarf_space = dwarf.dwarf_characteristics()['dwarf_space']  # Проверка на прыжок
        self.dwarf_image = dwarf.dwarf_characteristics()['dwarf_image']  # Изображение персонажа
        self.dwarf_bullets = dwarf.dwarf_characteristics()['dwarf_bullets']  # Список пуль
        self.dwarf_can_shoot = dwarf.dwarf_characteristics()['dwarf_can_shoot']  # Флаг возможности стрельбы
        self.dwarf_bullet_speed = dwarf.dwarf_characteristics()['dwarf_bullet_speed']  # Скорость пули

        # Стрельбы перса
        self.dwarf_can_shoot_DUBLE = True

        # Злодеи 0 lvl
        self.evil_dwarf_timer_shot = 0  # Таймер выстрела
        self.evil_dwarf_bullets = [] # Выстрелы злодея
        self.evil_dwarf_image = evil_dwarf.evil_dwarf_characteristics()['evil_dwarf_image']  # Изображение персонажа
        self.evil_dwarf_x = evil_dwarf.evil_dwarf_characteristics()['evil_dwarf_x']
        self.evil_dwarf_y = evil_dwarf.evil_dwarf_characteristics()['evil_dwarf_y']

        # Общие переменные
        self.vertical_velocity = 0  # Вертикальная скорость
        self.current_location = 0  # Текущая локация
        self.last_jump_time = 0  # Время последнего прыжка

        # Загрузка изображения пули
        self.bullet_image = pygame.image.load('media/image_main/Сфера-1-lvl.png')
        self.bullet_image = pygame.transform.scale(self.bullet_image, (30, 30))  # Масштабируем изображение пули

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

    def dwarf(self, keys, jump_delay, floor_y, size):
        """Управление движением персонажа (гл. герой)"""
        current_time = time.time()  # Текущее время в секундах
        character_rect = pygame.Rect(self.dwarf_x, self.dwarf_y, self.dwarf_image.get_width(), self.dwarf_image.get_height())

        """ДВИЖЕНИЕ ПО ЛЕСТНИЦЕ"""
        self.vertical_velocity, self.dwarf_y = dwarf.move_ladders(data={
            'dwarf_y': self.dwarf_y, 'ladders': ladders, 'current_location': self.current_location, 'character_rect': character_rect, 'vertical_velocity': self.vertical_velocity, 'keys': keys
        })

        """ПЕРЕХОД НА СЛЕДУЮЩИЙ УРОВЕНЬ (ДВЕРЬ)"""
        if character_rect.colliderect(self.door):
            pass

        """ДВИЖЕНИЕ DWARF"""
        self.dwarf_x = dwarf.moving_the_dwarf_LEFT(keys, self.dwarf_x) # Движение влево
        self.dwarf_x = dwarf.moving_the_dwarf_RIGHT(keys, self.dwarf_x) # Движение вправо

        """ПРЫЖОК DWARF"""
        self.dwarf_is_jumping, self.vertical_velocity, self.dwarf_space, self.last_jump_time = dwarf.dwarf_is_jumping_K_UP(
            self.dwarf_is_jumping, keys, self.vertical_velocity, current_time, jump_delay, jump_speed, self.last_jump_time
        )

        """ГРАВИТАЦИЯ И ОБНОВЛЕНИЕ ПЕРСОНАЖА НА КАРТЕ"""
        self.dwarf_space, self.vertical_velocity, self.dwarf_is_jumping, self.dwarf_y, self.dwarf_x = dwarf.dwarf_apply_gravity(data={
            'dwarf_space': self.dwarf_space, 'dwarf_is_jumping': self.dwarf_is_jumping, 'dwarf_y': self.dwarf_y,
            'dwarf_x': self.dwarf_x, 'floor_y': floor_y, 'vertical_velocity': self.vertical_velocity,
            'gravity': gravity, 'max_fall_speed': max_fall_speed, 'current_location': self.current_location, 'platforms': platforms
        })

        """ВЫХОД НА ЗА ГРАНИЦЫ ЭКРАНА И СМЕНА УРОВНЯ"""
        self.dwarf_x, self.current_location, self.dwarf_bullets, self.evil_dwarf_bullets = dwarf.dwarf_check_boundaries(
            size, self.current_location, self.dwarf_x, self.dwarf_bullets, self.evil_dwarf_bullets
        )

    def shoot(self, keys):
        """Стрельба с учетом времени задержки между выстрелами"""
        current_time = time.time()
        # Если прошла задержка, то стреляем
        if current_time - self.evil_dwarf_timer_shot >= 0.2:
            if keys[pygame.K_w] and keys[pygame.K_a]:
                self._shoot('w-a')
            elif keys[pygame.K_w] and keys[pygame.K_d]:
                self._shoot('w-d')
            elif keys[pygame.K_s] and keys[pygame.K_a]:
                self._shoot('s-a')
            elif keys[pygame.K_s] and keys[pygame.K_d]:
                self._shoot('s-d')
            elif keys[pygame.K_w]:
                self._shoot('w')
            elif keys[pygame.K_s]:
                self._shoot('s')
            elif keys[pygame.K_a]:
                self._shoot('a')
            elif keys[pygame.K_d]:
                self._shoot('d')

            self.evil_dwarf_timer_shot = current_time  # Обновляем таймер после выстрела

        # Стрельба в перса (если существует злой гном)
        if self.evil_dwarf_image:
            self._check_for_dwarf_collision()

    def _shoot(self, direction):
        """Создание пули и добавление ее в список"""
        bullet_rect = pygame.Rect(self.dwarf_x + self.dwarf_image.get_width() // 2,
                                  self.dwarf_y + self.dwarf_image.get_height() // 2,
                                  self.bullet_image.get_width(),
                                  self.bullet_image.get_height())  # Создаем прямоугольник для пули
        self.dwarf_bullets.append((bullet_rect, direction))

    def _check_for_dwarf_collision(self):
        """Проверка на столкновение с выстрелом злого гнома"""
        check_dwarf_rect = False
        if self.dwarf_image:
            dwarf_rect = pygame.Rect(self.dwarf_x, self.dwarf_y, self.dwarf_image.get_width(), self.dwarf_image.get_height())
            check_dwarf_rect = True

        for bullet, _ in self.evil_dwarf_bullets:
            if check_dwarf_rect and dwarf_rect.colliderect(bullet):
                self.dwarf_image = None  # Убираем гнома
                break  # Прерываем цикл после попадания

    def update_bullets(self, size):
        """Обновление положения пуль и удаление пуль, которые вышли за экран"""
        directions = {
            'w-d': (1, -1),
            'w-a': (-1, -1),
            's-d': (1, 1),
            's-a': (-1, 1),
            'w': (0, -1),
            's': (0, 1),
            'a': (-1, 0),
            'd': (1, 0)
        }
        # Обновление пуль
        for bullet, keyboard in self.dwarf_bullets:
            dx, dy = directions.get(keyboard, (0, 0))
            bullet.x += self.dwarf_bullet_speed * dx
            bullet.y += self.dwarf_bullet_speed * dy

        # Удаляем пули, которые вышли за экран
        self.dwarf_bullets = [(bullet, keyboard) for bullet, keyboard in self.dwarf_bullets if 0 < bullet.x < size[0] and 0 < bullet.y < size[1]]

    def evil_dwarf_main(self):
        # """Функция ЗЛОГО ГНОМА (ПРОТИВНИКА)"""
        #
        # # ____________ВЕДЕМ ОГОНЬ ПО ГЛ ГЕРОЮ__________________________________
        # # Проверяем расстояние до главного героя
        # distance_x = self.dwarf_x - self.evil_dwarf_x
        # shot_timer = time.time()  # Текущее время в секундах
        # if self.current_location == 0 and self.evil_dwarf_image and abs(distance_x) < 400 and (shot_timer - self.evil_dwarf_timer_shot > shot_delay):  # Если герой близко, создаем пулю
        #     # Создаем пулю на уровне злого гнома
        #     EVIL_bullet_rect = pygame.Rect(self.evil_dwarf_x + self.evil_dwarf_image.get_width() // 2,
        #                                    self.evil_dwarf_y + self.evil_dwarf_image.get_height() // 2,
        #                                    self.bullet_image.get_width(),
        #                                    self.bullet_image.get_height())  # Создаем прямоугольник для пули
        #
        #     # Определяем направление стрельбы
        #     direction = 1 if distance_x > 0 else -1  # Если герой слева, стреляем влево, иначе вправо
        #     self.evil_dwarf_bullets.append((EVIL_bullet_rect, direction))  # Добавляем пулю в список
        #     self.evil_dwarf_timer_shot = shot_timer
        #
        # # Обновление положения пуль злого гнома
        # if self.current_location == 0:
        #     for bullet, direction in self.evil_dwarf_bullets:
        #         bullet.x += 1 * direction  # Двигаем пулю в направлении
        #
        #     # Удаляем пули, которые вышли за экран
        #     self.evil_dwarf_bullets = [(bullet, direction) for bullet, direction in self.evil_dwarf_bullets if 0 < bullet.x < size[0]]
        # else:
        #     self.evil_dwarf_bullets = []
        #
        #
        # # ________________СТРЕЛЬБА В ЗЛОГО ГНОМА______________________________
        check_evil_dwarf_rect = False
        if self.evil_dwarf_image:
            evil_dwarf_rect = pygame.Rect(self.evil_dwarf_x, self.evil_dwarf_y, self.evil_dwarf_image.get_width(), self.evil_dwarf_image.get_height())
            check_evil_dwarf_rect = True

            # Если злой гном существует, проверяем столкновения
            dwarf_bullet_rects = [bullet for bullet, _ in self.dwarf_bullets]
            collided_indices = evil_dwarf_rect.collidelistall(dwarf_bullet_rects)
            if collided_indices:
                self.evil_dwarf_image = None  # Убираем злого гнома
                # Удаляем все столкнувшиеся пули
                for index in sorted(collided_indices, reverse=True):
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

        # Отображаем лестницу на 0 уровне
        # for ladder in ladders[self.current_location]:
        #     black_square = pygame.Surface((ladder.width, ladder.height))
        #
        #     # Задаем цвет поверхности (черный)
        #     black_square.fill((0, 0, 0))  # RGB (0, 0, 0) – черный цвет
        #     screen.blit(black_square, (ladder.x, ladder.y)) # Отображаем платформы

        # Отображение персонажа
        if self.dwarf_image:
            screen.blit(self.dwarf_image, [self.dwarf_x, self.dwarf_y])

        """ОТОБРАЖЕНИЕ EVIL DWARF"""
        # Если злой гном существует, рисуем его
        if self.evil_dwarf_image and self.current_location == 0:
            screen.blit(self.evil_dwarf_image, (self.evil_dwarf_x, self.evil_dwarf_y))


        # Отображение пуль
        for bullet, _ in self.dwarf_bullets:
            screen.blit(self.bullet_image, (bullet.x, bullet.y))  # Отображаем пули

        for bullet, _ in self.evil_dwarf_bullets:
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
            self.dwarf(keys, jump_delay, floor_y, size) # Функция работы гл героя
            self.evil_dwarf_main()
            self.shoot(keys)
            self.update_bullets(size)
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

    ladders_list = ladders(screen_width, screen_height)

    return size, screen, floor_y, platforms_list, background_images_list, ladders_list


if __name__ == "__main__":
    # Обработка косячной картинки
    image = Image.open("media/image_main/platform_1.png")
    image.save("media/image_main/platform_1_fixed.png", icc_profile=None)

    size, screen, floor_y, platforms, background_images, ladders = initialize_game()

    """Гл персы"""
    dwarf = Dwarf(screen.get_height()) # Гл. перс 0 lvl

    """Противники"""
    evil_dwarf = TheEvilDwarf(screen.get_height()) # Противник 0 lvl


    game_dwarf = GameDwarf(dwarf, evil_dwarf)
    game_dwarf.main(size, floor_y)
