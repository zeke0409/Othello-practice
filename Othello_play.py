import Othello_MCTS as mcts
import Othello_common as cm
from pygame.locals import QUIT,Rect, MOUSEBUTTONDOWN
import pygame
import sys
import matplotlib.pyplot as plt
'''
ゲームプレイ部
pygameが必要
'''
SURFACE = pygame.display.set_mode((800, 600))  # windowのサイズを設定
FPSCLOCK = pygame.time.Clock()
def show(nowstate):
    plt.rcParams['axes.facecolor'] = 'g'
    plt.rcParams['text.color'] = 'w'
    plt.rcParams['xtick.color'] = 'w'
    plt.rcParams['ytick.color'] = 'w'
    SIZE = 8
    line_width = 2
    plt.figure(figsize=(6, 6), facecolor='k')
    for y_pos in range(SIZE):
        plt.axhline(y_pos-.5, color='k', lw=line_width)
        for x_pos in range(SIZE):
            if nowstate.state[y_pos][x_pos] == 1:
                plt.plot(color='w', marker='o')
            plt.axvline(x_pos-.5, color='k', lw=line_width)

    plt.xlim([-.5, 8-.5])
    plt.ylim([-.5, 8-.5])
    for y_pos in range(SIZE):
        for x_pos in range(SIZE):
            if nowstate.state[y_pos][x_pos] == 1:
                plt.scatter(y_pos, x_pos, color='white',
                            marker='o', zorder=2, s=200)
            if nowstate.state[y_pos][x_pos] == 2:
                plt.scatter(y_pos, x_pos, color='black',
                            marker='o', zorder=2, s=200)
    plt.show()
    
def my_turn(nowstate,p_flag):
    #show(nowstate)
    print("My turn..")
    if nowstate.is_possible_hand():
        if p_flag==1:
            return nowstate, -1
        p_flag = 1
        print("PASS!!")
    else:
        p_flag = 0
        _,num=nowstate.possible_state()
        num=len(num)
        res = mcts.MCTS(nowstate,num*30,5)
        nowstate = nowstate.next_state(res)
        nowstate = cm.State(2, nowstate)
    nowstate.str_show()
    return nowstate,p_flag
def your_turn(nowstate,p_flag):
    print("yout turn..")
    if nowstate.is_possible_hand():
        if p_flag==1:
            return nowstate,-1
        p_flag = 1
        print("YOU PASS!!")
    else:
        p_flag = 0
        hand = 0
        flag=False
        while True:
            for event in pygame.event.get():
                if(event.type == QUIT):
                    pygame.quit()
                    sys.exit()
                if(event.type == MOUSEBUTTONDOWN and event.button == 1 and (event.pos[0] >= 50 and event.pos[0] <450 and event.pos[1]>=50 and event.pos[1]<450)):
                    x_pos=(event.pos[0]-50)//50
                    y_pos=(event.pos[1]-50)//50
                    pos=y_pos*8+x_pos
                    print(x_pos, y_pos)
                    _,p_hand=nowstate.possible_state()
                    if pos in p_hand:
                        nowstate = nowstate.next_state(pos)
                        flag=True
                        print("valid input")
                        break
            if flag:
                print("valid")
                break
        print("valid2")
        nowstate = cm.State(1, nowstate)
        nowstate.str_show()
    return nowstate,p_flag


def draw_stone(state):
    print("draw")
    for i in range(8):
        for j in range(8):
            #pygame.draw.rect(SURFACE, (255, 255, 0), Rect(10, 10, 300, 200))
            x1=50*i+50
            y1=50*j+50
            pygame.draw.rect(SURFACE, (0, 0, 0),Rect(x1, y1, 50,50),1)
    for i in range(8):
        for j in range(8):
            stone=state.state[i][j]
            ypos = (50 * i)+55
            xpos =  (50 * j)+55
            if(stone == 2):
                pygame.draw.ellipse(SURFACE, (0,0,0),((xpos, ypos), (40, 40)))
            elif(stone == 1):
                pygame.draw.ellipse(SURFACE, (0,0,0),((xpos, ypos), (40, 40)),1)
            elif(stone == 0):
                pass
            else:
                print("error")
                sys.exit()

if __name__=='__main__':
    '''initial define'''
    pygame.init()
    
    #screen = pygame.display.set_mode((800, 600))
    #pygame.display.set_caption("Othello by zeke")
    #nowstate=cm.State(1)
    p_flag=0
    #screen.fill((255, 63, 10,))
    #pygame.display.update()

    '''TITLE'''
    sysfont_title = pygame.font.SysFont('hg教科書体hgp教科書体hgs教科書体', 80)
    title = sysfont_title.render("Othello by zeke", True, (0, 0, 0))
    title_rect = title.get_rect()
    title_rect.center = (400, 200)

    sysfont_start = pygame.font.SysFont('hg教科書体hgp教科書体hgs教科書体', 20)
    start = sysfont_start.render("GAME START", True, (255, 255, 255))
    start_rect = start.get_rect()
    
    start_rect.center = (400, 400)
    while(True):
        xpos = 0
        ypos = 0
        for event in pygame.event.get():
            if(event.type == QUIT):
                pygame.quit()
                sys.exit()
            if(event.type == MOUSEBUTTONDOWN and event.button == 1):
                xpos, ypos = event.pos[0], event.pos[1]
        if((xpos >= 325) and (xpos <= 475) and (ypos >= 375) and (ypos <= 425)):
            break
        SURFACE.fill((255, 255, 255))
        SURFACE.blit(title, title_rect)
        x = 150
        y = 50
        pygame.draw.rect(SURFACE, (0, 0, 0), ((400-(x/2), 400-(y/2)), (x, y)))
        SURFACE.blit(start, start_rect)
        pygame.display.update()
        FPSCLOCK.tick(3)
    nowstate = cm.State(1)
    SURFACE.fill((255, 255, 255))
    draw_stone(nowstate)
    pygame.display.update()
    FPSCLOCK.tick(3)
    #play game!
    #global nowstate
    
    print("play game")
    while(1):
        nowstate,p_flag=my_turn(nowstate,p_flag)
        if p_flag==-1:
            break
        SURFACE.fill((255, 255, 255))
        draw_stone(nowstate)
        pygame.display.update()
        FPSCLOCK.tick(3)
        nowstate,p_flag=your_turn(nowstate,p_flag)
        if p_flag==-1:
            break
        SURFACE.fill((255, 255, 255))
        draw_stone(nowstate)
        pygame.display.update()
        FPSCLOCK.tick(3)
    print("FINISHed")
    if nowstate.is_win()==1:
        print("hahaha")
    elif nowstate.is_win()==0:
        print("you win")
    else:
        print("draw")
    
