 # %%
from tensorflow.keras.layers import Dense, Activation, Dropout, Flatten, BatchNormalization, MaxPooling2D, GlobalMaxPooling2D, Conv2D, MaxPool2D, Add, Input,Softmax
from tensorflow.keras.utils import plot_model, to_categorical
from keras.callbacks import LearningRateScheduler, LambdaCallback
from tensorflow.keras import backend as K
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.regularizers import l2
from keras.datasets import cifar10
import tensorflow as tf
from tensorflow import keras
import os
import numpy as np
FILTERS_num=128
BLOCKS_num=20
INPUT_shape=(8,8,2)
OUTPUT_size=64

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


def policy_network():


    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(8, 8,2)),
        keras.layers.BatchNormalization(axis=1, momentum=0.99, epsilon=0.001),
        keras.layers.Dense(512, activation='relu'),
        keras.layers.BatchNormalization(axis=1, momentum=0.99, epsilon=0.001),
        keras.layers.Dense(1024, activation='relu'),
        keras.layers.BatchNormalization(axis=1, momentum=0.99, epsilon=0.001),
        keras.layers.Dense(512, activation='relu'),
        keras.layers.BatchNormalization(axis=1, momentum=0.99, epsilon=0.001),
        keras.layers.Dense(256, activation='relu'),
        keras.layers.BatchNormalization(axis=1, momentum=0.99, epsilon=0.001),
        keras.layers.Dense(64, activation='softmax')
    ])
    os.makedirs('./model/', exist_ok=True)
    model.save('./model/policy_model.h5')
    print("save")

def dual_network():
    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(8, 8,2)),
        keras.layers.BatchNormalization(axis=1, momentum=0.99, epsilon=0.001),
        keras.layers.Dense(512, activation='sigmoid'),
        keras.layers.BatchNormalization(axis=1, momentum=0.99, epsilon=0.001),
        keras.layers.Dense(1024, activation='sigmoid'),
        keras.layers.BatchNormalization(axis=1, momentum=0.99, epsilon=0.001),
        keras.layers.Dense(512, activation='sigmoid'),
        keras.layers.BatchNormalization(axis=1, momentum=0.99, epsilon=0.001),
        keras.layers.Dense(256, activation='sigmoid'),
        keras.layers.BatchNormalization(axis=1, momentum=0.99, epsilon=0.001),
        keras.layers.Dense(1, activation='sigmoid')
    ])
    model.save('./model/latest.h5')
    print("save")
RN_EPOCHS=10



def train_network(state_list,value_list):
    #(500,8,8,2)
    print(state_list.shape)
    #policy_list=to_categorical(policy_list,65)
    #print(policy_list.shape)
    state_list = state_list.transpose(0,2,3,1)
    print(state_list.shape)
    model=load_model("./model/latest.h5")
    model.compile(loss='mse', optimizer='adam')
    print(value_list.shape)
    print("start")
    model.fit(state_list, value_list, epochs=RN_EPOCHS)
    model.save('./model/latest.h5')
    print("save")
    #K.clear_session()
    #del model
if __name__=='__main__':
    dual_network()

# %%
