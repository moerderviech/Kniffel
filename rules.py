import pygame, dice, rules, player, scorecard, os, game, sys, random

class Rules:
    def calculate_all(self, dice):
        vals=[d.value for d in dice]
        counts={i:vals.count(i) for i in range(1,7)}
        return {
            'ones':counts[1]*1,'twos':counts[2]*2,'threes':counts[3]*3,
            'fours':counts[4]*4,'fives':counts[5]*5,'sixes':counts[6]*6,
            'three_kind':sum(vals) if max(counts.values())>=3 else 0,
            'four_kind':sum(vals) if max(counts.values())>=4 else 0,
            'full_house':25 if sorted(counts.values(),reverse=True)[:2]==[3,2] else 0,
            'small_street':30 if any(set(s).issubset(vals) for s in ([1,2,3,4],[2,3,4,5],[3,4,5,6])) else 0,
            'large_street':40 if set(vals) in [set([1,2,3,4,5]),set([2,3,4,5,6])] else 0,
            'kniffel':50 if max(counts.values())==5 else 0,
            'chance':sum(vals)
        }