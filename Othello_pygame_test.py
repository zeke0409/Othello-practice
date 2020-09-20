""" othello16-pygame.py  Copyright 2019 niwakoma """
import sys
import pygame
import random
from math import floor
import numpy as np
from pygame.locals import QUIT, MOUSEBUTTONDOWN
import copy

pygame.init()  # pygameを初期化
SURFACE = pygame.display.set_mode((800, 600))  # windowのサイズを設定
FPSCLOCK = pygame.time.Clock()


def stone_location(stone):
    stone_list = []
    for i in range(4):
        for j in range(4):
            if(field[(i, j)] == stone):
                stone_list.append((i, j))
    return stone_list


def empty_location(stone_list):
    emp = {}
    for x, y in stone_list:
        for i in offset_x:
            for j in offset_y:
                p = (x+i, y+j)
                if((p[0] <= 3) and (p[0] >= 0) and (p[1] <= 3) and (p[1] >= 0)):
                    if((field[p] == EMPTY) and not(p in emp)):
                        emp[p] = []
                        emp[p].append((i, j))
                    elif((field[p] == EMPTY) and (p in emp)):
                        emp[p].append((i, j))
                    else:
                        pass
                else:
                    pass
    return emp


def black_turn():
    #白石が置かれている場所のリスト
    white_stone = stone_location(WHITE)
    # 空マスの座標を返す
    emp = empty_location(white_stone)
    # 黒石が置ける座標を返す
    black_possible = []
    black_dic = {}
    for kx, ky in emp.keys():
        #print("({0}, {1})".format(kx, ky))
        for vx, vy in emp[kx, ky]:
            addx = vx*(-1)
            addy = vy*(-1)
            px = kx+(vx*(-1))
            py = ky+(vy*(-1))
            p = (px, py)
            while((px >= 0 and px <= 3) and (py >= 0 and py <= 3)):
                #print(p, end="")
                if(field[p] == WHITE):
                    #print("WHITE")
                    pass
                elif(field[p] == BLACK):
                    if(not((kx, ky) in black_dic) and not((kx, ky) in black_possible)):
                        black_possible.append((kx, ky))
                        black_dic[(kx, ky)] = [(addx, addy)]
                    elif(((kx, ky) in black_dic) and ((kx, ky) in black_possible)):
                        black_dic[(kx, ky)].append((addx, addy))
                    #print("BLACK")
                    break
                else:
                    #print("EMPTY")
                    break
                px = px + addx
                py = py + addy
                p = (px, py)
            #print("({0}, {1})".format(kx+(vx*(-1)), ky+(vy*(-1))))
            #print("")
    # black_possibleから1つ選出する
    if(len(black_possible) == 0):
        return (-1, -1), [(0, 0)]
    r = random.randrange(len(black_possible))
    return black_possible[r], black_dic[black_possible[r]]


def white_turn():
    #黒石が置かれている場所のリスト
    black_stone = stone_location(BLACK)
    # 空マスの座標を返す
    emp = empty_location(black_stone)
    # 白石が置ける座標を返す
    white_possible = []
    white_dic = {}
    for kx, ky in emp.keys():
        #print("({0}, {1})".format(kx, ky))
        for vx, vy in emp[kx, ky]:
            addx = vx*(-1)
            addy = vy*(-1)
            px = kx+(vx*(-1))
            py = ky+(vy*(-1))
            p = (px, py)
            while((px >= 0 and px <= 3) and (py >= 0 and py <= 3)):
                #print(p, end="")
                if(field[p] == WHITE):
                    if(not((kx, ky) in white_dic) and not((kx, ky) in white_possible)):
                        white_possible.append((kx, ky))
                        white_dic[(kx, ky)] = [(addx, addy)]
                    elif(((kx, ky) in white_dic) and ((kx, ky) in white_possible)):
                        white_dic[(kx, ky)].append((addx, addy))
                    #print("WHITE")
                    break
                elif(field[p] == BLACK):
                    #print("BLACK")
                    pass
                else:
                    #print("EMPTY")
                    break
                px = px + addx
                py = py + addy
                p = (px, py)
            #print("({0}, {1})".format(kx+(vx*(-1)), ky+(vy*(-1))))
            #print("")
    # black_possibleから1つ選出する
    if(len(white_possible) == 0):
        return (-1, -1), [(0, 0)]
    r = random.randrange(len(white_possible))
    return white_possible[r], white_dic[white_possible[r]]


