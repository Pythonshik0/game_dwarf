import pygame


def platforms(screen_width, screen_height):
    return [
        # Платформы для первой локации
        [
            pygame.Rect(int(screen_width * 0.25), int(screen_height * 0.8), int(screen_width * 0.1), 35),
            pygame.Rect(int(screen_width * 0.45), int(screen_height * 0.6), int(screen_width * 0.1), 35),
            # pygame.Rect(int(screen_width * 0.70), int(screen_height * 0.6), int(screen_width * 0.1), 200)
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