import pygame
import random

pygame.init()
#Иконка
icon = pygame.image.load('images/snake.png')
pygame.display.set_icon(icon)
# Цвета
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
purple = (160, 32, 240)
orange = (255, 165, 0)


# Размеры экрана
screen_width = 600
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake 2.0')
clock = pygame.time.Clock()

# Параметры змеи
snake_block = 20
snake_speed = 10

# Шрифты для счета и уровня
font_style = pygame.font.SysFont("Yu Gothic", 25)
score_font = pygame.font.SysFont("Yu Gothic", 35)

# Вариации еды: список словарей с весом, цветом и временем исчезновения
food_types = [
    {'color': green, 'score': 1, 'lifetime': 50},
    {'color': orange, 'score': 2, 'lifetime': 60},
    {'color': red, 'score': 3, 'lifetime': 30},
]

# Функция для отображения счёта
def Your_score(score, level):
    value = score_font.render(f"Score: {score}   Level: {level}", True, blue)
    screen.blit(value, [0, 0])

# Рисование змейки
def draw_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, purple, [x[0], x[1], snake_block, snake_block])

# Сообщение при проигрыше
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [screen_width / 6, screen_height / 4])

# Случайная генерация еды
def generate_food(snake_list):
    food_type = random.choice(food_types)
    while True:
        x = round(random.randrange(0, screen_width - snake_block) / 20.0) * 20.0
        y = round(random.randrange(0, screen_height - snake_block) / 20.0) * 20.0
        if [x, y] not in snake_list:  # еда не на змейке
            return {'x': x, 'y': y, 'type': food_type, 'timer': food_type['lifetime']}

# Главный игровой цикл
def gameLoop():
    game_over = False
    game_close = False

    x1 = screen_width / 2
    y1 = screen_height / 2
    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1
    score = 0
    level = 1
    food = generate_food(snake_List)  # создаём еду

    while not game_over:
        while game_close:
            screen.fill(red)
            message("Defeat! Press P-Play Again", black)
            Your_score(score, level)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        gameLoop()

        # Управление движением
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        # Проверка столкновений со стенками
        if x1 >= screen_width or x1 < 0 or y1 >= screen_height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        screen.fill(black)

        # Отображение еды
        pygame.draw.rect(screen, food['type']['color'], [food['x'], food['y'], snake_block, snake_block])

        # Обновляем тело змейки
        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Проверка на самоуничтожение
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        draw_snake(snake_block, snake_List)
        Your_score(score, level)

        # Таймер еды
        food['timer'] -= 1
        if food['timer'] <= 0:
            food = generate_food(snake_List)

        # Проверка съедена ли еда
        if x1 == food['x'] and y1 == food['y']:
            score += food['type']['score']
            Length_of_snake += 1
            food = generate_food(snake_List)

            # Переход на следующий уровень 
            if score // 5 + 1 > level:
                level += 1
                global snake_speed
                snake_speed += 2  

        pygame.display.update()
        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Запуск игры
gameLoop()
