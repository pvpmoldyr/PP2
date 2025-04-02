import pygame
import time
import math 

pygame.init()

screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Clock")
icon = pygame.image.load('images/clock.png')
pygame.display.set_icon(icon)

background = pygame.transform.scale(pygame.image.load("images/clock.png"), (600, 400))
left_hand = pygame.transform.scale(pygame.image.load("images/leftarm.png"), (21, 480))
right_hand = pygame.transform.scale(pygame.image.load("images/rightarm.png"), (600, 400))

clock = pygame.time.Clock() 
running = True
while running:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    current_time = time.localtime()
    minute = current_time.tm_min
    second = current_time.tm_sec

    second_angle = second * 6
    minute_angle = minute * 6

    screen.blit(background, (0,0))
    
    rotated_right_hand = pygame.transform.rotate(right_hand, -minute_angle)
    right_hand_rect = rotated_right_hand.get_rect(center=(600 // 2, 400 // 2 + 10))
    screen.blit(rotated_right_hand, right_hand_rect)
    
   
    rotated_left_hand = pygame.transform.rotate(left_hand, -second_angle)
    leftarmrect = rotated_left_hand.get_rect(center=(600 // 2, 400 // 2 + 12))
    screen.blit(rotated_left_hand, leftarmrect)

    pygame.display.flip() 
    clock.tick(60)
pygame.quit()
