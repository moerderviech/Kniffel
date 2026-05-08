import pygame, dice, rules, player, scorecard, os, game, sys, random, cup

class Game:
    def __init__(self):
        self.win=pygame.display.set_mode((1100,700))
        pygame.display.set_caption("Kniffel")
        self.clock=pygame.time.Clock()
        self.font=pygame.font.SysFont(None,28)
        self.bigfont=pygame.font.SysFont(None,48)
 
        self.players=self.get_player_names()
        self.current=0
        self.cup=cup.Cup()
        self.rules=rules.Rules()
        self.game_over=False
 
    def get_player_names(self):
        names=[]
        input_box=""
        entering=True
        while entering:
            self.win.fill((0,0,0))
            txt=self.bigfont.render("Namen eingeben (ENTER=OK, min 2)",True,(255,255,255))
            self.win.blit(txt,(200,200))
            txt2=self.font.render(input_box,True,(255,255,255))
            self.win.blit(txt2,(200,260))
            pygame.display.flip()
 
            for e in pygame.event.get():
                if e.type==pygame.QUIT:
                    pygame.quit();sys.exit()
                if e.type==pygame.KEYDOWN:
                    if e.key==pygame.K_RETURN:
                        if input_box:
                            names.append(player.Player(input_box))
                            input_box=""
                        if len(names)>=2:
                            entering=False
                    elif e.key==pygame.K_BACKSPACE:
                        input_box=input_box[:-1]
                    else:
                        input_box+=e.unicode
        return names
 
    def draw_scorecard(self):
        x = 520
        y = 40

        row_h = 35
        col_w = 110
        left_w = 220

        fields = [
            'ones','twos','threes','fours','fives','sixes',
            'three_kind','four_kind','full_house',
            'small_street','large_street','kniffel','chance'
        ]

        current_player = self.players[self.current]
        possible = self.rules.calculate_all(self.cup.dice)

        total_width = left_w + len(self.players)*col_w
        total_height = (len(fields)+4)*row_h

        # Hintergrund
        pygame.draw.rect(
            self.win,
            (245,235,210),
            (x,y,total_width,total_height)
        )

        # Außenrahmen
        pygame.draw.rect(
            self.win,
            (0,0,0),
            (x,y,total_width,total_height),
            3
        )

        # Header
        pygame.draw.rect(
            self.win,
            (210,190,150),
            (x,y,total_width,row_h)
        )

        # Vertikale Linien
        for i in range(len(self.players)+1):
            line_x = x + left_w + i*col_w
            pygame.draw.line(
                self.win,
                (0,0,0),
                (line_x,y),
                (line_x,y+total_height),
                2
            )

        # Horizontale Linien
        for i in range(len(fields)+5):
            line_y = y + i*row_h
            pygame.draw.line(
                self.win,
                (0,0,0),
                (x,line_y),
                (x+total_width,line_y),
                2
            )

        # Spielernamen
        for i,p in enumerate(self.players):
            txt = self.font.render(p.name, True, (0,0,0))
            self.win.blit(
                txt,
                (x+left_w+i*col_w+15, y+8)
            )

        # Kategorien + Werte
        row = 1

        for field in fields:

            # Abschnittstrennung
            if field == "three_kind":
                pygame.draw.line(
                    self.win,
                    (0,0,0),
                    (x,y+row*row_h),
                    (x+total_width,y+row*row_h),
                    4
                )

            # Kategoriename
            label = scorecard.ScoreCard()
            label =label.labels[field]

            txt = self.font.render(label, True, (0,0,0))
            self.win.blit(txt, (x+10, y+row*row_h+8))

            # Spielerwerte
            for i,p in enumerate(self.players):

                score = p.card.scores[field]

                display = ""

                # Eingetragene Punkte
                if score is not None:
                    display = str(score)

                # Vorschau beim aktuellen Spieler
                elif (
                    p == current_player
                    and current_player.rolls < 3
                ):
                    display = f"({possible[field]})"

                color = (0,0,0)

                # Aktiver Spieler hervorheben
                if p == current_player:
                    pygame.draw.rect(
                        self.win,
                        (255,255,180),
                        (
                            x+left_w+i*col_w,
                            y+row*row_h,
                            col_w,
                            row_h
                        )
                    )

                txt2 = self.font.render(display, True, color)

                self.win.blit(
                    txt2,
                    (
                        x+left_w+i*col_w+35,
                        y+row*row_h+8
                    )
                )

            row += 1

        # Summenbereich
        summaries = [
            ("Summe oben", lambda p: p.card.upper_total()),
            ("Bonus", lambda p: p.card.bonus()),
            ("GESAMT", lambda p: p.card.total()+p.card.bonus())
        ]

        for title, func in summaries:

            txt = self.font.render(title, True, (0,0,0))
            self.win.blit(txt, (x+10, y+row*row_h+8))

            for i,p in enumerate(self.players):

                value = str(func(p))

                txt2 = self.font.render(value, True, (0,0,0))

                self.win.blit(
                    txt2,
                    (
                        x+left_w+i*col_w+35,
                        y+row*row_h+8
                    )
                )

            row += 1
 
    def next_turn(self):
        self.current=(self.current+1)%len(self.players)
        self.players[self.current].rolls=3
        self.cup.reset()
 
        if all(all(v is not None for v in p.card.scores.values()) for p in self.players):
            self.game_over=True
 
    def winner_screen(self):
        self.win.fill((0,0,0))
        scores=[(p.name,p.card.total()+p.card.bonus()) for p in self.players]
        winner=max(scores,key=lambda x:x[1])
 
        y=200
        for name,score in scores:
            txt=self.bigfont.render(f"{name}: {score}",True,(255,255,255))
            self.win.blit(txt,(300,y));y+=60
 
        win_txt=self.bigfont.render(f"Gewinner: {winner[0]}",True,(0,255,0))
        self.win.blit(win_txt,(300,100))
        pygame.display.flip()
 
        while True:
            for e in pygame.event.get():
                if e.type==pygame.QUIT:
                    pygame.quit();sys.exit()
 
    def run(self):
        while True:
            if self.game_over:
                self.winner_screen()
 
            self.win.fill((0,120,0))
            player=self.players[self.current]
 
            # Animation updaten
            self.cup.update()
 
            possible=self.rules.calculate_all(self.cup.dice)
 
            for e in pygame.event.get():
                if e.type==pygame.QUIT:
                    pygame.quit();sys.exit()
 
                if e.type==pygame.KEYDOWN:
                    if e.key==pygame.K_SPACE and player.rolls>0:
                        self.cup.roll_dice()
                        player.rolls-=1
 
                if e.type==pygame.MOUSEBUTTONDOWN:
                    for d in self.cup.dice:
                        if pygame.Rect(d.position_x,d.position_y,d.size,d.size).collidepoint(e.pos):
                            d.kept=not d.kept
 
                    y=50
                    for f in player.card.scores:
                        rect=pygame.Rect(700,y,350,30)
                        if rect.collidepoint(e.pos) and player.card.is_free(f) and player.rolls<3:
                            player.card.set_score(f,possible[f])
                            self.next_turn()
                        y+=35
 
            self.cup.draw(self.win)
 
            info=self.font.render(f"{player.name} | Würfe: {player.rolls}",True,(255,255,255))
            self.win.blit(info,(50,50))
 
            self.draw_scorecard()
 
            pygame.display.flip()
            self.clock.tick(30)