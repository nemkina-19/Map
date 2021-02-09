import os
import sys

import pygame
import requests


class Maps:
    def __init__(self, x, y, masshtab):
        self.x = x
        self.y = y
        self.masshtab = masshtab

    def update(self):
        self.map_request = f"http://static-maps.yandex.ru/1.x/?ll={self.y},{self.x}&z={self.masshtab}&l=map&size=650,450"
        self.response = requests.get(self.map_request)
        self.wrong(self.response)

    def wrong(self, response):
        if not response:
            print("Ошибка выполнения запроса:")
            print(self.map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    def write_picture(self):
    # Запишем полученное изображение в файл.
        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)

# Инициализируем pygame
pygame.init()
screen = pygame.display.set_mode((650, 450))
# Рисуем картинку, загружаемую из только что созданного файла.
screen.blit(pygame.image.load(map_file), (0, 0))
# Переключаем экран и ждем закрытия окна.
x, y, masshtab = 60.01, 29.71, 8
map = Maps(x, y, masshtab)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        move = ''
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                 move = 'right'
            elif event.key == pygame.K_LEFT:
                move = 'left'
            elif event.key == pygame.K_UP:
                move = 'up'
            elif event.key == pygame.K_DOWN:
                move = 'down'

    pygame.display.flip()

pygame.quit()
# Удаляем за собой файл с изображением.
os.remove(map_file)