def update_field(TURN, point, offset_list):
    # 石を更新する座標を返す
    px = point[0]
    py = point[1]
    update_possible = []
    update_possible.append(point)
    for addx, addy in offset_list:
        vx = px
        vy = py
        value = point
        while((vx >= 0 and vx <= 3) and (vy >= 0 and vy <= 3)):
            p = field[value]
            if((p == TURN) or (p == EMPTY) and not(value in update_possible)):
                break
            elif((p != TURN) and (p != EMPTY) and not(value in update_possible)):
                update_possible.append(value)
            else:
                pass
            vx = vx + addx
            vy = vy + addy
            value = (vx, vy)
    for i in update_possible:
        field[i] = TURN
    return field


def address2point(address):
    for i in range(0, 4):
        for j in range(0, 4):
            if(field_address[(i, j)] == address and field[(i, j)] == 0):
                return (i, j)
    return (-1, -1)


def point2offset(point, TURN):
    #print("TURN", TURN)
    px = point[0]
    py = point[1]
    p2o_list = []
    for i in offset_x:
        for j in offset_y:
            vx = px + i
            vy = py + j
            p = (vx, vy)
            if((p[0] <= 3) and (p[0] >= 0) and (p[1] <= 3) and (p[1] >= 0) and (field[p] != TURN) and (field[p] != EMPTY)):
                vx = vx + i
                vy = vy + j
                p = (vx, vy)
                while((p[0] <= 3) and (p[0] >= 0) and (p[1] <= 3) and (p[1] >= 0)):
                    if(field[p] != TURN and field[p] != EMPTY):
                        #print(" not TURN and not EMPTY")
                        pass
                    elif(field[p] == TURN and field[p] != EMPTY):
                        #print("TURN")
                        p2o_list.append((i, j))
                        break
                    elif(field[p] != TURN and field[p] == EMPTY):
                        #print("EMPTY")
                        break
                    vx = vx + i
                    vy = vy + j
                    p = (vx, vy)
    return p2o_list


def address_check(point, TURN):
    #TURNと反対の石が置かれている場所のリスト
    bw_stone = stone_location(3-TURN)
    # 空マスの座標を返す
    emp = empty_location(bw_stone)
    # TURNが置ける座標を返す
    stone_possible = []
    stone_dic = {}
    for kx, ky in emp.keys():
        for vx, vy in emp[kx, ky]:
            addx = vx*(-1)
            addy = vy*(-1)
            px = kx+(vx*(-1))
            py = ky+(vy*(-1))
            p = (px, py)
            while((px >= 0 and px <= 3) and (py >= 0 and py <= 3)):
                if(field[p] != TURN):
                    pass
                elif(field[p] == TURN):
                    if(not((kx, ky) in stone_dic) and not((kx, ky) in stone_possible)):
                        stone_possible.append((kx, ky))
                        stone_dic[(kx, ky)] = [(addx, addy)]
                    elif(((kx, ky) in stone_dic) and ((kx, ky) in stone_possible)):
                        stone_dic[(kx, ky)].append((addx, addy))
                    break
                else:
                    break
                px = px + addx
                py = py + addy
                p = (px, py)
    if(point in stone_possible):
        return True
    return False


def draw_stone(SURFACE, field):
    for i in range(4):
        for j in range(4):
            stone = field[(i, j)]
            ypos = 75 + (150 * i) - 60
            xpos = 175 + (150 * j) - 60
            if(stone == BLACK):
                pygame.draw.ellipse(SURFACE, 0x000000,
                                    ((xpos, ypos), (120, 120)))
            elif(stone == WHITE):
                pygame.draw.ellipse(SURFACE, 0x000000,
                                    ((xpos, ypos), (120, 120)), 10)
            elif(stone == EMPTY):
                pass
            else:
                print("error")
                sys.exit()

 
