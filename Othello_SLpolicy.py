# %%

import Othello_common
import Othello_SL
from tensorflow.keras.utils import plot_model, to_categorical
from tensorflow.keras.models import Model, load_model
import tensorflow as tf
from tensorflow import keras

# ヘルパーライブラリのインポート
import numpy as np
import matplotlib.pyplot as plt


print(tf.__version__)

# %%
'''
import sys
import pprint
pprint.pprint(sys.path)
'''

#鏡反転
def new_action(action):
    new_grid_basex = action//8-3.5
    new_grid_basey = action % 8-3.5
    return (-new_grid_basex+3.5)*8+(new_grid_basey+3.5)

#書式変換
def transform(string, W):
    flat = string.replace("\n", "").split(" ")
    state = np.array([int(flat[j]) for j in range(64)]).reshape(8, 8)
    #全部白が勝ったことにする
    if(W == 1):
      state = (3-state) % 3
    action = (int(flat[65])-1)*8 + int(flat[64])-1
    return state, action

#特徴量:ひっくり返せない盤面
def corner_state(old_state):
    res = np.zeros([8, 8])
    if(old_state[0][0] == 1):
        nowx = 0
        nowy = 0
        while((old_state[nowx][0] == 1)):
            res[nowx][0] = 1
            nowx += 1
            if(nowx == 8):
                break
        while((old_state[0][nowy] == 1)):
            res[0][nowy] = 1
            nowy += 1
            if(nowy == 8):
                break
        nowx = 0
        nowy = 0
        while((old_state[nowx][nowy] == 1)):
            res[nowx][nowy] = 1
            nowx += 1
            nowy += 1
            if(nowy == 8):
                break
    if(old_state[7][0] == 1):
        nowx = 7
        nowy = 0
        while((old_state[nowx][0] == 1)):
            res[nowx][0] = 1
            nowx -= 1
            if(nowx == -1):
                break
        while((old_state[7][nowy] == 1)):
            res[7][nowy] = 1
            nowy += 1
            if(nowy == 8):
                break
        nowx = 7
        nowy = 0
        while((nowy < 8) & (old_state[nowx][nowy] == 1)):
            res[nowx][nowy] = 1
            nowx -= 1
            nowy += 1
            if(nowy == 8):
                break
    if(old_state[0][7] == 1):
        nowx = 0
        nowy = 7
        while((old_state[nowx][7] == 1)):
            res[nowx][7] = 1
            nowx += 1
            if(nowx == 8):
                break
        while((old_state[0][nowy] == 1)):
            res[0][nowy] = 1
            nowy -= 1
            if(nowy == -1):
                break
        nowx = 0
        nowy = 7
        while((nowx < 8) & (old_state[nowx][nowy] == 1)):
            res[nowx][nowy] = 1
            nowx += 1
            nowy -= 1
            if(nowx == 8):
                break
    if(old_state[7][7] == 1):
        nowx = 7
        nowy = 7
        while((old_state[nowx][7] == 1)):
            res[nowx][7] = 1
            nowx -= 1
            if(nowx == -1):
                break
        while((old_state[7][nowy] == 1)):
            res[7][nowy] = 1
            nowy -= 1
            if(nowy == -1):
                break
        nowx = 7
        nowy = 7
        while((nowx >= 0) & (old_state[nowx][nowy] == 1)):
            res[nowx][nowy] = 1
            nowx -= 1
            nowy -= 1
            if(nowx == -1):
                break
    return res


def shuffle_dataset(X, y):
    zipped = list(zip(X, y))
    np.random.shuffle(zipped)
    X_result, y_result = zip(*zipped)
    return np.asarray(X_result), np.asarray(y_result)
#データ読み込み
with open("data\OthelloTeacher.txt") as f:
    data=f.readlines()
print("data loaded")
B_list=[];
W_list=[];
print(len(data))

#データ加工
for line in data:
    if "B" in line:
        B_list.append(line)
    else:
        W_list.append(line)
print(len(B_list),len(W_list))


state_list = np.zeros([len(data), 8, 8])
action_list = np.zeros([len(data)])
for index, line in enumerate(data):
    if "W" in line:
        state, action = transform(line, 0)
    else:
        state, action = transform(line, 1)
    #この状態から白が指す
    #なおかつ白が勝った
    state_list[index] = state
    action_list[index] = action

#メモリ確保
state_list = np.resize(state_list, (len(state_list)*4, 8, 8))
action_list = np.resize(action_list, len(action_list)*4)
print(state_list.shape, action_list.shape)

#回転して新しい状態を作る
original_len=148718
for index in range(original_len):
    now_state=state_list[index]
    now_action=action_list[index]
    for k in range(3):
        now_state=np.rot90(now_state).copy()
        now_action=new_action(now_action)
        state_list[index+original_len*(k+1)]=now_state
        action_list[index+original_len*(k+1)]=now_action
print(action_list.shape,state_list.shape)

print("zeke")

#学習のためにシャッフルしておく
print(type(state_list))
print(state_list[0])
print(state_list.shape)   
#白盤面と黒盤面に分ける
state_list_1 = np.where(state_list == 1, 1, 0)
state_list_2 = np.where(state_list == 2, 1, 0)

train = np.array([state_list_1, state_list_2])

print(train.shape)

#policyネットワークモデルを取得後学習
model1 = load_model("./model/policy_model.h5")
action_list=to_categorical(action_list)
train = train.transpose(1, 2, 3,0 )
print(train.shape)
print(action_list.shape)
model1.compile(loss=['categorical_crossentropy'], optimizer='adam')
model1.fit(train,action_list,epochs=100)

model1.save("./model/policy_model.h5")

# %%



model2 = load_model("./model/policy_model.h5")
for index in range(10):
    tempstate1=Othello_SL.selfplay(play_num=20)
    tempstate=tempstate1.state
    state_list_1 = np.where(tempstate== 1, 1, 0)
    state_list_2 = np.where(tempstate == 2, 1, 0)

    test = np.array([state_list_1, state_list_2])
    test = test.transpose(1,2,0)

    test = test[np.newaxis,:,:,:]
    ans=model2.predict(test)
    ans2=np.argsort(-ans)
    print(ans)
    print(ans2)
    prediction_data = np.array([ans[0][j] for j in range(64)]).reshape(8, 8)
    plt.imshow(np.log(prediction_data), origin='lower', vmax=np.log(prediction_data).max(), vmin=np.log(prediction_data).min(), cmap="cool")
    plt.colorbar(cmap="cool")
    for j in range(8): 
        for k in range(8):
            if(test[0][k][j][0] == 1):
                plt.scatter(j, k, marker="o", c="black", s=50)
            if(test[0][k][j][1] == 1):
                plt.scatter(j, k, marker="o", c="white", s=50)
    _,p_hands=tempstate1.possible_state()
    res_action = 0
    #print(result)
    #合法手の中でSLポリシーの最も高い行動を選択していくわよ
    for i in p_hands:
        plt.scatter(i % 8, i//8, marker="x", c="green", s=50)
    for i in ans2[0]:
        if i in p_hands:
            res_action = i
    res_action = 0
    #print(result)
    #合法手の中でSLポリシーの最も高い行動を選択していくわよ
    for i in ans2[0]:
        if i in p_hands:
            plt.scatter(i % 8, i//8, c="yellow", s=400)
            break
    '''for i in range(5):
        s="$"+str(i+1)+"$"
        plt.scatter(ans2[0][i] % 8, ans2[0][i]//8,
                    marker=s, c="yellow", s=400)
    '''
    plt.show()
# %%
