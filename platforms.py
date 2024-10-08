import pygame


def platforms(screen_width, screen_height):
    left_level_0_platform = 0
    return [
        # Платформы для первой локации
        [
            pygame.Rect(left_level_0_platform, int(screen_height * 0.63), 1330, int(screen_width * 0.02)),
        ],
        # Платформы для второй локации
        [
            pygame.Rect(int(screen_width * 0.2), int(screen_height * 0.66), int(screen_width * 0.1), 10),
            pygame.Rect(int(screen_width * 0.6), int(screen_height * 0.58), int(screen_width * 0.1), 10)
        ]
    ]


def ladders(screen_width, screen_height):
    return [
        [ # 0 - первая лока
            pygame.Rect(int(screen_width * 0.95), int(screen_height * 0.64), 70, int(screen_width * 0.2)),
        ],
    ]

def save_home():
    return [
        pygame.Rect(0, 511, 250, 250),
    ]


def background_images(size):
    return [
        pygame.transform.scale(pygame.image.load("media/image_main/Уровень-1.png").convert(), size),
        pygame.transform.scale(pygame.image.load("media/image_main/Уровень-1.png").convert(), size)
]