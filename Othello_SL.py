import Othello_common
import numpy as np
import matplotlib.pyplot as plt
import random
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPool2D
from tensorflow.keras.layers import Add
from tensorflow.keras.layers import Input
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Dense, Activation, Dropout, Flatten, BatchNormalization, MaxPooling2D, GlobalMaxPooling2D
from tensorflow.keras.utils import plot_model, to_categorical
from keras.callbacks import TensorBoard
from tensorflow.keras.models import Model
from tensorflow.keras.regularizers import l2
from keras.datasets import cifar10
import tensorflow as tf
from tensorflow import keras
import os

#勝負が決まる条件
#すでに相手に合法手がないときに自分の合法手もないとき

#(500,8,8,2)->[(1),(64)]

#(State,keras.model)->State
def SLpolicy_selfplay(nowstate,model):
    is_terminated=False
    while(True):
        _,p_hands=nowstate.possible_state()
        if((is_terminated) & (len(p_hands) == 0)):
            break
        if(len(p_hands) == 0):
            is_terminated = True
            nowstate = Othello_common.State(3-nowstate.turn, nowstate.state)
            continue
        temp_state1 = np.where(nowstate.state == 1, 1, 0)
        temp_state2 = np.where(nowstate.state == 2, 1, 0)
        #後手番時は入れ替えることで対処
        if nowstate.turn==2:
            temp_state1,temp_state2=temp_state2,temp_state1
        test = [temp_state1, temp_state2]
        test = np.array(test)
        test = test.transpose(1, 2, 0)
        result = model.predict(test)[0]
        result = np.argsort(result)
        res_action=0
        #合法手の中でSLポリシーの最も高い行動を選択していくわよ
        for i in range(result):
            if i in p_hands:
                res_action=i
        nowstate=Othello_common.State(3-nowstate.turn,nowstate.next_state(res_action))
    return nowstate

#先手model1.後手model2とし、互いに戦わせることでどちらが強いか調べる
#(keras.model,keras.model)->(State)
def SLpolicy_compete_selfplay(model1,model2):
    nowstate=Othello_common.State(1)
    is_terminated = False
    while(True):
        _, p_hands = nowstate.possible_state()
        if((is_terminated) & (len(p_hands) == 0)):
            break
        if(len(p_hands) == 0):
            is_terminated = True
            nowstate = Othello_common.State(3-nowstate.turn, nowstate.state)
            continue
        temp_state1 = np.where(nowstate.state == 1, 1, 0)
        temp_state2 = np.where(nowstate.state == 2, 1, 0)
        #後手番時は入れ替えることで対処
        if nowstate.turn == 2:
            temp_state1, temp_state2 = temp_state2, temp_state1
        test = [temp_state1, temp_state2]
        test = np.array(test)
        test = test.transpose(1, 2, 0)
        result=0
        if nowstate.turn == 1:
            result=model1.predict(test)
        else:
            result=model2.predict(test)
        res_action = 0
        #合法手の中でSLポリシーの最も高い行動を選択していくわよ
        for i in range(result):
            if i in p_hands:
                res_action = i
        nowstate = Othello_common.State(
            3-nowstate.turn, nowstate.next_state(res_action))
    #あいこ以上だったらTrue
    return nowstate.is_win()>=0.5
#自己対戦(ランダム)
#nowstate指定なしで最初から、play_num指定なしで最後まで自己対戦
def selfplay(nowstate=None,play_num=1000):
    is_terminated=False
    if (play_num<0)|(play_num>32)&(play_num!=1000):
        return None
    if nowstate is None:
        nowstate=Othello_common.State(1)
    #仕様上先手番を返したいのでplay_numは偶数にする
    play_num*=2
    index=0
    while(True):
        index+=1
        if __name__ == '__main__':
            print(index, nowstate.turn)
            print(nowstate.str_show())
            print(nowstate.piece_num())
        if(index==play_num):
            break
        _,possible_list=nowstate.possible_state()
        #終了条件
        if((is_terminated) & (len(possible_list)==0)):
            break
        if(len(possible_list)==0):
            is_terminated=True
            #先後をかえるだけ
            nowstate = Othello_common.State(3-nowstate.turn, nowstate.state)
            continue
        is_terminated = False
        #ランダムで次の手を選択
        nextstate=nowstate.next_state(nowstate.random_action())
        #状態更新
        nowstate=Othello_common.State(3-nowstate.turn,nextstate)
    return nowstate
if __name__=='__main__':
    
    k=selfplay(play_num=10)
    print("hello")
    print(k.str_show())
