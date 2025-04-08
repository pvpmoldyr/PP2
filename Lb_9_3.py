import pygame
import sys
import math

pygame.init()

# Размер экрана
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Paint")

# Цвета
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
purple = (160, 32, 240)
white = (255, 255, 255)

# Список цветов
colors = [white, red, green, blue, purple]
current_color = white

# Наши инструменты
DRAW_RECTANGLE = 0
DRAW_CIRCLE = 1
DRAW_SQUARE = 3
DRAW_RIGHT_TRIANGLE = 4
DRAW_EQUILATERAL_TRIANGLE = 5
DRAW_RHOMBUS = 6
ERASER = 2
current_tool = DRAW_RECTANGLE

# Переменные для рисования
drawing = False
x1, y1 = 0, 0

# Функция рисования кнопок для выбора цвета
def draw_color_buttons():
    y_offset = 10  # Начальная позиция для кнопок по вертикали
    for i, color in enumerate(colors):  # Цикл для рисования каждой кнопки
        pygame.draw.rect(screen, color, (10, y_offset, 50, 50))  # Отрисовка кнопки
        y_offset += 60  # Смещение кнопок по вертикали

# Функция для проверки нажатия на кнопки
def check_color_button_click(pos):
    global current_color
    x, y = pos
    if 10 < x < 60:  # Проверяем, находится ли клик в области кнопок (по горизонтали)
        for i, color in enumerate(colors):
            if 10 + i * 60 < y < 60 + i * 60:  # Проверяем, на какой кнопке по вертикали кликнули
                current_color = color
                return True
    return False
#Квадрат
def draw_square(x1, y1, side_length):
    pygame.draw.rect(screen, current_color, (x1, y1, side_length, side_length))
# Прямоугольный треугольник
def draw_right_triangle(x1, y1, base, height):
    pygame.draw.polygon(screen, current_color, [(x1, y1), (x1 + base, y1), (x1, y1 - height)]) #мы создаем полигон что принимает 3 точки 1-основание А, 2-основание В, 3-вершина
# Рвностороний треугольник
def draw_equilateral_triangle(x1, y1, side_length):
    height = side_length * math.sqrt(3) / 2
    points = [(x1, y1), (x1 + side_length, y1), (x1 + side_length / 2, y1 - height)]
    pygame.draw.polygon(screen, current_color, points)
# Ромб
def draw_rhombus(x1, y1, diagonal1, diagonal2):
    points = [(x1, y1 - diagonal2 / 2),  (x1 + diagonal1 / 2, y1),  (x1, y1 + diagonal2 / 2),  (x1 - diagonal1 / 2, y1)]
    pygame.draw.polygon(screen, current_color, points)

screen.fill(black)

# Главный цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:  # Левая кнопка мыши нажата
            if event.button == 1:  
                drawing = True
                x1, y1 = event.pos
                if check_color_button_click(event.pos):  # Если клик по кнопке с цветом
                    continue  # Если клик по кнопке цвета, ничего не рисуем

        if event.type == pygame.MOUSEBUTTONUP:  # Левая кнопка мыши отпущена
            if event.button == 1:  
                drawing = False
                end_x, end_y = event.pos
                if current_tool == DRAW_RECTANGLE:
                    pygame.draw.rect(screen, current_color, (x1, y1, end_x - x1, end_y - y1))

                elif current_tool == DRAW_CIRCLE:
                    radius = int(((end_x - x1) ** 2 + (end_y - y1) ** 2) ** 0.5)
                    pygame.draw.circle(screen, current_color, (x1, y1), radius)

                elif current_tool == DRAW_SQUARE:
                    side_length = min(abs(end_x - x1), abs(end_y - y1))  
                    draw_square(x1, y1, side_length)

                elif current_tool == DRAW_RIGHT_TRIANGLE:
                    base = abs(end_x - x1)
                    height = abs(end_y - y1)
                    draw_right_triangle(x1, y1, base, height)

                elif current_tool == DRAW_EQUILATERAL_TRIANGLE:
                    side_length = int(((end_x - x1) ** 2 + (end_y - y1) ** 2) ** 0.5)
                    draw_equilateral_triangle(x1, y1, side_length)

                elif current_tool == DRAW_RHOMBUS:
                    diagonal1 = abs(end_x - x1)
                    diagonal2 = abs(end_y - y1)
                    draw_rhombus(x1, y1, diagonal1, diagonal2)

                elif current_tool == ERASER:
                    pygame.draw.circle(screen, black, (end_x, end_y), 10)  

        if event.type == pygame.MOUSEMOTION:  # Движение мыши
            if drawing:
                end_x, end_y = event.pos
                screen.fill(black)  
                draw_color_buttons()  # Перерисовываем кнопки
                if current_tool == DRAW_RECTANGLE:
                    pygame.draw.rect(screen, current_color, (x1, y1, end_x - x1, end_y - y1), 2)

                elif current_tool == DRAW_CIRCLE:
                    radius = int(((end_x - x1) ** 2 + (end_y - y1) ** 2) ** 0.5)
                    pygame.draw.circle(screen, current_color, (x1, y1), radius, 2)

                elif current_tool == DRAW_SQUARE:
                    side_length = min(abs(end_x - x1), abs(end_y - y1))
                    draw_square(x1, y1, side_length)

                elif current_tool == DRAW_RIGHT_TRIANGLE:
                    base = abs(end_x - x1)
                    height = abs(end_y - y1)
                    draw_right_triangle(x1, y1, base, height)

                elif current_tool == DRAW_EQUILATERAL_TRIANGLE:
                    side_length = int(((end_x - x1) ** 2 + (end_y - y1) ** 2) ** 0.5)
                    draw_equilateral_triangle(x1, y1, side_length)

                elif current_tool == DRAW_RHOMBUS:
                    diagonal1 = abs(end_x - x1)
                    diagonal2 = abs(end_y - y1)
                    draw_rhombus(x1, y1, diagonal1, diagonal2)

                elif current_tool == ERASER:
                    pygame.draw.circle(screen, black, (end_x, end_y), 10)  

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r: 
                current_tool = DRAW_RECTANGLE
            if event.key == pygame.K_c: 
                current_tool = DRAW_CIRCLE
            if event.key == pygame.K_s:  # Выбор квадрата
                current_tool = DRAW_SQUARE
            if event.key == pygame.K_t:  # Выбор прямоугольного треугольника
                current_tool = DRAW_RIGHT_TRIANGLE
            if event.key == pygame.K_w:  # Выбор равностороннего треугольника
                current_tool = DRAW_EQUILATERAL_TRIANGLE
            if event.key == pygame.K_b:  # Выбор ромба
                current_tool = DRAW_RHOMBUS
            if event.key == pygame.K_e:  # Выбор ластика
                current_tool = ERASER

    draw_color_buttons()  # Рисуем кнопки выбора цвета
    pygame.display.update()  # Обновляем экран