def show_result():
    black_stone = 0
    white_stone = 0
    for i in range(4):
        for j in range(4):
            stone = field[(i, j)]
            if(stone == 1):
                black_stone += 1
            elif(stone == 2):
                white_stone += 1
            else:
                pass
    s = ""
    winner = ""
    if(black_stone < white_stone):
        winner = "後手（白石）"
        s = "勝者は{0}".format(winner)
    elif(black_stone > white_stone):
        winner = "先手（黒石）"
        s = "勝者は{0}".format(winner)
    elif(black_stone == white_stone):
        s = "引き分け"
    else:
        winner = ""

    print("")
    print("===================")
    print("結果発表")
    print("黒石：{0}石".format(black_stone))
    print("白石：{0}石".format(white_stone))
    print("")
    print("よって、{0}です。".format(s))


def player_turn():
    sysfont_turn = pygame.font.SysFont(None, 24)
    turn = sysfont_turn.render("TURN", True, (0, 0, 0))
    turn_rect = turn.get_rect()
    turn_rect.center = (50, 50)
    sysfont_pt = pygame.font.SysFont(None, 24)
    pt = sysfont_pt.render("Player", True, (0, 0, 0))
    pt_rect = pt.get_rect()
    pt_rect.center = (50, 100)
    s = ""
    if(Player == BLACK):
        s = "BLACK"
    elif(Player == WHITE):
        s = "WHITE"
    sysfont_color = pygame.font.SysFont(None, 24)
    color = sysfont_color.render(s, True, (0, 0, 0))
    color_rect = color.get_rect()
    color_rect.center = (50, 150)
    while(True):
        address = ""
        for event in pygame.event.get():
            if(event.type == QUIT):
                pygame.quit()
                sys.exit()
            if(event.type == MOUSEBUTTONDOWN and event.button == 1 and (event.pos[0] >= 100 and event.pos[0] < 700)):
                xpos, ypos = floor(
                    (event.pos[0]-100)/150), floor(event.pos[1]/150)
                address = field_address[(ypos, xpos)]
                #print("({0}, {1}), address = {2}".format(ypos, xpos, address))
                break
        if(address in field_address):
            break
        # drawing line
        SURFACE.fill((255, 255, 255))
        weight = 10
        for xpos in range(100, 701, 150):
            pygame.draw.line(SURFACE, 0x000000, (xpos, 0), (xpos, 601), weight)
        for ypos in range(0, 601, 150):
            pygame.draw.line(SURFACE, 0x000000, (100, ypos),
                             (701, ypos), weight)
        # drawing stone
        draw_stone(SURFACE, field)
        SURFACE.blit(turn, turn_rect)
        SURFACE.blit(pt, pt_rect)
        SURFACE.blit(color, color_rect)

        pygame.display.update()
        FPSCLOCK.tick(3)
    return address

# playerが画面のクリックするまで画面のを表示


def computer_turn():
    sysfont_turn = pygame.font.SysFont(None, 24)
    turn = sysfont_turn.render("TURN", True, (0, 0, 0))
    turn_rect = turn.get_rect()
    turn_rect.center = (50, 50)
    sysfont_ct = pygame.font.SysFont(None, 24)
    ct = sysfont_ct.render("Computer", True, (0, 0, 0))
    ct_rect = ct.get_rect()
    ct_rect.center = (50, 100)
    s = ""
    if(Computer == BLACK):
        s = "BLACK"
    elif(Computer == WHITE):
        s = "WHITE"
    sysfont_color = pygame.font.SysFont(None, 24)
    color = sysfont_color.render(s, True, (0, 0, 0))
    color_rect = color.get_rect()
    color_rect.center = (50, 150)
    x, y = -1, -1
    while(True):
        for event in pygame.event.get():
            if(event.type == QUIT):
                pygame.quit()
                sys.exit()
            if(event.type == MOUSEBUTTONDOWN and event.button == 1):
                x, y = event.pos[0], event.pos[1]
                break
        # drawing line
        SURFACE.fill((255, 255, 255))
        weight = 10
        for xpos in range(100, 701, 150):
            pygame.draw.line(SURFACE, 0x000000, (xpos, 0), (xpos, 601), weight)
        for ypos in range(0, 601, 150):
            pygame.draw.line(SURFACE, 0x000000, (100, ypos),
                             (701, ypos), weight)
        # drawing stone
        draw_stone(SURFACE, field)
        SURFACE.blit(turn, turn_rect)
        SURFACE.blit(ct, ct_rect)
        SURFACE.blit(color, color_rect)
        pygame.display.update()
        FPSCLOCK.tick(3)
        if(x >= 0 and y >= 0):
            break


