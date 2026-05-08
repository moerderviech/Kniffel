import pygame, dice, rules, player, scorecard, os, game, sys, random

class Dice:
    def __init__(self, x, y, size=60):
        self.value = 1
        self.size = size
        self.position_x = x
        self.position_y = y
        self.kept = False
 
        # Animationszustand
        self.animating = False
        self.anim_frames = 0
        self.anim_duration = 20  # frames

        # Punktepositionen
        cx = self.position_x
        cy = self.position_y
        s = self.size
        self.r = 5  # Radius der Punkte
        
        self.positions = {
            "tl": (cx + s*0.25, cy + s*0.25),
            "tr": (cx + s*0.75, cy + s*0.25),
            "ml": (cx + s*0.25, cy + s*0.5),
            "mr": (cx + s*0.75, cy + s*0.5),
            "bl": (cx + s*0.25, cy + s*0.75),
            "br": (cx + s*0.75, cy + s*0.75),
            "c":  (cx + s*0.5,  cy + s*0.5),
        }

        # Welche Punkte pro Zahl gezeichnet werden
        self.dice_patterns = {
            1: ["c"],
            2: ["tl", "br"],
            3: ["tl", "c", "br"],
            4: ["tl", "tr", "bl", "br"],
            5: ["tl", "tr", "c", "bl", "br"],
            6: ["tl", "tr", "ml", "mr", "bl", "br"],
            }
        
    def start_animation(self):
        if not self.kept:
            self.animating = True
            self.anim_frames = 0
 
    def update_animation(self):
        if self.animating:
            self.anim_frames += 1
            # während Animation zufällige Werte anzeigen
            self.value = random.randint(1, 6)
 
            if self.anim_frames >= self.anim_duration:
                self.animating = False
                self.value = random.randint(1, 6)
 
    def roll_dice(self):
        if not self.kept:
            self.start_animation()
 
    def draw(self, screen):
        rect = pygame.Rect(self.position_x, self.position_y, self.size, self.size,)
 
        # Farbe je nach Zustand
        if self.animating:
            color = (255, 255, 150)  # gelb = animiert
        elif self.kept:
            color = (200, 255, 200)
        else:
            color = (255, 255, 255)
 
        pygame.draw.rect(screen, color, rect, border_radius=15)
        pygame.draw.rect(screen, (0,0,0), rect, 2, border_radius=15)
 
        # Punkte zeichnen
        for pos in self.dice_patterns[self.value]:
            pygame.draw.circle(screen, (0,0,0), self.positions[pos], self.r)