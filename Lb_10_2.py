import pygame
import random
import psycopg2

# Функции базы данных 
def connect_db():
    return psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="12345",  
        host="localhost",
        port="5432"
    )

# Создание таблицы
def create_table():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(""" 
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT UNIQUE NOT NULL
        );

        CREATE TABLE IF NOT EXISTS user_scores (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            level INTEGER,
            score INTEGER,
            saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def create_user(username):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    if user:
        user_id = user[0]
    else:
        cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING id", (username,))
        user_id = cur.fetchone()[0]
        conn.commit()
    cur.close()
    conn.close()
    return user_id

def get_last_score(user_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT level, score FROM user_scores WHERE user_id = %s ORDER BY saved_at DESC LIMIT 1", (user_id,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result if result else (1, 0)

def save_progress(user_id, level, score):
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO user_scores (user_id, level, score) VALUES (%s, %s, %s)", (user_id, level, score))
        conn.commit()
        cur.close()
        conn.close()
        print("Игровой процесс сохранен")
    except Exception as e:
        print(f"Ошибка при сохранении прогресса: {e}")

# Игровой цикл
pygame.init()
icon = pygame.image.load('images/snake.png')
pygame.display.set_icon(icon)

black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
purple = (160, 32, 240)
orange = (255, 165, 0)

screen_width = 600
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake 2.0')
clock = pygame.time.Clock()

snake_block = 20
snake_speed = 10

font_style = pygame.font.SysFont("Yu Gothic", 25)
score_font = pygame.font.SysFont("Yu Gothic", 35)

food_types = [
    {'color': green, 'score': 1, 'lifetime': 50},
    {'color': orange, 'score': 2, 'lifetime': 60},
    {'color': red, 'score': 3, 'lifetime': 30},
]

def Your_score(score, level):
    value = score_font.render(f"Score: {score}   Level: {level}", True, blue)
    screen.blit(value, [0, 0])

def draw_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, purple, [x[0], x[1], snake_block, snake_block])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [screen_width / 6, screen_height / 4])

def generate_food(snake_list):
    food_type = random.choice(food_types)
    while True:
        x = round(random.randrange(0, screen_width - snake_block) / 20.0) * 20.0
        y = round(random.randrange(0, screen_height - snake_block) / 20.0) * 20.0
        if [x, y] not in snake_list:
            return {'x': x, 'y': y, 'type': food_type, 'timer': food_type['lifetime']}

# Главный цикл игры
def gameLoop():
    global snake_speed
    game_over = False
    game_close = False
    game_paused = False

    x1 = screen_width / 2
    y1 = screen_height / 2
    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    level = last_level
    score = last_score
    snake_speed = 10 + (level - 1) * 2

    food = generate_food(snake_List)

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
                    elif event.key == pygame.K_s:
                        save_progress(user_id, level, score)

        while game_paused:
            screen.fill(purple)
            message("Game Paused. Press P to resume.", black)
            Your_score(score, level)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        game_paused = False

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
                elif event.key == pygame.K_n:  # Пауза
                    game_paused = True
                elif event.key == pygame.K_s:  # Сохранение
                    save_progress(user_id, level, score)

        if x1 >= screen_width or x1 < 0 or y1 >= screen_height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        screen.fill(black)

        pygame.draw.rect(screen, food['type']['color'], [food['x'], food['y'], snake_block, snake_block])

        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        draw_snake(snake_block, snake_List)
        Your_score(score, level)

        food['timer'] -= 1
        if food['timer'] <= 0:
            food = generate_food(snake_List)

        if x1 == food['x'] and y1 == food['y']:
            score += food['type']['score']
            Length_of_snake += 1
            food = generate_food(snake_List)

            if score // 5 + 1 > level:
                level += 1
                snake_speed += 2  

        pygame.display.update()
        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Создание таблиц и начало игры
create_table()
username = input("Enter your username: ")
user_id = create_user(username)
last_level, last_score = get_last_score(user_id)

gameLoop()