def main():
    """ define """
    # 4*4のオセロ
    # 空白＝０、　黒＝１、　白＝２
    global EMPTY
    EMPTY = 0
    global BLACK
    BLACK = 1
    global WHITE
    WHITE = 2
    global TURN
    TURN = 0
    global Player
    global Computer

    global field
    field = np.array([[0, 0, 0, 0],
                      [0, 2, 1, 0],
                      [0, 1, 2, 0],
                      [0, 0, 0, 0]])

    global field_address
    #                        　  a,    b,    c,    d
    field_address = np.array([["a1", "b1", "c1", "d1"],  # 1
                              ["a2", "b2", "c2", "d2"],  # 2
                              ["a3", "b3", "c3", "d3"],  # 3
                              ["a4", "b4", "c4", "d4"]])  # 4
    global offset_x
    offset_x = [-1, 0, 1]
    global offset_y
    offset_y = [-1, 0, 1]

    """ drawing title """
    sysfont_title = pygame.font.SysFont(None, 80)
    title = sysfont_title.render("othello(4×4).", True, (0, 0, 0))
    title_rect = title.get_rect()
    title_rect.center = (400, 200)
    sysfont_start = pygame.font.SysFont(None, 60)
    start = sysfont_start.render("start.", True, (255, 255, 255))
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

    """ drawing select first hand or late hand """
    bxpos, bypos = 250, 350
    wxpos, wypos = 550, 350
    radius = 100
    d = radius * 2  # diameter
    sysfont = pygame.font.SysFont(None, 60)
    select_black = sysfont.render("First hand.", True, (0, 0, 0))
    select_black_rect = select_black.get_rect()
    select_black_rect.center = (250, 200)
    select_white = sysfont.render("Late hand.", True, (0, 0, 0))
    select_white_rect = select_white.get_rect()
    select_white_rect.center = (550, 200)
    select_message = sysfont.render(
        "Select First hand or Late hand.", True, (0, 0, 0))
    select_message_rect = select_message.get_rect()
    select_message_rect.center = (400, 100)
    while(True):
        xpos = 0
        ypos = 0
        for event in pygame.event.get():
            if(event.type == QUIT):
                pygame.quit()
                sys.exit()
            if(event.type == MOUSEBUTTONDOWN and event.button == 1):
                xpos, ypos = event.pos[0], event.pos[1]
        # calculate radius
        br = np.sqrt((xpos - bxpos)**2 + (ypos - bypos)**2)
        wr = np.sqrt((xpos - wxpos)**2 + (ypos - wypos)**2)
        if(br <= radius):
            Player = BLACK
            Computer = WHITE
            TURN = Player
            break
        elif(wr <= radius):
            Player = WHITE
            Computer = BLACK
            TURN = Computer
            break
        # drawing background
        SURFACE.fill((255, 255, 255))
        # Rect
        pygame.draw.ellipse(SURFACE, (0, 0, 0),
                            ((bxpos-100, bypos-100), (d, d)))
        pygame.draw.ellipse(SURFACE, (0, 0, 0),
                            ((wxpos-100, wypos-100), (d, d)), 10)
        # Font
        SURFACE.blit(select_black, select_black_rect)
        SURFACE.blit(select_white, select_white_rect)
        SURFACE.blit(select_message, select_message_rect)
        pygame.display.update()
        FPSCLOCK.tick(3)

    num = 0
    before_field = copy.copy(field)
    after_field = copy.copy(field)
    while(True):
        """ pygame """
        for event in pygame.event.get():
            if(event.type == QUIT):
                pygame.quit()
                sys.exit()

        while(TURN != 0):
            """ othello(4x4) """
            while(TURN != 0):
                # 黒の手番
                if(TURN == BLACK):
                    point, offset_list = black_turn()
                    if(TURN == Player):
                        print("TURN : you")
                        if(point == (-1, -1)):  # pass判定
                            if((before_field == after_field).all()):
                                print("pass")
                                print("両者がpassのため対局を終了します")
                                TURN = 0
                                break
                            print("pass")
                            print(field)
                            print("")
                            TURN = WHITE
                            before_field = copy.copy(after_field)
                            after_field = copy.copy(field)
                            break
                        address = player_turn()
                        point = address2point(address)
                        offset_list = point2offset(point, Player)
                        if(not(address_check(point, TURN))):  # 反則負け
                            print("「{0}」は無効な手です。".format(address))
                            print("「先手（黒駒）」は反則により負けになります。")
                            print("勝者は「後手（白駒）」になります。")
                            print(field)
                            Player = 0
                            break
                    else:
                        print("TURN : computer")
                        if(point == (-1, -1)):
                            if((before_field == after_field).all()):  # pass判定
                                print("pass")
                                print("両者がpassのため対局を終了します")
                                TURN = 0
                                break
                            print("pass")
                            print(field)
                            print("")
                            TURN = WHITE
                            before_field = copy.copy(after_field)
                            after_field = copy.copy(field)
                            break
                        computer_turn()
                    field = update_field(TURN, point, offset_list)
                    pygame.display.update()
                    FPSCLOCK.tick(3)
                    TURN = WHITE
                    before_field = copy.copy(after_field)
                    after_field = copy.copy(field)
                    print("field")
                    print(field)
                    print("")
                # 白の手番
                elif(TURN == WHITE):
                    point, offset_list = white_turn()
                    if(TURN == Player):
                        print("TURN : you")
                        if(point == (-1, -1)):
                            if((before_field == after_field).all()):
                                print("両者がpassのため対局を終了します")
                                TURN = 0
                                break
                            print("pass")
                            print(field)
                            print("")
                            TURN = BLACK
                            before_field = copy.copy(after_field)
                            after_field = copy.copy(field)
                            break
                        address = player_turn()
                        point = address2point(address)
                        offset_list = point2offset(point, Player)
                        if(not(address_check(point, TURN))):  # 反則負け
                            print("「{0}」は無効な手です。".format(address))
                            print("「先手（黒駒）」は反則により負けになります。")
                            print("勝者は「後手（白駒）」になります。")
                            print(field)
                            TURN = 0
                            break
                    else:
                        print("TURN : computer")
                        if(point == (-1, -1)):
                            if((before_field == after_field).all()):
                                print("両者がpassのため対局を終了します")
                                TURN = 0
                                break
                            print("pass")
                            print(field)
                            print("")
                            TURN = BLACK
                            before_field = copy.copy(after_field)
                            after_field = copy.copy(field)
                            break
                        computer_turn()
                    field = update_field(TURN, point, offset_list)
                    pygame.display.update()
                    FPSCLOCK.tick(3)
                    TURN = BLACK
                    before_field = copy.copy(after_field)
                    after_field = copy.copy(field)
                    print("field")
                    print(field)
                    print("")
                else:
                    print("error : TURN is not BLACK and WHITE")
                    break

                #print(field)
                if(not(0 in field)):
                    show_result()
                    TURN = 0
                    break
            # othelloのwhile文　終了

        # drawing line
        SURFACE.fill((255, 255, 255))
        weight = 10
        for xpos in range(100, 701, 150):
            pygame.draw.line(SURFACE, 0x000000, (xpos, 0), (xpos, 601), weight)
        for ypos in range(0, 601, 150):
            pygame.draw.line(SURFACE, 0x000000, (100, ypos),
                             (701, ypos), weight)
        # drawing stone
        draw_stone(SURFACE, field)
        pygame.display.update()
        FPSCLOCK.tick(3)


if __name__ == '__main__':
    main()
