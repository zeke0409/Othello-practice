
# ヘルパーライブラリのインポート
import numpy as np
import matplotlib.pyplot as plt
import random
import copy

# State class
# 基本的に白視点
# turnの手番時の盤面を想定

#置くことのできる盤面を返す
def possible_state(state_1, state_2):
    dx = [1, 1, 1, 0, -1, -1, -1, 0]
    dy = [-1, 0, 1, 1, 1, 0, -1, -1]
    possible_1 = np.zeros([8, 8])
    possible_2 = np.zeros([8, 8])
    state = np.zeros([8, 8])
    for i in range(8):
        for j in range(8):
            if state_1[i][j] == 1:
                state[i][j] = 1
            elif state_2[i][j] == 1:
                state[i][j] = 2
    num = 1
    for h in range(8):
        for w in range(8):
            if(state[h][w] != 0):
                continue
            for lx, ly in zip(dx, dy):
                nowh = h+lx
                noww = w+ly
                flag = False
                possible_lists = []
                while(True):
                    if((nowh < 0) | (nowh >= 8) | (noww < 0) | (noww >= 8)):
                        break
                    if(state[nowh][noww] == num):
                        if(len(possible_lists) >= 1):
                            flag = True
                        break
                    elif(state[nowh][noww] == 3-num):
                        possible_lists.append(nowh*8+noww)
                    else:
                        break
                    nowh += lx
                    noww += ly
                if(flag):
                    break
            if(flag):
                possible_1[h][w] = 1
    num = 2
    for h in range(8):
        for w in range(8):
            if(state[h][w] != 0):
                continue
            for lx, ly in zip(dx, dy):
                nowh = h+lx
                noww = w+ly
                flag = False
                possible_lists = []
                while(True):
                    if((nowh < 0) | (nowh >= 8) | (noww < 0) | (noww >= 8)):
                        break
                    if(state[nowh][noww] == num):
                        if(len(possible_lists) >= 1):
                            flag = True
                        break
                    elif(state[nowh][noww] == 3-num):
                        possible_lists.append(nowh*8+noww)
                    else:
                        break
                    nowh += lx
                    noww += ly
                if(flag):
                    break
            if(flag):
                possible_2[h][w] = 1
    return possible_1, possible_2
#あまりやりたくなかった...端より(1,1)離れている場所に石を置くのは、相手に端に石を置かせるのと同義としてみただけ
def emergence_state(state1,state2):
    if(state1[7][7]==0&state2[7][7]==0):
        state1[7][7]=state2[6][6]
    if(state1[0][0]==0&state2[0][0]==0):
        state1[0][0]=state2[1][1]
    if(state1[7][0]==0&state2[7][0]==0):
        state1[7][0]=state2[6][1]
    if(state1[0][7] == 0&state1[0][7]==0):
        state1[0][7] = state2[1][6]
