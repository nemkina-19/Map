import os
import sys

import pygame
import requests

ZOOM = 17


def map_write():
    map_file = "map.png"
    map_request = f"https://static-maps.yandex.ru/1.x/?ll=37.620070,53.453630&z={ZOOM}&size=450,450&l=map"
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
    screen.blit(pygame.image.load("map.png"), (0, 0))
    pygame.display.flip()

pygame.quit()
