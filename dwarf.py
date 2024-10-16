import pygame
import os
import time

from PIL import Image


class Dwarf:
    def __init__(self, screen_height, platforms):
        self.dwarf_image = None
        self.ghost_bullets = None # Пульки призрака

        # Начальная позиция персонажа
        self.dwarf_x = 70 # Положение слева
        self.dwarf_y = screen_height # Вычисляем высоту пола
        self.dwarf_speed = 3  # Скорость перемещения персонажа
        self.dwarf_is_jumping = False
        self.dwarf_jump_speed = 23  # Начальная скорость прыжка
        self.dwarf_bullets = [] # Список для хранения пуль
        self.vertical_velocity = 0  # Вертикальная скорость
        self.last_jump_time = 0  # Время последнего прыжка
        self.dwarf_bullet_speed = 5 # Скорость пуль
        self.gravity = 2.7  # Сила гравитации (ускорение падения)
        self.max_fall_speed = 2.7  # Максимальная скорость падения
        self.timer_shot = 0  # Таймер выстрела
        self.jump_delay = 0.8  # Задержка между прыжками в секундах

        self.breath_images = {
            'worth': [
                pygame.image.load("media/image_main/Стоит-на-месте.png"),
                pygame.image.load("media/image_main/Стоит-на-месте-1.png"),
                pygame.image.load("media/image_main/Стоит-на-месте-2.png"),
            ],
            'goes_right': [
                pygame.image.load("media/image_main/Идет-1.png"),
                pygame.image.load("media/image_main/Идет-2.png"),
                pygame.image.load("media/image_main/Идет-3.png"),
            ],
            'goes_left': [
                pygame.image.load("media/image_main/Идет-лево-1.png"),
                pygame.image.load("media/image_main/Идет-лево-2.png"),
                pygame.image.load("media/image_main/Идет-лево-3.png"),
            ]
        }

        # Масштабируем изображения под нужный размер (например, 120x150)
        self.dwarf_image = [pygame.transform.scale(img, (100, 150)) for img in self.breath_images['worth']]
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()

        # Загрузка изображения пули
        self.bullet_image = pygame.image.load('media/image_main/Сфера-1-lvl.png')
        self.bullet_image = pygame.transform.scale(self.bullet_image, (30, 30))  # Масштабируем изображение пули

        self.dwarf_can_shoot = True # Флаг для проверки, можно ли стрелять
        self.dwarf_space = True # Проверка на прыжок
        self.platforms = platforms # Платформы

        self.check_K_DOWN = False

    def gif_dwarf(self, now):
        """Создание движения картинки"""
        frame_delay = 200
        if now - self.last_update > frame_delay:
            self.current_frame = (self.current_frame + 1) % len(self.dwarf_image) # Переход к следующему кадру если взять последний кадр по счету
            self.last_update = now  # Обновляем время последнего обновления

    def dwarf_screen(self, screen):
        """Вывод персонажа на экран"""
        screen.blit(self.dwarf_image[self.current_frame], (self.dwarf_x, self.dwarf_y))

    def dwarf_rect(self):
        """rect dwarf"""
        current_image = self.dwarf_image[self.current_frame]  # Получаем текущее изображение
        dwarf_rect = pygame.Rect(self.dwarf_x, self.dwarf_y, current_image.get_width(), current_image.get_height())
        return dwarf_rect

    def moving_the_dwarf(self, keys):
        """Перемещение гнома влево или вправо и смена изображения"""
        if keys[pygame.K_RIGHT] and not keys[pygame.K_DOWN]:
            self.dwarf_image = [pygame.transform.scale(img, (100, 150)) for img in self.breath_images['goes_right']]
            self.dwarf_x += self.dwarf_speed

            if self.check_K_DOWN:
                self.dwarf_y -= 80
                self.check_K_DOWN = False


        elif keys[pygame.K_LEFT] and not keys[pygame.K_DOWN]:
            self.dwarf_image = [pygame.transform.scale(img, (100, 150)) for img in self.breath_images['goes_left']]
            self.dwarf_x -= self.dwarf_speed

            if self.check_K_DOWN:
                self.dwarf_y -= 80
                self.check_K_DOWN = False

        elif keys[pygame.K_DOWN]:
            self.dwarf_image = [pygame.transform.scale(img, (100, 70)) for img in self.breath_images['worth']]

            if self.check_K_DOWN is False:
                print('Тут')
                # self.dwarf_y += 80
                self.check_K_DOWN = True
        else:
            if self.check_K_DOWN:
                self.dwarf_y -= 80

            self.check_K_DOWN = False
            # Если ни одна из клавиш не нажата, отображаем анимацию "стоит на месте"
            self.dwarf_image = [pygame.transform.scale(img, (100, 150)) for img in self.breath_images['worth']]


    def dwarf_is_jumping_K_UP(self, keys):
        """Проверка на прыжок: можно прыгать только после задержки"""
        current_time = time.time()
        if keys[pygame.K_UP] and not self.dwarf_is_jumping and (current_time - self.last_jump_time > self.jump_delay):
            self.dwarf_is_jumping = True  # Устанавливаем флаг прыжка
            self.vertical_velocity -= self.dwarf_jump_speed  # Начальная вертикальная скорость при прыжке
            self.dwarf_space = True  # Флаг пространства для прыжка
            self.last_jump_time = current_time  # Обновляем время последнего прыжка

    def contact_trap_update_x_or_y(self, update_dwarf_x, update_dwarf_y):
        """Функция для смены положения персонажа при соприкосновении с stone trap"""
        if self.dwarf_x > update_dwarf_x:
            self.dwarf_x -= 3
            self.dwarf_y -= 3

        elif self.dwarf_x < update_dwarf_x:
            self.dwarf_x += 3
            self.dwarf_y -= 3

    def dwarf_apply_gravity(self, floor_y, current_location, platforms):
        """Применение гравитации и обновление положения персонажа"""
        if self.dwarf_is_jumping:
            self.dwarf_y += self.vertical_velocity # Обновляем положение по Y с учётом скорости
            self.vertical_velocity += self.gravity  # Применяем гравитацию (ускорение)

            # Ограничиваем скорость падения
            if self.vertical_velocity > self.max_fall_speed:
                self.vertical_velocity = self.max_fall_speed

        # Проверяем коллизии с платформами и полом
        if self.dwarf_image:
            character_rect = self.dwarf_rect()

            # Проверяем столкновение с платформами
            for platform in platforms[current_location]:
                if (character_rect.colliderect(platform)) and \
                   (self.vertical_velocity >= 0) and \
                   (character_rect.bottom <= platform.top + 10) and \
                   (platform.bottom > character_rect.bottom) and \
                   (character_rect.bottom > platform.top): # Проверка, что персонаж сверху платформы

                    self.dwarf_y = platform.top - self.dwarf_image[self.current_frame].get_height()  # Корректируем положение на платформе
                    self.dwarf_is_jumping = False  # Завершаем прыжок
                    self.vertical_velocity = 0  # Останавливаем вертикальную скорость
                    break
            else:
                if self.dwarf_y < floor_y - self.dwarf_image[self.current_frame].get_height():
                    self.dwarf_is_jumping = True  # Продолжаем прыжок, если ещё не на земле
                else:
                    self.dwarf_y = floor_y - self.dwarf_image[self.current_frame].get_height()  # Останавливаем на земле
                    self.dwarf_is_jumping = False  # Завершаем прыжок
                    self.vertical_velocity = 0  # Обнуляем скорость
                    self.dwarf_space = False  # Персонаж на земле

    def dwarf_check_boundaries(self, size, current_location):
        """Проверка выхода за границы экрана и смена уровня"""
        # if self.dwarf_image:
        #     if dwarf_x >= size[0] - self.dwarf_image.get_width() and current_location == 0:
        #         current_location += 1  # Переход на следующую локацию
        #         dwarf_x = 0  # Персонаж перемещается в начало экрана
        #
        #     elif dwarf_x <= 0 and current_location == 1:
        #         evil_dwarf_bullets = [] # Очищаем пули злодея
        #         dwarf_bullets = []  # Очищаем пули
        #         current_location = 0  # Возвращаемся на предыдущую локацию
        #         dwarf_x = size[0] - 50  # Персонаж в конец экрана

        # Ограничиваем движение персонажа в пределах экрана
        self.dwarf_x = max(0, min(self.dwarf_x, size[0] - self.dwarf_image[self.current_frame].get_width()))

        return self.dwarf_x, current_location

    def move_ladders(self, ladders, keys, current_location):
        """Движение по лестнице"""
        rect = self.dwarf_rect()
        for ladder in ladders[current_location]:
            if rect.colliderect(ladder):
                self.vertical_velocity = 0 # Останавливаем вертикальное движение
                if keys[pygame.K_DOWN]: # Спуск вниз
                    self.dwarf_y += 5
                elif keys[pygame.K_UP]: # Подъем вверх
                    self.dwarf_y -= 5

    def collision_platform(self, current_location, platforms, ghost_rect):
        """Удаление пулек при попадании в платформу или врагов"""
        dwarf_bullet_rects = [bullet for bullet, _ in self.dwarf_bullets]

        for platform in platforms[current_location]:
            collided_indices = platform.collidelistall(dwarf_bullet_rects)
            if collided_indices:
                for index in collided_indices: # Удаляем все столкнувшиеся пули
                    del self.dwarf_bullets[index]

        # ________________Стрельба в GHOST главным героем______________________________
        collided_indices_ghost = ghost_rect.collidelistall(dwarf_bullet_rects)
        if collided_indices_ghost:
            for index in collided_indices_ghost:  # Удаляем все столкнувшиеся пули
                del self.dwarf_bullets[index]

    def shoot(self, keys, ghost_image, ghost_bullets): # СТРЕЛЬБА ГЛ. ГЕРОЯ
        """Стрельба с учетом времени задержки между выстрелами"""
        current_time = time.time()
        self.ghost_bullets = ghost_bullets
        # Если прошла задержка, то стреляем
        if current_time - self.timer_shot >= 0.2:
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

            self.timer_shot = current_time  # Обновляем таймер после выстрела

        # Стрельба в перса (если существует злой гном)
        if ghost_image:
            self._check_for_dwarf_collision()

    def _shoot(self, direction): # СТРЕЛЬБА ГЛ. ГЕРОЯ
        """Создание пули и добавление ее в список"""
        bullet_rect = pygame.Rect(self.dwarf_x + self.dwarf_image[self.current_frame].get_height() // 2,
                                  self.dwarf_y + self.dwarf_image[self.current_frame].get_height() // 2,
                                  self.bullet_image.get_width(),
                                  self.bullet_image.get_height())  # Создаем прямоугольник для пули
        self.dwarf_bullets.append((bullet_rect, direction))

    def _check_for_dwarf_collision(self): # СТРЕЛЬБА В ГЛ. ГЕРОЯ
        """Проверка на столкновение с выстрелом ЗЛОДЕЕВ"""
        if self.dwarf_image:
            dwarf = self.dwarf_rect()

            for bullet, _, _ in self.ghost_bullets:
                if dwarf.colliderect(bullet):
                    # self.dwarf_image = None  # Убираем гнома
                    break  # Прерываем цикл после попадания

    def update_bullets(self, size): # СТРЕЛЬБА ГЛ. ГЕРОЯ
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

    def door_next_level(self, door):
        """Переход на след уровень (Дверь)"""
        dwarf_rect = self.dwarf_rect()
        if dwarf_rect.colliderect(door):  # ПЕРЕХОД НА СЛЕДУЮЩИЙ УРОВЕНЬ (ДВЕРЬ)
            pass