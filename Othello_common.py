from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPool2D

from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Dense, Activation, Dropout, Flatten, BatchNormalization
from tensorflow.keras.utils import plot_model, to_categorical
from keras.callbacks import TensorBoard

from keras.datasets import cifar10

import tensorflow as tf
from tensorflow import keras

# ヘルパーライブラリのインポート
import numpy as np
import matplotlib.pyplot as plt

def corner_state(old_state):
    res=np.zeros([8,8])
    if(old_state[0][0]==1):
        nowx=0
        nowy=0
        while((old_state[nowx][0]==1)):
            res[nowx][0]=1
            nowx+=1
            if(nowx==8):
                break
        while((old_state[0][nowy]==1)):
            res[0][nowy]=1
            nowy+=1
            if(nowy==8):
                break
        nowx=0
        nowy=0
        while((old_state[nowx][nowy]==1)):
            res[nowx][nowy]=1
            nowx+=1
            nowy+=1
            if(nowy==8):
                break
    if(old_state[7][0]==1):
        nowx=7
        nowy=0
        while((old_state[nowx][0]==1)):
            res[nowx][0]=1
            nowx-=1
            if(nowx==-1):
                break
        while((old_state[7][nowy]==1)):
            res[7][nowy]=1
            nowy+=1
            if(nowy==8):
                break
        nowx=7
        nowy=0
        while((nowy<8)&(old_state[nowx][nowy]==1)):
            res[nowx][nowy]=1
            nowx-=1
            nowy+=1
            if(nowy==8):
                break
    if(old_state[0][7]==1):
        nowx=0
        nowy=7
        while((old_state[nowx][7]==1)):
            res[nowx][7]=1
            nowx+=1
            if(nowx==8):
                break
        while((old_state[0][nowy]==1)):
            res[0][nowy]=1
            nowy-=1
            if(nowy==-1):
                break
        nowx=0
        nowy=7
        while((nowx<8)&(old_state[nowx][nowy]==1)):
            res[nowx][nowy]=1
            nowx+=1
            nowy-=1
            if(nowx==8):
                break
    if(old_state[7][7]==1):
        nowx=7
        nowy=7
        while((old_state[nowx][7]==1)):
            res[nowx][7]=1
            nowx-=1
            if(nowx==-1):
                break
        while((old_state[7][nowy]==1)):
            res[7][nowy]=1
            nowy-=1
            if(nowy==-1):
                break
        nowx=7
        nowy=7
        while((nowx>=0)&(old_state[nowx][nowy]==1)):
            res[nowx][nowy]=1
            nowx-=1
            nowy-=1
            if(nowx==-1):
                break
    return res

def possible_state(old_state):
    dx=[1,1,1,0,-1,-1,-1,0]
    dy=[-1,0,1,1,1,0,-1,-1]
    possible_1=np.zeros([8,8])
    possible_2=np.zeros([8,8])
    possible_hand_1=np.zeros([8,8])
    possible_hand_2=np.zeros([8,8])
    for h in range(8):
        for w in range(8):
            num=1
            if(old_state[h][w]!=num):
                continue
            for lx,ly in zip(dx,dy):
                nowh=h+lx
                noww=w+ly
                flag=False
                possible_lists=[]
                while(True):
                    if((nowh<0)|(nowh>=8)|(noww<0)|(noww>=8)):
                        break
                    if(old_state[nowh][noww]==num):
                        break
                    elif(old_state[nowh][noww]==3-num):
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
            if(old_state[h][w]!=num):
                continue
            for lx,ly in zip(dx,dy):
                nowh=h+lx
                noww=w+ly
                flag=False
                possible_lists=[]
                while(True):
                    if((nowh<0)|(nowh>=8)|(noww<0)|(noww>=8)):
                        break
                    if(old_state[nowh][noww]==num):
                        break
                    elif(old_state[nowh][noww]==3-num):
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