import numpy as np
class Process():
    def __init__(self):
        self.field = np.zeros((8, 8))
        self.field[4][4] = 1
        self.field[3][3] = 1
        self.field[4][3] = 2
        self.field[3][4] = 2

    def Othello_input(self, x, y):
        if(x==-1000):
            return self.field,-2
        if((x<0)|(x>=8)|(y<0)|(y>=8)):
            return self.field,-1
        return self.field,1

    def possible_state(self):
        dx = [1, 1, 1, 0, -1, -1, -1, 0]
        dy = [-1, 0, 1, 1, 1, 0, -1, -1]
        possible_1 = np.zeros([8, 8])
        possible_2 = np.zeros([8, 8])
        possible_hand_1 = np.zeros([8, 8])
        possible_hand_2 = np.zeros([8, 8])
        for h in range(8):
            for w in range(8):
                num = 1
                if(self.field[h][w] != num):
                    continue
                for lx, ly in zip(dx, dy):
                    nowh = h+lx
                    noww = w+ly
                    flag = False
                    possible_lists = []
                    while(True):
                        if((nowh < 0) | (nowh >= 8) | (noww < 0) | (noww >= 8)):
                            break
                        if(self.field[nowh][noww] == num):
                            break
                        elif(self.field[nowh][noww] == 3-num):
                            possible_lists.append(nowh*8+noww)
                        else:
                            if(len(possible_lists) >= 1):
                                possible_hand_1[nowh][noww] = 1
                            flag = True
                            break
                        nowh += lx
                        noww += ly
                    if(flag):
                        for possible in possible_lists:
                            possible_1[int(possible//8)][int(possible % 8)] = 1

        for h in range(8):
            for w in range(8):
                num = 2
                if(self.field[h][w] != num):
                    continue
                for lx, ly in zip(dx, dy):
                    nowh = h+lx
                    noww = w+ly
                    flag = False
                    possible_lists = []
                    while(True):
                        if((nowh < 0) | (nowh >= 8) | (noww < 0) | (noww >= 8)):
                            break
                        if(self.field[nowh][noww] == num):
                            break
                        elif(self.field[nowh][noww] == 3-num):
                            possible_lists.append(nowh*8+noww)
                        else:
                            if(len(possible_lists) >= 1):
                                possible_hand_2[nowh][noww] = 1
                            flag = True
                            break
                        nowh += lx
                        noww += ly
                    if(flag):
                        for possible in possible_lists:
                            possible_2[int(possible//8)][int(possible % 8)] = 1
        return possible_1, possible_2, possible_hand_1, possible_hand_2
