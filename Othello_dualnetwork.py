 # %%
from tensorflow.keras.layers import Dense, Activation, Dropout, Flatten, BatchNormalization, MaxPooling2D, GlobalMaxPooling2D, Conv2D, MaxPool2D, Add, Input,Softmax
from tensorflow.keras.utils import plot_model, to_categorical
from keras.callbacks import LearningRateScheduler, LambdaCallback
from tensorflow.keras import backend as K
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.regularizers import l2
from keras.datasets import cifar10
import tensorflow as tf
from keras.utils import plot_model
from tensorflow import keras
from keras.utils.vis_utils import plot_model
import os
import numpy as np
'''
モデルを構築する
'''
def policy_network():#外部からとってきたデータの学習用
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

def dual_network():#dualとか言っときながらsingle、最初は価値と方策を一緒にやろうとしてたんだ...
    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(8, 8,6)),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dense(1, activation='sigmoid')
    ])
    model.save('./model/latest2.h5')
    print("save")
RN_EPOCHS=20
def train_network(state_list,value_list):#実際にvalueNetworkを学習する
    #(-1,8,8,2)
    print(state_list.shape)
    state_list = state_list.transpose(0,2,3,1)
    print(state_list.shape)
    model=load_model("./model/latest2.h5")
    model.compile(loss='mse', optimizer='adam')
    print(value_list.shape)
    print("start")
    model.fit(state_list, value_list, epochs=RN_EPOCHS)
    model.save('./model/latest2.h5')
    print("save")
    #K.clear_session()
    #del model
# %%
if __name__=='__main__':
    #dual_network()
    #policy_network()
    '''モデル可視化
    model = load_model('./model/latest2.h5')
    print(model.summary())
    from tensorflow.keras.utils import plot_model
    plot_model(
        model,
        to_file='model.png',
        show_shapes=True,
    )
    '''
# %%
