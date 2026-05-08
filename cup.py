import pygame, dice, rules, player, scorecard, os, game, sys, random

class Cup:
    def __init__(self):
        self.dice = [
            dice.Dice(180, 180),  # oben links
            dice.Dice(260, 180),  # oben rechts

            dice.Dice(140, 270),  # unten links
            dice.Dice(220, 270),  # unten mitte
            dice.Dice(300, 270),  # unten rechts
        ]
 
    def draw(self, screen):
        # Container
        container = pygame.Rect(90, 120, 320, 280)

        pygame.draw.rect(screen, (80, 50, 20), container, border_radius=20)
        pygame.draw.rect(screen, (160, 120, 70), container, 5, border_radius=20)

        # Würfel zeichnen
        for d in self.dice:
            d.draw(screen)

    def roll_dice(self):
        for d in self.dice:
            d.roll_dice()
 
    def update(self):
        for d in self.dice:
            d.update_animation()
 
    def reset(self):
        for d in self.dice:
            d.kept = False