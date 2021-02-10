import math
import sys

import pygame
import requests

ZOOM = 17
x, y = 59.9386, 30.3141


def map_write():
    map_file = "map.png"
    map_request = f"https://static-maps.yandex.ru/1.x/?ll={y},{x}&z={ZOOM}&size=450,450&l=map"
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    # Запишем полученное изображение в файл.

    with open(map_file, "wb") as file:
        file.write(response.content)


# Инициализируем pygame
pygame.init()
screen = pygame.display.set_mode((450, 450))
# Рисуем картинку, загружаемую из только что созданного файла.
map_write()
screen.blit(pygame.image.load("map.png"), (0, 0))
# Переключаем экран и ждем закрытия окна.
running = True
pygame.display.flip()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                if ZOOM + 1 <= 17:
                    ZOOM += 1
                    map_write()
            if event.key == pygame.K_PAGEDOWN:
                if ZOOM - 1 >= 0:
                    ZOOM -= 1
                    map_write()
            if event.key == pygame.K_UP:
                x_1 = 256 / 2 * math.pi * 2 ** ZOOM * (math.pi + math.radians(y))
                x += (450 * x_1 / 10 ** 8) / 10 ** 5.55
                map_write()
            if event.key == pygame.K_DOWN:
                x_1 = 256 / 2 * math.pi * 2 ** ZOOM * (math.pi + math.radians(y))
                x -= (450 * x_1 / 10 ** 8) / 10 ** 5.55
                map_write()
            if event.key == pygame.K_LEFT:
                y_1 = 360 / (math.pow(2, ZOOM + y))
                print(y)
                y -= 450 * y_1 * 10 ** 6.72
                print(y)
                map_write()
            if event.key == pygame.K_RIGHT:
                y_1 = 360 / (math.pow(2, ZOOM + y))
                y += 450 * y_1 * 10 ** 6.72
                map_write()
    screen.blit(pygame.image.load("map.png"), (0, 0))
    pygame.display.flip()

pygame.quit()
