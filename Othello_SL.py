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

def selfplay_RL(nowstate=None,play_num=1000):
    is_terminated = False
    if (play_num < 0) | (play_num > 32) & (play_num != 1000):
        return None
    if nowstate is None:
        nowstate = Othello_common.State(1)
    index = 0
    finished = True
    while(index != play_num):
        index += 1
        if __name__ == '__main__':
            print(index, nowstate.turn)
            print(nowstate.str_show())
            print(nowstate.piece_num())
        _, possible_list = nowstate.possible_state()
        if((is_terminated) & (len(possible_list) == 0)):
            print(nowstate.is_win())
            finished = False
            break
        if(len(possible_list) == 0):
            print("passed")
            is_terminated = True
            nowstate = Othello_common.State(3-nowstate.turn, nowstate.state)
            continue
        is_terminated = False
        nextstate = nowstate.next_state(nowstate.random_action())
        nowstate = Othello_common.State(3-nowstate.turn, nextstate)
    if finished:
        return nowstate
    else:
        return None
def selfplay(nowstate=None,play_num=1000):
    is_terminated=False
    if (play_num<0)|(play_num>32)&(play_num!=1000):
        return None
    if nowstate is None:
        nowstate=Othello_common.State(1)
    index=0
    finished=True
    while(index!=play_num):
        index+=1
        if __name__ == '__main__':
            print(index, nowstate.turn)
            print(nowstate.str_show())
            print(nowstate.piece_num())
        _,possible_list=nowstate.possible_state()
        if((is_terminated) & (len(possible_list)==0)):
            print(nowstate.is_win())
            finished=False
            break
        if(len(possible_list)==0):
            print("passed")
            is_terminated=True
            nowstate = Othello_common.State(3-nowstate.turn, nowstate.state)
            continue
        is_terminated = False
        nextstate=nowstate.next_state(nowstate.random_action())
        nowstate=Othello_common.State(3-nowstate.turn,nextstate)
    if finished:
        return nowstate
    else:
        return None
if __name__=='__main__':
    print("hello")
    selfplay(play_num=10)
