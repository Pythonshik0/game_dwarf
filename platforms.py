import pygame


def platforms(screen_width, screen_height):
    return [
        # Платформы для первой локации
        [
            pygame.Rect(int(screen_width * 0.25), int(screen_height * 0.75), int(screen_width * 0.15), 10),
            pygame.Rect(int(screen_width * 0.45), int(screen_height * 0.6), int(screen_width * 0.1), 10)
        ],
        # Платформы для второй локации
        [
            pygame.Rect(int(screen_width * 0.2), int(screen_height * 0.66), int(screen_width * 0.1), 10),
            pygame.Rect(int(screen_width * 0.6), int(screen_height * 0.58), int(screen_width * 0.1), 10)
        ]
    ]



def background_images(size):
    return [
        pygame.transform.scale(pygame.image.load("media/image_main/home_1_lvl.jpg").convert(), size),
        pygame.transform.scale(pygame.image.load("media/image_main/home-level-2.jpg").convert(), size)
]