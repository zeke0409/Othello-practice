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
import numpy as np
FILTERS_num=128
BLOCKS_num=20
INPUT_shape=(8,8,2)
OUTPUT_size=65

def conv(filters):
    return Conv2D(filters,3,padding='same',use_bias=False)
def residual_block():
    def f(x):
        sc=x
        x=conv(FILTERS_num)(x)
        x=BatchNormalization()(x)
        x=Activation('relu')(x)
        x = conv(FILTERS_num)(x)
        x=BatchNormalization()(x)
        x=Add()([x,sc])
        x=Activation('relu')(x)
        return x
    return f
def dual_network():
    input=Input(shape=INPUT_shape)
    print(input.shape)
    x=conv(FILTERS_num)(input)
    print(x.shape)
    x=BatchNormalization()(x)
    x=Activation('relu')(x)
    print(x.shape)
    for i in range(BLOCKS_num):
        x=residual_block()(x)
    x=GlobalMaxPooling2D()(x)
    p=Dense(OUTPUT_size)(x)
    v = Dense(1, kernel_regularizer=l2(0.005),activation='tanh')(x)
    print(type(p),type(v))
    model=Model(inputs=input,outputs=[p,v])
    os.makedirs('./model/',exist_ok=True)
    model.save('./model/best.h5')

def train_network(state_list,value_list,policy_list):
    a,b,c=INPUT_shape
    #white state
    state_list_1 = np.where(state_list == 1, 1, 0)
    #black state
    state_list_2 = np.where(state_list == 2, 1, 0)

if __name__=='__main__':
    dual_network()
