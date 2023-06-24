import sys # used to quit the game
import copy
import pygame as pyg
import numpy as np
from constants import *
import random
pyg.init()# intialising pygame
screen =pyg.display.set_mode( (600,600) )
screen.fill(BG)
pyg.display.set_caption("TIC TAC TOE ")

class board:
    def __init__(self):
        self.squares=np.zeros((ROWS,COLS))
    def mark_board(self,rows,cols,player):
        self.squares[rows][cols]=player
    def empty(self,row,col):
        return self.squares[row][col]==0

        
    def isfull(self,main_li):
        for row in range(ROWS):
            for col in range(COLS):
                if main_li[row][col]==0:
                    return False
                    break
        else:
            return True

    def win_cond(self):
        for col in range(COLS):
            if self.squares[0][col]==self.squares[1][col]==self.squares[2][col]!=0:
                return self.squares[0][col]
        for row in range(ROWS):
            if self.squares[row][0]==self.squares[row][1]==self.squares[row][2]!=0:
                return self.squares[row][0]
        if self.squares[1][1]==self.squares[0][0]==self.squares[2][2]!=0 or self.squares[0][2]==self.squares[1][1]==self.squares[2][0]!=0:
            return self.squares[1][1]
        else:
            return 0
    def sqr_zero(self):
        sqr_zero=[]
        for i,row in enumerate(self.squares):
            for j,ele in enumerate(row):
                if ele==0:
                    sqr_zero.append((i,j))
        return sqr_zero


    def win_mssg(self,player):
        mssg=" "
        if player and player!="DRAW":
            mssg=f"PL{int(player)} wins"
            

        elif not player and self.isfull(self.squares):
            mssg="DRAW"
        if player or mssg=="DRAW":
            font = pyg.font.SysFont(None, 48)
            text = font.render(f"{mssg}", True, (255, 255, 255))
            text_rect = text.get_rect(center=(width // 2, height // 2))
            screen.blit(text, text_rect)
            pyg.display.flip()
            
class AI:
    def __init__(self,level=1,player=2):
        self.player=player
        self.level=level
    def minimax(self,board,maximizing):
        case =board.win_cond()
        empty_li=board.sqr_zero()
        if case==1:
            return 1,None # eval,None
        elif case ==2:
            return -1,None
        elif board.isfull(board.squares):
            return 0,None
        if maximizing:
            max_eval=-100
            best_move=None
            for (row,col) in empty_li:
                temp_board=copy.deepcopy(board)
                temp_board.mark_board(row,col,1)
                eval=self.minimax(temp_board,False)[0]
                if eval > max_eval:
                    max_eval=eval
                    best_move=(row,col)
            return max_eval,best_move
        elif not maximizing:
            min_eval=100
            best_move=None
            for (row,col) in empty_li:
                temp_board=copy.deepcopy(board)
                temp_board.mark_board(row,col,self.player)
                eval=self.minimax(temp_board,True)[0]
                if eval<min_eval:
                    min_eval=eval
                    best_move=(row,col)
            return min_eval,best_move

            
    def ai_main(self,empty_li,main_board,res_li):
        move=[]
        if (self.level==0):
            if len(empty_li)!=0:
                move=random.choice(empty_li)
                res_li[move[0]][move[1]]=2
        else:
            eval,move=self.minimax(main_board,False)
            print(eval)
        return move


        
class Game:
    def __init__(self):
        self.board=board()
        self.player=1# cross marks
        self.show_lines()

    def show_lines(self):
        screen.fill(BG)
        #vertical
        pyg.draw.line(screen,line_color,(SQRSIZE,0),(SQRSIZE,height),line_width)
        pyg.draw.line(screen,line_color,(2*SQRSIZE,0),(2*SQRSIZE,height),line_width)
        #horizontal
        pyg.draw.line(screen,line_color,(0,SQRSIZE),(width,SQRSIZE),line_width)
        pyg.draw.line(screen,line_color,(0,2*SQRSIZE),(width,2*SQRSIZE),line_width)
    def drawfig(self,row,col):
        if (self.player==1):
            pyg.draw.line(screen,CR_COLOR,(col*SQRSIZE+40,row*SQRSIZE+40),(col*SQRSIZE+160,row*SQRSIZE+160),CR_WIDTH)
            pyg.draw.line(screen,CR_COLOR,(col*SQRSIZE+160,row*SQRSIZE+40),(col*SQRSIZE+40,row*SQRSIZE+160),CR_WIDTH)
        elif (self.player==2):
            center=(col*SQRSIZE+SQRSIZE//2,row*SQRSIZE+SQRSIZE//2)
            pyg.draw.circle(screen,circ_col,center,radius,circ_width)
    def next_turn(self):
        if (self.player==1):
            self.player=2
        else:
            self.player=1
    def reset(self):
        self.__init__()
        

def main():
    game=Game()
    board=game.board
    ai=AI()
    # mainloop
    while True:
        for event in pyg.event.get():
            if (event.type==pyg.QUIT):
                pyg.quit()
                sys.exit()
            if (event.type==pyg.KEYDOWN):
                if event.key==pyg.K_0:
                    ai.level=0
                    print(ai.level)
                if event.key==pyg.K_1:
                    ai.level=1
                    print(ai.level)
                if event.key==pyg.K_r:
                    game.reset()
                    board=game.board
            if game.player!=2:
                if ((event.type==pyg.MOUSEBUTTONDOWN) and not board.win_cond()):
                    pos=event.pos
                    row=pos[1]//SQRSIZE
                    col=pos[0]//SQRSIZE
                    if (board.empty(row,col)):
                        board.mark_board(row,col,1)
                        game.drawfig(row,col)
                        board.win_mssg(board.win_cond())
                        if not board.win_cond() and not board.isfull(board.squares):
                            game.next_turn()
            else:
                k=ai.ai_main(board.sqr_zero(),board,board.squares)
                if len(k)==2:
                    board.mark_board(k[0],k[1],2)
                    game.drawfig(k[0],k[1])
                    board.win_mssg(board.win_cond())
                game.next_turn()




        pyg.display.update()
main()
