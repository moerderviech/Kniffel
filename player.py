import pygame, dice, rules, player, scorecard, os, game, sys, random

class Player:
    def __init__(self, name):
        self.name=name
        self.rolls=3
        self.card=scorecard.ScoreCard()
