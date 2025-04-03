#Импортируем все что нужно
import pygame, sys
from pygame.locals import * #cпособ импортировать все константы и события, определённые в Pygame. Чтобы не писать pygame.quit
import random, time

pygame.init()
#Ограничение количества кадров в секунду
FPS = 60
FramePerSec = pygame.time.Clock()
#Цвета
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
#Размеры экрана
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
#Нужные параметры для игрока
SPEED = 5
SCORE = 0
SCORE_COINS = 0
SPEED_COINS = 7
# В случае столкновения с врагом
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load("PygameTutorial_3_0/AnimatedStreet.png")
#Размеры экрана
DISPLAYSURF = pygame.display.set_mode((400,600))
DISPLAYSURF.fill(WHITE) 
#Добавляем иконку и название
pygame.display.set_caption("Game")
icon = pygame.image.load('PygameTutorial_3_0/Enemy.png')
pygame.display.set_icon(icon)

#Создаем класс для врага
class Enemy(pygame.sprite.Sprite):
      def __init__(self):#функция для инициализации и появления в случайном месте
        super().__init__() 
        self.image = pygame.image.load("PygameTutorial_3_0/Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40,SCREEN_WIDTH-40), 0)

      def move(self):# Функция для движения врага
        global SCORE
        self.rect.move_ip(0,SPEED)
        if (self.rect.bottom > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
#Создаем класс для монетки
class Coin(pygame.sprite.Sprite):
      def __init__(self): #Фунция инилизации монетки в случайном месте
        super().__init__() 
        self.image = pygame.image.load("PygameTutorial_3_0/icons8-coin-48.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40,SCREEN_WIDTH-40), 0)

      def move(self): #Для движения монетки
        global SCORE_COINS
        self.rect.move_ip(0,SPEED_COINS)
        if (self.rect.bottom > 600):
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

#Для движения игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("PygameTutorial_3_0/Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
       
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)
                  

P1 = Player()
E1 = Enemy()
C1 = Coin()
#Создаем группы спрайтов 
enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
coins.add(C1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)


#Создаем пользовательские события для увеличения скорости врагов в дальнейшем
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

while True:
      
    for event in pygame.event.get():
        if event.type == INC_SPEED: #Используем пользовательское событие
              SPEED += 0.5      
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


    DISPLAYSURF.blit(background, (0,0))
    #Обновление спрайтов и отображения их на экране
    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)
    
    #Проверка столкновения игрока с монеткой 
    if pygame.sprite.spritecollideany(P1, coins):
        SCORE_COINS += 1
        C1.rect.top = 0
        C1.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    #Отображение счетов 
    scores = font_small.render("Enemies: " + str(SCORE), True, BLACK)
    coins_score = font_small.render("Coins: " + str(SCORE_COINS), True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))
    DISPLAYSURF.blit(coins_score, (300, 10))

    #Проверка столкновении игрока с врагом
    if pygame.sprite.spritecollideany(P1, enemies):
          pygame.mixer.Sound('PygameTutorial_3_0/crash.wav').play()
          time.sleep(1)
                   
          DISPLAYSURF.fill(RED)
          DISPLAYSURF.blit(game_over, (30,250))
          
          pygame.display.update()
          for entity in all_sprites:
                entity.kill() 
          time.sleep(2)
          pygame.quit()
          sys.exit()        
        
    pygame.display.update()
    FramePerSec.tick(FPS)
