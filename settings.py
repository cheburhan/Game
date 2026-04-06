import pygame
WIDTH, HEIGHT = 1200, 800  # Устанавливаем ширину и высоту окна игры
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Создаем окно игры с заданными размерами
clock = pygame.time.Clock()  # Создаем объект часов для контроля FPS (кадров в секунду)

# [НОВОЕ] Загрузка фона арены
background = pygame.image.load("arena.jpg")  # Загружаем изображение арены
background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # Масштабируем под размер окна