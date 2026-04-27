import pygame, dice, rules, player, scorecard, os

os.system("cls")
pygame.init()
surface = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Kniffel")

#Variablen:
running = True
