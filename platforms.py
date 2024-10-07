import pygame


def platforms(screen_width, screen_height):
    left_level_0_platform = 200
    return [
        # Платформы для первой локации
        [
            pygame.Rect(left_level_0_platform, int(screen_height * 0.8), int(screen_width * 0.1), int(screen_width * 0.02)),
            pygame.Rect(int(left_level_0_platform * 1.45), int(screen_height * 0.6), int(screen_width * 0.1), int(screen_width * 0.02)),
            pygame.Rect(int(left_level_0_platform * 1.45 * 1.3), int(screen_height * 0.4), int(screen_width * 0.1), int(screen_width * 0.02)),
            pygame.Rect(int(left_level_0_platform * 5), int(screen_height * 0.6), int(screen_width * 0.1), int(screen_width * 0.02)),
        ],
        # Платформы для второй локации
        [
            pygame.Rect(int(screen_width * 0.2), int(screen_height * 0.66), int(screen_width * 0.1), 10),
            pygame.Rect(int(screen_width * 0.6), int(screen_height * 0.58), int(screen_width * 0.1), 10)
        ]
    ]


def background_images(size):
    return [
        pygame.transform.scale(pygame.image.load("media/image_main/Уровень-1.png").convert(), size),
        pygame.transform.scale(pygame.image.load("media/image_main/Уровень-1.png").convert(), size)
]