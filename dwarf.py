import pygame
import os


class Dwarf:
    def __init__(self, screen_height, platforms):
        self.dwarf_image = None

        # Начальная позиция персонажа
        self.dwarf_x = 70 # Положение слева
        self.dwarf_y = screen_height # Вычисляем высоту пола
        self.dwarf_speed = 0.6  # Скорость перемещения персонажа
        self.dwarf_is_jumping = False
        self.dwarf_jump_speed = 12  # Начальная скорость прыжка
        self.dwarf_bullets = [] # Список для хранения пуль

        self.dwarf_bullet_speed = 1 # Скорость пуль

        self.dwarf_can_shoot = True # Флаг для проверки, можно ли стрелять
        self.dwarf_space = True # Проверка на пыжок

        self.platforms = platforms # Платформы
        # Загрузка частей персонажа
        self.leg_image = pygame.image.load("media/image_main/нога.png").convert_alpha()
        self.head_image = pygame.image.load("media/image_main/голова.png").convert_alpha()
        self.body_image = pygame.image.load("media/image_main/туловище.png").convert_alpha()
        self.arm_image = pygame.image.load("media/image_main/рука.png").convert_alpha()

        # Сохранение размеров частей
        self.leg_width, self.leg_height = self.leg_image.get_size()
        self.head_width, self.head_height = self.head_image.get_size()
        self.body_width, self.body_height = self.body_image.get_size()
        self.arm_width, self.arm_height = self.arm_image.get_size()

        # Создание единого изображения персонажа
        self.create_dwarf_image()

    def create_dwarf_image(self):
        """Создание единого изображения персонажа из частей."""
        extra_space_for_arms = self.arm_width

        # Рассчитываем общие размеры персонажа
        dwarf_width = (max(self.head_width, self.body_width, self.leg_width) + 2 * extra_space_for_arms)  # Добавляем место для рук
        dwarf_height = self.head_height + self.body_height + self.leg_height  # Высота персонажа

        # Создаем пустое изображение для персонажа
        self.dwarf_image = pygame.Surface((dwarf_width, dwarf_height), pygame.SRCALPHA)

        # Рассчитываем координаты для каждой части
        leg_y = dwarf_height - self.leg_height
        body_y = leg_y - self.body_height
        head_y = body_y - self.head_height
        arm_y = body_y   # Рука чуть выше туловища

        # Координаты для рук
        arm_x_left = 5  # Левая рука будет в самой левой части изображения
        arm_x_right = dwarf_width - self.arm_width - 5 # Правая рука будет в правой части изображения

        # Отзеркаливание правой руки
        self.right_arm_flipped = pygame.transform.flip(self.arm_image, True, False)  # Отзеркалить по горизонтали

        # Отрисовка частей персонажа на общем изображении
        self.dwarf_image.blit(self.leg_image, (extra_space_for_arms, leg_y))  # Ноги
        self.dwarf_image.blit(self.leg_image, (extra_space_for_arms + 10, leg_y))  # Ноги
        self.dwarf_image.blit(self.body_image, (extra_space_for_arms, body_y))  # Туловище
        self.dwarf_image.blit(self.head_image, (extra_space_for_arms, head_y))  # Голова

        # Отрисовка двух рук: левой и правой
        self.dwarf_image.blit(self.arm_image, (arm_x_left, arm_y))  # Левая рука
        self.dwarf_image.blit(self.right_arm_flipped, (arm_x_right, arm_y))  # Правая рука


    def dwarf_characteristics(self):
        # Загрузка спрайта персонажа
        # dwarf = pygame.image.load("media/image_main/dworf.png").convert_alpha()

        # Задание нового размера персонажа (например, 100x100 пикселей)
        self.dwarf_image = pygame.transform.scale(self.dwarf_image, (120, 150))
        data = {
            'dwarf_image': self.dwarf_image, # Задание нового размера персонажа
            'dwarf_x': self.dwarf_x, # Положение слева
            'dwarf_y': self.dwarf_y, # Положение над полом
            'character_speed': self.dwarf_speed, # Скорость перемещения персонажа
            'dwarf_is_jumping': self.dwarf_is_jumping, # Проверка на нажатый пробел
            'jump_speed': self.dwarf_jump_speed, # Начальная высота прыжка
            'dwarf_bullets': self.dwarf_bullets, # Список для хранения пуль
            'dwarf_bullet_speed': self.dwarf_bullet_speed, # Скорость пуль
            'dwarf_can_shoot': self.dwarf_can_shoot,
            'dwarf_space': self.dwarf_space,
        }
        return data

    def moving_the_dwarf_LEFT(self, keys, dwarf_x):
        if keys[pygame.K_LEFT]:
            self.dwarf_x = dwarf_x
            self.dwarf_x -= self.dwarf_speed

            # Перемещаем гнома влево и задаем направление стрельбы
            return self.dwarf_x

        return dwarf_x


    def moving_the_dwarf_RIGHT(self, keys, dwarf_x):
        if keys[pygame.K_RIGHT]:
            self.dwarf_x = dwarf_x
            self.dwarf_x += self.dwarf_speed

            # Перемещаем гнома вправо и задаем направление стрельбы
            return self.dwarf_x

        return dwarf_x

    def dwarf_is_jumping_K_UP(self, dwarf_is_jumping, keys, vertical_velocity, current_time, jump_delay, jump_speed, last_jump_time):
        # Проверка на прыжок: можно прыгать только после задержки
        if keys[pygame.K_UP] and not dwarf_is_jumping and (current_time - last_jump_time > jump_delay):
            self.dwarf_is_jumping = True  # Устанавливаем флаг прыжка
            vertical_velocity -= jump_speed  # Начальная вертикальная скорость при прыжке
            self.dwarf_space = True  # Флаг пространства для прыжка
            last_jump_time = current_time  # Обновляем время последнего прыжка

            return self.dwarf_is_jumping, vertical_velocity, self.dwarf_space, last_jump_time

        return dwarf_is_jumping, vertical_velocity, self.dwarf_space, last_jump_time

    def dwarf_apply_gravity(self, data):
        # Применение гравитации и обновление положения персонажа
        if data['dwarf_is_jumping']:
            data['dwarf_y'] += data['vertical_velocity']  # Обновляем положение по Y с учётом скорости
            data['vertical_velocity'] += data['gravity']  # Применяем гравитацию (ускорение)

            # Ограничиваем скорость падения
            if data['vertical_velocity'] > data['max_fall_speed']:
                data['vertical_velocity'] = data['max_fall_speed']

        # Проверяем коллизии с платформами и полом
        if self.dwarf_image:
            character_rect = pygame.Rect(data['dwarf_x'], data['dwarf_y'], self.dwarf_image.get_width(), self.dwarf_image.get_height())

            # Проверяем столкновение с платформами
            for platform in self.platforms[data['current_location']]:
                if (character_rect.colliderect(platform)) and \
                   (data['vertical_velocity'] >= 0) and \
                   (character_rect.bottom <= platform.top + 10) and \
                   (platform.bottom > character_rect.bottom) and \
                   (character_rect.bottom > platform.top): # Проверка, что персонаж сверху платформы

                    data['dwarf_y'] = platform.top - self.dwarf_image.get_height()  # Корректируем положение на платформе
                    data['dwarf_is_jumping'] = False  # Завершаем прыжок
                    data['vertical_velocity'] = 0  # Останавливаем вертикальную скорость
                    break
            else:
                if data['dwarf_y'] < data['floor_y'] - self.dwarf_image.get_height():
                    data['dwarf_is_jumping'] = True  # Продолжаем прыжок, если ещё не на земле
                else:
                    data['dwarf_y'] = data['floor_y'] - self.dwarf_image.get_height()  # Останавливаем на земле
                    data['dwarf_is_jumping'] = False  # Завершаем прыжок
                    data['vertical_velocity'] = 0  # Обнуляем скорость
                    data['dwarf_space'] = False  # Персонаж на земле

        return data['dwarf_space'], data['vertical_velocity'], data['dwarf_is_jumping'], data['dwarf_y'], data['dwarf_x']

    def dwarf_check_boundaries(self, size, current_location, dwarf_x, dwarf_bullets, evil_dwarf_bullets):
        # Проверка выхода за границы экрана
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
        dwarf_x = max(0, min(dwarf_x, size[0] - self.dwarf_image.get_width()))

        return dwarf_x, current_location, dwarf_bullets, evil_dwarf_bullets

    def move_ladders(self, data):
        for ladder in data['ladders'][data['current_location']]:
            if data['character_rect'].colliderect(ladder):
                data['vertical_velocity'] = 0 # Останавливаем вертикальное движение
                if data['keys'][pygame.K_DOWN]: # Спуск вниз
                    data['dwarf_y'] += 1
                elif data['keys'][pygame.K_UP]: # Подъем вверх
                    data['dwarf_y'] -= 1

        return data['vertical_velocity'], data['dwarf_y']

    def collision_platform(self, data):
        dwarf_bullet_rects = [bullet for bullet, _ in data['dwarf_bullets']]

        for platform in self.platforms[data['current_location']]:
            collided_indices = platform.collidelistall(dwarf_bullet_rects)
            if collided_indices:
                for index in collided_indices:  # Удаляем все столкнувшиеся пули
                    del data['dwarf_bullets'][index]

        return data['dwarf_bullets']

