import math
import sys

import pygame
import requests

ZOOM = 17
MODE = 'map'
x, y = 59.9386, 30.3141
xc, yc = 59.9386, 30.3141
TXT = 0
geoflag = False


# отрисовка кнопки
def draw(screen, x, y, btn_size_x, btn_size_y, text, search=False):
    global TXT
    font = pygame.font.Font(None, 25)
    text1 = font.render(text[TXT:], True, (0, 0, 0))
    if text != '':
        pygame.draw.rect(screen, (211, 211, 211), (x, y, btn_size_x, btn_size_y))
    else:
        pygame.draw.rect(screen, (255, 255, 255), (x, y, btn_size_x, btn_size_y))
    if text1.get_width() > 240:
        TXT += 35
    screen.blit(text1, (x + 10, y + btn_size_y // 4))


def geoXY(request):
    response = requests.get(request)
    # Пример \\\\\\   Красная пл-дь, 1
    if not response:
        print("Ошибка выполнения запроса:")
        print(request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        return False
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
    toponym_coodrinates = toponym["Point"]["pos"]
    return toponym["Point"]["pos"]


def map_write():
    map_file = "map.png"
    map_request = f"https://static-maps.yandex.ru/1.x/?ll={y},{x}&z={ZOOM}&size=450,450&l={MODE}"
    if geoflag:
        map_request = f"https://static-maps.yandex.ru/1.x/?ll={y},{x}&z={ZOOM}&size=450,450&l={MODE}&pt={yc},{xc},pm2rdm"
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
screen = pygame.display.set_mode((450, 560))
# Рисуем картинку, загружаемую из только что созданного файла.
map_write()
screen.blit(pygame.image.load("map.png"), (0, 0))
# Переключаем экран и ждем закрытия окна.
search = False
search_txt = ''
running = True
pygame.display.flip()
screen.fill(pygame.Color(105, 105, 105))
# Координаты кнопок
btn_1x, btn_1y = 20, 460
btn_2x, btn_2y = 165, 460
btn_3x, btn_3y = 310, 460
btn_size_x = 120
btn_size_y = 50
btn_search_x, btn_search_y = 310, 520
btn_search_size_x, btn_search_size_y = 120, 30
# Прорисовываем кнопки
draw(screen, btn_1x, btn_1y, btn_size_x, btn_size_y, 'Схема  ')
draw(screen, btn_2x, btn_2y, btn_size_x, btn_size_y, 'Спутник')
draw(screen, btn_3x, btn_3y, btn_size_x, btn_size_y, 'Гибрид ')
draw(screen, btn_search_x, btn_search_y, btn_search_size_x, btn_search_size_y, 'Поиск  ')
# Поле ввода
table_x, table_y, table_size_x, table_size_y = 20, 520, 265, 30
draw(screen, table_x, table_y, table_size_x, table_size_y, '', True)
# Основной цикл
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if btn_1x <= event.pos[0] <= btn_1x + btn_size_x and btn_1y <= event.pos[1] <= btn_1y + btn_size_y:
                MODE = 'map'
                map_write()
                search = False
            elif btn_2x <= event.pos[0] <= btn_2x + btn_size_x and btn_2y <= event.pos[1] <= btn_2y + btn_size_y:
                MODE = 'sat'
                map_write()
                search = False
            elif btn_3x <= event.pos[0] <= btn_3x + btn_size_x and btn_3y <= event.pos[1] <= btn_3y + btn_size_y:
                MODE = 'sat,skl'
                map_write()
                search = False
            elif btn_search_x <= event.pos[0] <= btn_search_x + btn_search_size_x and btn_search_y <= event.pos[1] <= \
                    btn_search_y + btn_search_size_y:
                b = geoXY(f"http://geocode-maps.yandex.ru/1.x/?apikey=40d16"
                            f"49f-0493-4b70-98ba-98533de7710b&geocode={search_txt}&format=json")
                if b:
                    y, x = b.split()
                    geoflag = True
                    yc = float(y)
                    xc = float(x)
                    y = yc
                    x = xc
                    search_txt = ''
                    map_write()
                search = False
            elif table_x <= event.pos[0] <= table_x + table_size_x \
                    and table_y <= event.pos[1] <= table_y + table_size_y:
                search = True
        if event.type == pygame.KEYDOWN:
            if search:
                search_txt += event.unicode
                draw(screen, table_x, table_y, table_size_x, table_size_y, search_txt)
            if search and event.key == pygame.K_BACKSPACE and search_txt:
                search_txt = search_txt[:-1]
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                if ZOOM + 1 <= 17:
                    ZOOM += 1
                    map_write()
            if event.key == pygame.K_PAGEDOWN:
                if ZOOM - 1 >= 0:
                    ZOOM -= 1
                    map_write()
            # ошибка при большом шасштабе
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
                y -= 450 * y_1 * 10 ** 6.72
                map_write()
            if event.key == pygame.K_RIGHT:
                y_1 = 360 / (math.pow(2, ZOOM + y))
                y += 450 * y_1 * 10 ** 6.72
                map_write()
    screen.blit(pygame.image.load("map.png"), (0, 0))
    pygame.display.flip()

pygame.quit()
