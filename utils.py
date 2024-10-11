
def screen_ghost_shot(bullet_image, bullets, screen):
    for bullet_info in bullets:
        bullet = bullet_info[0] # Первый элемент всегда будет пуля (bullet)
        screen.blit(bullet_image, (bullet.x, bullet.y))  # Отображаем пули
