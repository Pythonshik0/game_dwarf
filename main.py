import pygame
import os
from main_class import Dwarf
from platforms import platforms, background_images

jump_speed = 8  # Начальная скорость прыжка
gravity = 0.35  # Сила гравитации (ускорение падения)
max_fall_speed = 0.4  # Максимальная скорость падения


class GameDwarf:
    def __init__(self, dwarf):
        self.runGame = True

        self.dwarf_x = dwarf.dwarf_characteristics()['dwarf_x']
        self.dwarf_y = dwarf.dwarf_characteristics()['dwarf_y']
        self.dwarf_is_jumping = dwarf.dwarf_characteristics()['dwarf_is_jumping']
        self.dwarf_shoot_direction = dwarf.dwarf_characteristics()['dwarf_shoot_direction']
        self.dwarf_space = dwarf.dwarf_characteristics()['dwarf_space']
        self.dwarf_image = dwarf.dwarf_characteristics()['dwarf_image']
        self.dwarf_bullets = dwarf.dwarf_characteristics()['dwarf_bullets']
        self.dwarf_can_shoot = dwarf.dwarf_characteristics()['dwarf_can_shoot']
        self.dwarf_bullet_speed = dwarf.dwarf_characteristics()['dwarf_bullet_speed']

        # Общие переменные
        self.vertical_velocity = 0
        self.current_location = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.runGame = False

    def move_dwarf(self, keys):
        if keys[pygame.K_LEFT]:
            self.dwarf_x, self.dwarf_shoot_direction = dwarf.moving_the_dwarf_LEFT(self.dwarf_x)

        if keys[pygame.K_RIGHT]:
            self.dwarf_x, self.dwarf_shoot_direction = dwarf.moving_the_dwarf_RIGHT(self.dwarf_x)

        if keys[pygame.K_UP] and not self.dwarf_is_jumping:
            self.dwarf_is_jumping = True
            self.vertical_velocity -= jump_speed
            self.dwarf_space = True

    def apply_gravity(self, floor_y):
        if self.dwarf_is_jumping:
            self.dwarf_y += self.vertical_velocity
            self.vertical_velocity += gravity

            if self.vertical_velocity > max_fall_speed:
                self.vertical_velocity = max_fall_speed

        character_rect = pygame.Rect(self.dwarf_x, self.dwarf_y, self.dwarf_image.get_width(), self.dwarf_image.get_height())
        on_ground = self.dwarf_y >= floor_y - self.dwarf_image.get_height()

        for platform in platforms[self.current_location]:
            if character_rect.colliderect(platform) and self.vertical_velocity >= 0 and self.dwarf_space:
                self.dwarf_y = platform.top - self.dwarf_image.get_height()
                self.dwarf_is_jumping = False
                self.vertical_velocity = 0
                break
        else:
            if self.dwarf_y < floor_y - self.dwarf_image.get_height():
                self.dwarf_is_jumping = True
            else:
                self.dwarf_y = floor_y - self.dwarf_image.get_height()
                self.dwarf_is_jumping = False
                self.vertical_velocity = 0
                self.dwarf_space = False

    def check_boundaries(self, size):
        if self.dwarf_x >= size[0] - self.dwarf_image.get_width() and self.current_location == 0:
            self.current_location += 1
            self.dwarf_x = 0

        elif self.dwarf_x <= 0 and self.current_location == 1:
            self.dwarf_bullets = []
            self.current_location = 0
            self.dwarf_x = size[0] - 50

        self.dwarf_x = max(0, min(self.dwarf_x, size[0] - self.dwarf_image.get_width()))

    def shoot(self, keys):
        if keys[pygame.K_SPACE] and self.dwarf_can_shoot:
            bullet_rect = pygame.Rect(self.dwarf_x + self.dwarf_image.get_width() // 2,
                                       self.dwarf_y + self.dwarf_image.get_height() // 2, 10, 5)
            self.dwarf_bullets.append((bullet_rect, self.dwarf_shoot_direction))
            self.dwarf_can_shoot = False

        if not keys[pygame.K_SPACE]:
            self.dwarf_can_shoot = True

    def update_bullets(self, size):
        for bullet, direction in self.dwarf_bullets:
            bullet.x += self.dwarf_bullet_speed * direction

        self.dwarf_bullets = [(bullet, direction) for bullet, direction in self.dwarf_bullets if bullet.x > 0 and bullet.x < size[0]]

    def draw(self, screen):
        screen.blit(background_images[self.current_location], [0, 0])

        for platform in platforms[self.current_location]:
            pygame.draw.rect(screen, (0, 255, 0), platform)

        screen.blit(self.dwarf_image, [self.dwarf_x, self.dwarf_y])

        for bullet, _ in self.dwarf_bullets:
            pygame.draw.rect(screen, (100, 0, 0), bullet)

        pygame.display.flip()

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

    floor_y = screen_height - 100
    platforms_list = platforms(screen_width, screen_height)
    background_images_list = background_images(size)

    return size, screen, floor_y, platforms_list, background_images_list


if __name__ == "__main__":
    size, screen, floor_y, platforms, background_images = initialize_game()
    dwarf = Dwarf(screen.get_height())
    game_dwarf = GameDwarf(dwarf)
    game_dwarf.main(size, floor_y)
