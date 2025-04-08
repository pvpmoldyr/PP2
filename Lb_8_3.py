import pygame
import sys

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
ERASER = 2
current_tool = DRAW_RECTANGLE

# Переменные для рисования
drawing = False
x1, y1 = 0, 0

# Функция рисования кнопок
def draw_color_buttons():
    y_offset = 10  # Начальная позиция для кнопок 
    for i, color in enumerate(colors):  
        pygame.draw.rect(screen, color, (10, y_offset, 50, 50)) 
        y_offset += 60  

# Функция для проверки нажатия на кнопки
def check_color_button_click(pos):
    global current_color
    x, y = pos
    if 10 < x < 60:  # Проверяем, находится ли клик в области кнопок 
        for i, color in enumerate(colors):
            if 10 + i * 60 < y < 60 + i * 60:  # Проверяем, на какой кнопке по вертикали кликнули
                current_color = color
                return True
    return False

# Главный цикл
screen.fill(black)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:  # Левая кнопка мыши нажата
            if event.button == 1:  
                drawing = True
                x1, y1 = event.pos
                if check_color_button_click(event.pos):  
                    continue  # Если клик по кнопке цвета, ничего не рисуем

        if event.type == pygame.MOUSEBUTTONUP:  # Левая кнопка мыши отпущена
            if event.button == 1:  
                drawing = False
                if current_tool == DRAW_RECTANGLE:
                    end_x, end_y = event.pos
                    pygame.draw.rect(screen, current_color, (x1, y1, end_x - x1, end_y - y1))

                elif current_tool == DRAW_CIRCLE:
                    end_x, end_y = event.pos
                    radius = int(((end_x - x1) ** 2 + (end_y - y1) ** 2) ** 0.5)
                    pygame.draw.circle(screen, current_color, (x1, y1), radius)

                elif current_tool == ERASER:
                    end_x, end_y = event.pos
                    pygame.draw.circle(screen, black, (end_x, end_y), 10)  

        if event.type == pygame.MOUSEMOTION:  # Движение мыши
            if drawing:
                if current_tool == DRAW_RECTANGLE:
                    end_x, end_y = event.pos
                    screen.fill(black)  
                    draw_color_buttons()  
                    pygame.draw.rect(screen, current_color, (x1, y1, end_x - x1, end_y - y1), 2)

                elif current_tool == DRAW_CIRCLE:
                    end_x, end_y = event.pos
                    radius = int(((end_x - x1) ** 2 + (end_y - y1) ** 2) ** 0.5)
                    screen.fill(black)  
                    draw_color_buttons()  
                    pygame.draw.circle(screen, current_color, (x1, y1), radius, 2)

                elif current_tool == ERASER:
                    end_x, end_y = event.pos
                    pygame.draw.circle(screen, black, (end_x, end_y), 10)  

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r: 
                current_tool = DRAW_RECTANGLE
            if event.key == pygame.K_c: 
                current_tool = DRAW_CIRCLE
            if event.key == pygame.K_e:  
                current_tool = ERASER

    draw_color_buttons()
    pygame.display.update()