#初期化 State state(先手(1)か後手(2)か,state(np.array([8,8]))(未指定の場合最初から))
class State:
    #state np(8*8)
    def __init__(self,turn,state=None):
        self.state = state
        self.turn = turn
        self.temp_possible_hand=[]
        self.play_out=10
        self.temp_possible1=np.zeros([8,8])
        #initiate Othello state
        #White:1 Black:2
        if state is None:
            self.state = np.zeros([8, 8])
            self.state[3][3] = 1
            self.state[4][4] = 1
            self.state[3][4] = 2
            self.state[4][3] = 2
            
    #現在の白、黒のコマ数を返す
    def piece_num(self):
        white = 0
        black = 0
        for h in range(8):
            for w in range(8):
                if(self.state[h][w] == 1):
                    white += 1
                if(self.state[h][w] == 2):
                    black += 1
        return white, black
    #白が勝っているかを返す
    def is_win(self):
        w, b = self.piece_num()
        if w>b:
            return 1
        elif b>w:
            return 0
        else:
            return 0.5

    def is_finished(self):
        _,possible_hand = self.possible_state()
        return len(possible_hand) == 0
    
    def str_show(self):
        for i in range(8):
            for j in range(8):
                if(self.state[i][j]==1):
                    print('o',end='')
                elif(self.state[i][j]==2):
                    print('x',end='')
                else:
                    print('-',end='')
            print('')
        print()
    #絶対にひっくりかえせない盤面を返す
    #->np.array(8*8)
    def corner_state(self):
        res = np.zeros([8, 8])
        if(self.state[0][0] == self.turn):
            nowx = 0
            nowy = 0
            while((self.state[nowx][0] == self.turn)):
                res[nowx][0] = 1
                nowx += 1
                if(nowx == 8):
                    break
            while((self.state[0][nowy] == self.turn)):
                res[0][nowy] = 1
                nowy += 1
                if(nowy == 8):
                    break
            nowx = 0
            nowy = 0
            while((self.state[nowx][nowy] == self.turn)):
                res[nowx][nowy] = 1
                nowx += 1
                nowy += 1
                if(nowy == 8):
                    break
        if(self.state[7][0] == self.turn):
            nowx = 7
            nowy = 0
            while((self.state[nowx][0] == self.turn)):
                res[nowx][0] = 1
                nowx -= 1
                if(nowx == -1):
                    break
            while((self.state[7][nowy] == self.turn)):
                res[7][nowy] = 1
                nowy += 1
                if(nowy == 8):
                    break
            nowx = 7
            nowy = 0
            while((nowy < 8) & (self.state[nowx][nowy] == self.turn)):
                res[nowx][nowy] = 1
                nowx -= 1
                nowy += 1
                if(nowy == 8):
                    break
        if(self.state[0][7] == self.turn):
            nowx = 0
            nowy = 7
            while((self.state[nowx][7] == self.turn)):
                res[nowx][7] = 1
                nowx += 1
                if(nowx == 8):
                    break
            while((self.state[0][nowy] == self.turn)):
                res[0][nowy] = 1
                nowy -= 1
                if(nowy == -1):
                    break
            nowx = 0
            nowy = 7
            while((nowx < 8) & (self.state[nowx][nowy] == self.turn)):
                res[nowx][nowy] = 1
                nowx += 1
                nowy -= 1
                if(nowx == 8):
                    break
        if(self.state[7][7] == self.turn):
            nowx = 7
            nowy = 7
            while((self.state[nowx][7] == self.turn)):
                res[nowx][7] = 1
                nowx -= 1
                if(nowx == -1):
                    break
            while((self.state[7][nowy] == self.turn)):
                res[7][nowy] = 1
                nowy -= 1
                if(nowy == -1):
                    break
            nowx = 7
            nowy = 7
            while((nowx >= 0) & (self.state[nowx][nowy] == self.turn)):
                res[nowx][nowy] = 1
                nowx -= 1
                nowy -= 1
                if(nowx == -1):
                    break
        return res
    
    #その盤面における合法手を返す
    # ->np.array(8*8),list
    def possible_state(self):
        if(len(self.temp_possible_hand)!=0):
            return self.temp_possible1,self.temp_possible_hand
        dx = [1, 1, 1, 0, -1, -1, -1, 0]
        dy = [-1, 0, 1, 1, 1, 0, -1, -1]
        possible_1 = np.zeros([8,8])
        num = self.turn
        possible_hand_list = []
        for h in range(8):
            for w in range(8):
                if(self.state[h][w] != 0):
                    continue
                for lx, ly in zip(dx, dy):
                    nowh = h+lx
                    noww = w+ly
                    flag = False
                    possible_lists = []
                    while(True):
                        if((nowh < 0) | (nowh >= 8) | (noww < 0) | (noww >= 8)):
                            break
                        if(self.state[nowh][noww] == num):
                            if(len(possible_lists) >= 1):
                                flag = True
                            break
                        elif(self.state[nowh][noww] == 3-num):
                            possible_lists.append(nowh*8+noww)
                        else:
                            break
                        nowh += lx
                        noww += ly
                    if(flag):
                        break
                if(flag):
                    possible_hand_list.append(h*8+w)
                    possible_1[h][w] = 1
        self.temp_possible1=possible_1
        self.temp_possible_hand=possible_hand_list
        return possible_1, possible_hand_list

    #手に対しての結果盤面を返す
    # ->np.array(8,8)
    def next_state(self, action):
        _, lists = self.possible_state()
        actionh=action//8
        actionw=action%8
        if not(action in lists):
            print("ERROR! next_state invalid hand")
            return -1
        num=self.turn
        dx = [1, 1, 1, 0, -1, -1, -1, 0]
        dy = [-1, 0, 1, 1, 1, 0, -1, -1]
        result=self.state.copy()
        result[actionh][actionw]=num
        for lx, ly in zip(dx, dy):
            nowh = actionh+lx
            noww = actionw+ly
            flag = False
            possible_lists = []
            while(True):
                if((nowh < 0) | (nowh >= 8) | (noww < 0) | (noww >= 8)):
                    break
                if(self.state[nowh][noww] == num):
                    flag = True
                    break
                elif(self.state[nowh][noww] == 3-num):
                    possible_lists.append(nowh*8+noww)
                else:
                    break
                nowh += lx
                noww += ly
            if(flag):
                for possible in possible_lists:
                    result[int(possible//8)][int(possible % 8)] = num
        return result
    
    #適当な手を返す
    #->int(h*8+w)
    def random_action(self):
        _,rand=self.possible_state()
        random.shuffle(rand)
        a = random.choice(rand)
        return a
    #学習済みバリューネットワークからの
    
    def playout_policy(self,model1):
        if self.play_out != 10:
            return self.play_out
        final_list=[]
        
        
        res1, res2 = self.unchangeable_state()
        p1, p2 = possible_state(np.where(self.state == 1, 1, 0),
                                    np.where(self.state == 2, 1, 0))
        state1=copy.copy(np.where(self.state == 1, 1, 0))
        state2=copy.copy(np.where(self.state == 2, 1, 0))
        emergence_state(state1,state2)
        emergence_state(state2,state1)
        test_state = np.array([state1,state2,res1,res2,p1,p2])
        test_state=test_state[np.newaxis,:,:,:]
        test_state=test_state.transpose(0,2,3,1)
        res = model1.predict(test_state)

        test_state2 = np.array([state2,state1,res2,res1,p2,p1])
        test_state2=test_state2[np.newaxis,:,:,:]
        test_state2=test_state2.transpose(0,2,3,1)
        res2 = model1.predict(test_state2)
        #final_list.append(res)
            #self.state=np.rot90(self.state)
        #final_res=statistics.median(final_list)
        self.play_out=res+(1-res2)
        return self.play_out
    def is_possible_hand(self):
        _, rand = self.possible_state()
        return len(rand)==0
    def unchangeable_state(self):
        res1=np.zeros([8,8])
        res2 = np.zeros([8, 8])
        for rotate_num in range(4):
            for h in range(8):
                if self.state[h][0]!=1:
                    break
                for w in range(8):
                    if (h!=0) and (res1[h-1][w]!=1):
                        break
                    if self.state[h][w]!=1:
                        break
                    res1[h][w]=1
            res1=np.rot90(res1)
            self.state=np.rot90(self.state)
        for rotate_num in range(4):
            for h in range(8):
                if self.state[h][0] != 2:
                    break
                for w in range(8):
                    if (h != 0) and (res2[h-1][w] != 2):
                        break
                    if self.state[h][w] != 2:
                        break
                    res2[h][w] = 1
            res2 = np.rot90(res2)
            self.state = np.rot90(self.state)
        return res1,res2
