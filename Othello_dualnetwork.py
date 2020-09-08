from tensorflow.keras.layers import Dense, Activation, Dropout, Flatten, BatchNormalization, MaxPooling2D, GlobalMaxPooling2D, Conv2D, MaxPool2D, Add, Input
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
    print(p.shape,v.shape)
    model=Model(inputs=input,outputs=[p,v])
    os.makedirs('./model/',exist_ok=True)
    model.save('./model/best.h5')
RN_EPOCHS=10

def train_network(state_list,value_list,policy_list):
    #(500,8,8,2)
    print(state_list.shape)
    policy_list=to_categorical(policy_list,65)
    print(policy_list.shape)
    state_list = state_list.transpose(0,2,3,1)
    print(state_list.shape)
    model=load_model("./model/best.h5")
    model.compile(loss=['categorical_crossentropy','mse'], optimizer='adam')
    print(policy_list.shape)
    print(value_list.shape)
    '''def step_decay(epoch):
        x=0.001
        if epoch>=50:
            x=0.0005
        if epoch>=80:
            x=0.00025
        return x
    lr_decay=LearningRateScheduler(step_decay)
    '''
    print("start")
    model.fit(state_list, [policy_list,value_list],
              batch_size=FILTERS_num, epochs=RN_EPOCHS)
    model.save('/model/latest.h5')
    K.clear__session()
    del model
if __name__=='__main__':
    dual_network()
