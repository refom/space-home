import pygame

from pygame import mixer
from pygame import mixer_music

def music():
    pygame.mixer.Channel(0).play(pygame.mixer.Sound('assets/bgm.wav'),-1)
    pygame.mixer.Channel(0).set_volume(0.4)
    
def click_sound():
    pygame.mixer.Channel(1).play(pygame.mixer.Sound('assets/click.wav'))
