import pygame


def screen_ghost_shot(bullet_image, bullets, screen):
    for bullet_info in bullets:
        bullet = bullet_info[0] # Первый элемент всегда будет пуля (bullet)
        screen.blit(bullet_image, (bullet.x, bullet.y))  # Отображаем пули


def dwarf_move_left_or_right(dwarf_x, flag, dwarf_speed, check_K_DOWN, breath_images, original_height):
    """Функция перемещения dwarf вместе с приседанием"""
    if flag == "L":
        dwarf_x -= dwarf_speed
    elif flag == "R":
        dwarf_x += dwarf_speed

    if check_K_DOWN:  # Возвращаем персонажа в полный рост
        dwarf_image = [pygame.transform.scale(img, (100, original_height)) for img in breath_images]
    else:
        dwarf_image = [pygame.transform.scale(img, (100, original_height)) for img in breath_images]

    return dwarf_x, dwarf_image


def return_to_the_standing_position(check_K_DOWN, dwarf_y, original_height, crouch_height):
    """Возвращение в положение стоя"""
    if check_K_DOWN:
        dwarf_y -= (original_height - crouch_height)
        check_K_DOWN = False

    return dwarf_y, check_K_DOWN