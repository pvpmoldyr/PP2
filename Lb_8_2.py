import pygame      
import random        

pygame.init()  

# Цвета 
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
purple = (138, 43, 226)

# Размеры окна
screen_width = 600
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake')

# Параметры змейки
snake_block = 20
snake_speed = 10 

clock = pygame.time.Clock()

# Шрифты для счета и уровня
font_style = pygame.font.SysFont("Yu Gothic", 25)
score_font = pygame.font.SysFont("Yu Gothic", 30)

# Функция для счёта и уровня
def show_score(score, level):
    value = score_font.render(f"Score: {score}   Level: {level}", True, white)
    screen.blit(value, [10, 10])

# Рисуем змейку
def draw_snake(snake_block, snake_list):
    for segment in snake_list:
        pygame.draw.rect(screen, purple, [segment[0], segment[1], snake_block, snake_block])

# Функция для вызова сообщения при проигрыше
def show_message(msg, color):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [screen_width / 6, screen_height / 3])

# Генерация еды, исключая положение змейки
def generate_food(snake_list):
    while True:
        foodx = round(random.randrange(0, screen_width - snake_block) / snake_block) * snake_block
        foody = round(random.randrange(0, screen_height - snake_block) / snake_block) * snake_block
        if [foodx, foody] not in snake_list:
            return foodx, foody

# Основная функция игры
def gameLoop():
    game_over = False
    game_close = False

    # Начальная позиция
    x1 = screen_width // 2
    y1 = screen_height // 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1
    snake_speed = 10
    # Очки и уровень
    score = 0
    level = 1

    # Первая еда
    foodx, foody = generate_food(snake_List)

    while not game_over:

        # Проигрыш
        while game_close:
            screen.fill(red)
            show_message("Game Over! Press P to play again", black)
            show_score(score, level)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        gameLoop()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0

        # Проверка на столкновение со стеной
        if x1 >= screen_width or x1 < 0 or y1 >= screen_height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change

        screen.fill(black)
        pygame.draw.rect(screen, green, [foodx, foody, snake_block, snake_block])

        snake_Head = [x1, y1]
        snake_List.append(snake_Head)

        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Проверка: не врезалась ли змейка в себя
        for segment in snake_List[:-1]:
            if segment == snake_Head:
                game_close = True

        draw_snake(snake_block, snake_List)
        show_score(score, level)
        pygame.display.update()

        # Если съели еду
        if x1 == foodx and y1 == foody:
            foodx, foody = generate_food(snake_List)
            Length_of_snake += 1
            score += 1

            # Переход на следующий уровень каждые 3 очка
            if score % 3 == 0:
                level += 1
                # Увеличиваем скорость на каждом уровне 
                snake_speed = min(30, snake_speed + 2)

        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Начинаем игру
gameLoop()
