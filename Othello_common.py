'''from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPool2D

from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Dense, Activation, Dropout, Flatten, BatchNormalization
from tensorflow.keras.utils import plot_model, to_categorical
from keras.callbacks import TensorBoard

from keras.datasets import cifar10

import tensorflow as tf
from tensorflow import keras'''

# ヘルパーライブラリのインポート
import numpy as np
import matplotlib.pyplot as plt
# State class
class State:
    def __init__(self,state=None):
        self.state=state
        #initiate Othello state
        #White:1 Black:2
        if(self.state==None):
            self.state=np.zeros([8,8])
            self.state[3][3]=1
            self.state[4][4]=1
            self.state[3][4]=2
            self.state[4][3]=2
    def piece_num(self):
        white=0
        black=0
        for h in range(8):
            for w in range(8):
                if(self.state[h][w]==1):
                    white+=1
                if(self.state[h][w]==2):
                    black+=1
        return white,black
    def is_win(self):
        w,b=self.piece_num()
        return w>=b
    def is_finished(self):
        possible_hand=self.possible_state_list
        return len(possible_hand)==0
    def corner_state(self):
        res=np.zeros([8,8])
        if(self.state[0][0]==1):
            nowx=0
            nowy=0
            while((self.state[nowx][0]==1)):
                res[nowx][0]=1
                nowx+=1
                if(nowx==8):
                    break
            while((self.state[0][nowy]==1)):
                res[0][nowy]=1
                nowy+=1
                if(nowy==8):
                    break
            nowx=0
            nowy=0
            while((self.state[nowx][nowy]==1)):
                res[nowx][nowy]=1
                nowx+=1
                nowy+=1
                if(nowy==8):
                    break
        if(self.state[7][0]==1):
            nowx=7
            nowy=0
            while((self.state[nowx][0]==1)):
                res[nowx][0]=1
                nowx-=1
                if(nowx==-1):
                    break
            while((self.state[7][nowy]==1)):
                res[7][nowy]=1
                nowy+=1
                if(nowy==8):
                    break
            nowx=7
            nowy=0
            while((nowy<8)&(self.state[nowx][nowy]==1)):
                res[nowx][nowy]=1
                nowx-=1
                nowy+=1
                if(nowy==8):
                    break
        if(self.state[0][7]==1):
            nowx=0
            nowy=7
            while((self.state[nowx][7]==1)):
                res[nowx][7]=1
                nowx+=1
                if(nowx==8):
                    break
            while((self.state[0][nowy]==1)):
                res[0][nowy]=1
                nowy-=1
                if(nowy==-1):
                    break
            nowx=0
            nowy=7
            while((nowx<8)&(self.state[nowx][nowy]==1)):
                res[nowx][nowy]=1
                nowx+=1
                nowy-=1
                if(nowx==8):
                    break
        if(self.state[7][7]==1):
            nowx=7
            nowy=7
            while((self.state[nowx][7]==1)):
                res[nowx][7]=1
                nowx-=1
                if(nowx==-1):
                    break
            while((self.state[7][nowy]==1)):
                res[7][nowy]=1
                nowy-=1
                if(nowy==-1):
                    break
            nowx=7
            nowy=7
            while((nowx>=0)&(self.state[nowx][nowy]==1)):
                res[nowx][nowy]=1
                nowx-=1
                nowy-=1
                if(nowx==-1):
                    break
        return res

    def possible_state(self):
        dx=[1,1,1,0,-1,-1,-1,0]
        dy=[-1,0,1,1,1,0,-1,-1]
        possible_1=np.zeros([8,8])
        possible_2=np.zeros([8,8])
        possible_hand_1=np.zeros([8,8])
        possible_hand_2=np.zeros([8,8])
        for h in range(8):
            for w in range(8):
                num=1
                if(self.state[h][w]!=num):
                    continue
                for lx,ly in zip(dx,dy):
                    nowh=h+lx
                    noww=w+ly
                    flag=False
                    possible_lists=[]
                    while(True):
                        if((nowh<0)|(nowh>=8)|(noww<0)|(noww>=8)):
                            break
                        if(self.state[nowh][noww]==num):
                            break
                        elif(self.state[nowh][noww]==3-num):
                            possible_lists.append(nowh*8+noww)
                        else:
                            if(len(possible_lists)>=1):
                                possible_hand_1[nowh][noww]=1
                            flag=True
                            break
                        nowh+=lx
                        noww+=ly
                    if(flag):
                        for possible in possible_lists:
                            possible_1[int(possible//8)][int(possible%8)]=1
            
        for h in range(8):
            for w in range(8):
                num=2
                if(self.state[h][w]!=num):
                    continue
                for lx,ly in zip(dx,dy):
                    nowh=h+lx
                    noww=w+ly
                    flag=False
                    possible_lists=[]
                    while(True):
                        if((nowh<0)|(nowh>=8)|(noww<0)|(noww>=8)):
                            break
                        if(self.state[nowh][noww]==num):
                            break
                        elif(self.state[nowh][noww]==3-num):
                            possible_lists.append(nowh*8+noww)
                        else:
                            if(len(possible_lists)>=1):
                                possible_hand_2[nowh][noww]=1
                            flag=True
                            break
                        nowh+=lx
                        noww+=ly
                    if(flag):
                        for possible in possible_lists:
                            possible_2[int(possible//8)][int(possible%8)]=1
        return possible_1,possible_2,possible_hand_1,possible_hand_2
    def possible_state_list(self,turn):
        if(turn):
            self.state=(3-self.state)%3
        _,_,possible,_=self.possible_state()
        possibles=[]
        dx=[1,1,1,0,-1,-1,-1,0]
        dy=[-1,0,1,1,1,0,-1,-1]
        for h in range(8):
            for w in range(8):
                if(possible[h][w]==1):
                    result=state
                    for lx,ly in zip(dx,dy):
                        possible_lists=[]
                        flag=False
                        nowh=h+lx
                        noww=w+ly
                        while(True):
                            if((nowh<0)|(nowh>=8)|(noww<0)|(noww>=8)):
                                break
                            if(self.state[nowh][noww]==0):
                                break
                            elif(self.state[nowh][noww]==2):
                                possible_lists.append(nowh*8+noww)
                            else:
                                flag=True
                                break
                            nowh+=lx
                            noww+=ly
                        if(flag): 
                            for i in possible_lists:
                                result[i//8][i%8]=1
                    if(turn):
                        state=(3-state)%3
                    possibles.append(result)
        return possibles
    def next_state(self,actionh,actionw,tuen):
        if(turn):
            self.state=(3-self.state)%3
        
        if(turn):
            self.state=(3-self.state)%3
    def playout_policy(self):
        return 1
