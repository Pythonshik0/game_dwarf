import pygame
import os
from PIL import Image
import time

from main_class import Dwarf
from platforms import platforms, background_images

jump_speed = 16  # Начальная скорость прыжка
gravity = 0.9  # Сила гравитации (ускорение падения)
max_fall_speed = 0.9  # Максимальная скорость падения

jump_delay = 0.8  # Задержка между прыжками в секундах
class GameDwarf:
    def __init__(self, dwarf):
        # Инициализация игры
        self.runGame = True

        # Параметры персонажа
        self.dwarf_x = dwarf.dwarf_characteristics()['dwarf_x']  # Положение по оси X
        self.dwarf_y = dwarf.dwarf_characteristics()['dwarf_y']  # Положение по оси Y
        self.dwarf_is_jumping = dwarf.dwarf_characteristics()['dwarf_is_jumping']  # Флаг прыжка
        self.dwarf_shoot_direction = dwarf.dwarf_characteristics()['dwarf_shoot_direction']  # Направление стрельбы
        self.dwarf_space = dwarf.dwarf_characteristics()['dwarf_space']  # Проверка на прыжок
        self.dwarf_image = dwarf.dwarf_characteristics()['dwarf_image']  # Изображение персонажа
        self.dwarf_bullets = dwarf.dwarf_characteristics()['dwarf_bullets']  # Список пуль
        self.dwarf_can_shoot = dwarf.dwarf_characteristics()['dwarf_can_shoot']  # Флаг возможности стрельбы
        self.dwarf_bullet_speed = dwarf.dwarf_characteristics()['dwarf_bullet_speed']  # Скорость пули

        # Общие переменные
        self.vertical_velocity = 0  # Вертикальная скорость
        self.current_location = 0  # Текущая локация
        self.last_jump_time = 0  # Время последнего прыжка

        # Загрузка изображения пули
        self.bullet_image = pygame.image.load('media/image_main/Сфера-1-lvl.png')
        self.bullet_image = pygame.transform.scale(self.bullet_image, (50, 50))  # Масштабируем изображение пули

    def handle_events(self):
        # Обработка событий (закрытие окна)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.runGame = False  # Завершаем игру, если закрыли окно

    def move_dwarf(self, keys):
        # Управление движением персонажа
        current_time = time.time()  # Текущее время в секундах

        if keys[pygame.K_LEFT]:  # Движение влево
            self.dwarf_x, self.dwarf_shoot_direction = dwarf.moving_the_dwarf_LEFT(self.dwarf_x)

        if keys[pygame.K_RIGHT]:  # Движение вправо
            self.dwarf_x, self.dwarf_shoot_direction = dwarf.moving_the_dwarf_RIGHT(self.dwarf_x)

        # Проверка на прыжок: можно прыгать только после задержки
        if keys[pygame.K_UP] and not self.dwarf_is_jumping and (current_time - self.last_jump_time > jump_delay):
            self.dwarf_is_jumping = True  # Устанавливаем флаг прыжка
            self.vertical_velocity -= jump_speed  # Начальная вертикальная скорость при прыжке
            self.dwarf_space = True  # Флаг пространства для прыжка
            self.last_jump_time = current_time  # Обновляем время последнего прыжка

    def apply_gravity(self, floor_y):
        # Применение гравитации и обновление положения персонажа
        if self.dwarf_is_jumping:
            self.dwarf_y += self.vertical_velocity  # Обновляем положение по Y с учётом скорости
            self.vertical_velocity += gravity  # Применяем гравитацию (ускорение)

            # Ограничиваем скорость падения
            if self.vertical_velocity > max_fall_speed:
                self.vertical_velocity = max_fall_speed

        # Проверяем коллизии с платформами и полом
        character_rect = pygame.Rect(self.dwarf_x, self.dwarf_y, self.dwarf_image.get_width(), self.dwarf_image.get_height())
        on_ground = self.dwarf_y >= floor_y - self.dwarf_image.get_height()

        # Проверяем столкновение с платформами
        for platform in platforms[self.current_location]:
            if character_rect.colliderect(platform) and self.vertical_velocity >= 0 and self.dwarf_space:
                self.dwarf_y = platform.top - self.dwarf_image.get_height()  # Корректируем положение на платформе
                self.dwarf_is_jumping = False  # Завершаем прыжок
                self.vertical_velocity = 0  # Останавливаем вертикальную скорость

                break
        else:
            if self.dwarf_y < floor_y - self.dwarf_image.get_height():
                self.dwarf_is_jumping = True  # Продолжаем прыжок, если ещё не на земле

            else:
                self.dwarf_y = floor_y - self.dwarf_image.get_height()  # Останавливаем на земле

                self.dwarf_is_jumping = False  # Завершаем прыжок
                self.vertical_velocity = 0  # Обнуляем скорость
                self.dwarf_space = False  # Персонаж на земле

    def check_boundaries(self, size):
        # Проверка выхода за границы экрана
        if self.dwarf_x >= size[0] - self.dwarf_image.get_width() and self.current_location == 0:
            self.current_location += 1  # Переход на следующую локацию
            self.dwarf_x = 0  # Персонаж перемещается в начало экрана

        elif self.dwarf_x <= 0 and self.current_location == 1:
            self.dwarf_bullets = []  # Очищаем пули
            self.current_location = 0  # Возвращаемся на предыдущую локацию
            self.dwarf_x = size[0] - 50  # Персонаж в конец экрана

        # Ограничиваем движение персонажа в пределах экрана
        self.dwarf_x = max(0, min(self.dwarf_x, size[0] - self.dwarf_image.get_width()))

    def shoot(self, keys):
        # Стрельба персонажа
        if keys[pygame.K_SPACE] and self.dwarf_can_shoot:  # Если нажата пробел и можно стрелять
            bullet_rect = pygame.Rect(self.dwarf_x + self.dwarf_image.get_width() // 2,
                                      self.dwarf_y + self.dwarf_image.get_height() // 2,
                                      self.bullet_image.get_width(),
                                      self.bullet_image.get_height())  # Создаем прямоугольник для пули

            self.dwarf_bullets.append((bullet_rect, self.dwarf_shoot_direction))  # Добавляем пулю в список
            self.dwarf_can_shoot = False  # Запрещаем стрельбу до следующего нажатия

        if not keys[pygame.K_SPACE]:  # Если пробел отпущен
            self.dwarf_can_shoot = True  # Разрешаем стрельбу снова

    def update_bullets(self, size):
        # Обновление положения пуль
        for bullet, direction in self.dwarf_bullets:
            bullet.x += self.dwarf_bullet_speed * direction  # Двигаем пулю в направлении

        # Удаляем пули, которые вышли за экран
        self.dwarf_bullets = [(bullet, direction) for bullet, direction in self.dwarf_bullets if bullet.x > 0 and bullet.x < size[0]]

    def draw(self, screen):
        # Отрисовка элементов игры
        screen.blit(background_images[self.current_location], [0, 0])  # Отображаем фон

        # Отображение платформ
        for platform in platforms[self.current_location]:
            scaled_platform_image = pygame.transform.scale(pygame.image.load('media/image_main/platform_1_fixed.png'), (platform.width, platform.height))  # Масштабируем платформы
            screen.blit(scaled_platform_image, (platform.x, platform.y))  # Отображаем платформы

        # Отображение персонажа
        screen.blit(self.dwarf_image, [self.dwarf_x, self.dwarf_y])

        # Отображение пуль
        for bullet, _ in self.dwarf_bullets:
            screen.blit(self.bullet_image, (bullet.x, bullet.y))  # Отображаем пули

        pygame.display.flip()  # Обновляем экран

    def main(self, size, floor_y):
        while self.runGame:
            self.handle_events()
            keys = pygame.key.get_pressed()
            self.move_dwarf(keys)
            self.apply_gravity(floor_y)
            self.check_boundaries(size)
            self.shoot(keys)
            self.update_bullets(size)
            self.draw(screen)

        pygame.quit()


def initialize_game():
    pygame.init()
    os.environ['SDL_VIDEO_WINDOW_POS'] = "100,100"

    screen_info = pygame.display.Info()
    screen_width = screen_info.current_w
    screen_height = screen_info.current_h

    size = (screen_width, screen_height)
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)
    pygame.display.set_caption("DWARF")

    floor_y = screen_height - 60
    platforms_list = platforms(screen_width, screen_height)
    background_images_list = background_images(size)

    return size, screen, floor_y, platforms_list, background_images_list


if __name__ == "__main__":
    # Обработка косячной картинки
    image = Image.open("media/image_main/platform_1.png")
    image.save("media/image_main/platform_1_fixed.png", icc_profile=None)

    size, screen, floor_y, platforms, background_images = initialize_game()
    dwarf = Dwarf(screen.get_height())
    game_dwarf = GameDwarf(dwarf)
    game_dwarf.main(size, floor_y)
