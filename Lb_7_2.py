import pygame
import os

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Music player")
icon = pygame.image.load('images/Qi Yu(Rafayel).png')
pygame.display.set_icon(icon)
background = pygame.transform.scale(pygame.image.load("images/Qi Yu(Rafayel).png"), (600,400))


tracks_folder = "C:/Users/ASUS/Desktop/Pirate Playlist"
os.chdir(tracks_folder)
music_files = [f for f in os.listdir() if f.endswith(".mp3")]

current_song = 0
pygame.mixer.music.load(os.path.join(tracks_folder, music_files[current_song]))

running = True
while running:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:  
                pygame.mixer.music.play()
            elif event.key == pygame.K_s:  
                pygame.mixer.music.stop()
            elif event.key == pygame.K_d:  
                current_song = (current_song + 1) % len(music_files)
                pygame.mixer.music.load(os.path.join(tracks_folder, music_files[current_song]))
                pygame.mixer.music.play()
            elif event.key == pygame.K_a:  
                current_song = (current_song - 1) % len(music_files)
                pygame.mixer.music.load(os.path.join(tracks_folder, music_files[current_song]))
                pygame.mixer.music.play()
            elif event.key == pygame.K_e:  
                    pygame.mixer.music.unpause()  
            elif event.key == pygame.K_r: 
                    pygame.mixer.music.pause()  
                
    
   
    screen.blit(background, (0, 0))
    pygame.display.flip()

pygame.quit()
