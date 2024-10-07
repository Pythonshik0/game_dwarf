import pygame
import os


class Dwarf:
    def __init__(self, screen_height):
        self.dwarf_image = None
        # Начальная позиция персонажа
        self.dwarf_x = 50 # Положение слева
        self.dwarf_y = screen_height - 100 # Вычисляем высоту пола
        self.dwarf_speed = 1  # Скорость перемещения персонажа
        self.dwarf_is_jumping = False
        self.dwarf_jump_speed = 8  # Начальная высота прыжка
        self.dwarf_bullets = [] # Список для хранения пуль

        self.dwarf_bullet_speed = 3 # Скорость пуль

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

    def moving_the_dwarf_LEFT(self, keys, dwarf_x):
        if keys[pygame.K_LEFT]:
            self.dwarf_x = dwarf_x
            self.dwarf_x -= self.dwarf_speed
            self.dwarf_shoot_direction = -1  # Устанавливаем направление стрельбы влево

            # Перемещаем гнома влево и задаем направление стрельбы
            return self.dwarf_x, self.dwarf_shoot_direction

        return dwarf_x, self.dwarf_shoot_direction


    def moving_the_dwarf_RIGHT(self, keys, dwarf_x):
        if keys[pygame.K_RIGHT]:
            self.dwarf_x = dwarf_x
            self.dwarf_x += self.dwarf_speed
            self.dwarf_shoot_direction = 1  # Устанавливаем направление стрельбы влево

            # Перемещаем гнома вправо и задаем направление стрельбы
            return self.dwarf_x, self.dwarf_shoot_direction

        return dwarf_x, self.dwarf_shoot_direction

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
            on_ground = data['dwarf_y'] >= data['floor_y'] - self.dwarf_image.get_height()

            # Проверяем столкновение с платформами
            for platform in data['platforms'][data['current_location']]:
                if character_rect.colliderect(platform) and data['vertical_velocity'] >= 0 and data['dwarf_space']:
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
        if self.dwarf_image:
            if dwarf_x >= size[0] - self.dwarf_image.get_width() and current_location == 0:
                current_location += 1  # Переход на следующую локацию
                dwarf_x = 0  # Персонаж перемещается в начало экрана

            elif dwarf_x <= 0 and current_location == 1:
                evil_dwarf_bullets = [] # Очищаем пули злодея
                dwarf_bullets = []  # Очищаем пули
                current_location = 0  # Возвращаемся на предыдущую локацию
                dwarf_x = size[0] - 50  # Персонаж в конец экрана

            # Ограничиваем движение персонажа в пределах экрана
            dwarf_x = max(0, min(dwarf_x, size[0] - self.dwarf_image.get_width()))

        return dwarf_x, current_location, dwarf_bullets, evil_dwarf_bullets


