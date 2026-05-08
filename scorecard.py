import pygame, dice, rules, player, scorecard, os, game, sys, random

class ScoreCard:
    def __init__(self):
        self.scores = {k: None for k in [
            'ones','twos','threes','fours','fives','sixes',
            'three_kind','four_kind','full_house','small_street',
            'large_street','kniffel','chance']}
        
        self.labels = {
            'ones': 'Einser',
            'twos': 'Zweier',
            'threes': 'Dreier',
            'fours': 'Vierer',
            'fives': 'Fünfer',
            'sixes': 'Sechser',
            'three_kind': 'Dreierpasch',
            'four_kind': 'Viererpasch',
            'full_house': 'Full House',
            'small_street': 'Kleine Straße',
            'large_street': 'Große Straße',
            'kniffel': 'Kniffel',
            'chance': 'Chance'
        }
        
    def set_score(self, field, score):
        self.scores[field] = score
 
    def total(self):
        return sum(v for v in self.scores.values() if v is not None)
 
    def upper_total(self):
        return sum(v for k,v in self.scores.items() if k in ['ones','twos','threes','fours','fives','sixes'] and v)
 
    def bonus(self):
        return 35 if self.upper_total() >= 63 else 0
 
    def is_free(self, field):
        return self.scores[field] is None