import pygame

pygame.init()
screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()

radius = 25 
color = ("Red") 
circle_pos = [250, 250] 

running = True
while running:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            running = False


    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            circle_pos[0] -= 20
        elif event.key == pygame.K_RIGHT:
            circle_pos[0] += 20
        elif event.key == pygame.K_UP:
            circle_pos[1] -= 20
        elif event.key == pygame.K_DOWN:
            circle_pos[1] += 20
    
    circle_pos[0] = max(radius, min(500 - radius, circle_pos[0]))
    circle_pos[1] = max(radius, min(500 - radius, circle_pos[1]))
    
    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, color, circle_pos, radius)

    pygame.display.flip()
    clock.tick(60)
