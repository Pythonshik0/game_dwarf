import pygame


class StaticObject(pygame.sprite.Sprite):
    """Статические объекты RECT"""
    def __init__(self, image, position, size):
        super().__init__()
        self.image = pygame.transform.scale(image, size)
        self.rect = pygame.Rect(position[0], position[1], size[0], size[1])

    def draw(self, screen):
        """Отрисовка"""
        screen.blit(self.image, self.rect)


def platforms(screen_width, screen_height):
    left_level_0_platform = 0
    return [
        # Платформы для первой локации
        [
            pygame.Rect(left_level_0_platform, int(screen_height * 0.63), 1270, int(screen_width * 0.02)),
            pygame.Rect(left_level_0_platform + 150, int(screen_height * 0.29), 1270, int(screen_width * 0.02)),
        ],
        # Платформы для второй локации
        [
            pygame.Rect(int(screen_width * 0.2), int(screen_height * 0.66), int(screen_width * 0.1), 10),
            pygame.Rect(int(screen_width * 0.6), int(screen_height * 0.58), int(screen_width * 0.1), 10)
        ]
    ]


def bounding_box_ghost(screen_width, screen_height):
    return [
        # Платформы для первой локации
        [
            pygame.Rect(int(screen_width * 0.1), int(screen_height * 0.01), int(screen_width * 0.8), # Верхний чек бокс
                        int(screen_width * 0.15)),

            pygame.Rect(int(screen_width * 0.1), int(screen_height * 0.35), int(screen_width * 0.8), # Нижний чек бокс
                        int(screen_width * 0.15))
        ],
        [

        ]
    ]



def ladders(screen_width, screen_height):
    return [
        [ # 0 - первая лока
            pygame.Rect(int(screen_width * 0.95), int(screen_height * 0.63), 80, int(screen_width * 0.15)),
            pygame.Rect(int(screen_width * 0), int(screen_height * 0.29), 80, int(screen_width * 0.15)),
        ],
        [

        ]
    ]



def background_images(size):
    return [
        pygame.transform.scale(pygame.image.load("media/image_main/Уровень-1.png").convert(), size),
        pygame.transform.scale(pygame.image.load("media/image_main/Уровень-1.png").convert(), size)
]