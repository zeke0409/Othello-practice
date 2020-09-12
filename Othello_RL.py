# %%
# ヘルパーライブラリのインポート
import numpy as np
import matplotlib.pyplot as plt
import random

from tensorflow.keras.models import Model, load_model
#Othelloライブラリ
import Othello_SL as sl
import Othello_common as cm
import Othello_dualnetwork as dn
# %%
#SLpolicyの方策通りに指すことで盤面のvalueを求めていきたい
EPOCHS = 1
x=[]
y=[]
def main():
    for epoch in range(EPOCHS):
        print("EPOCH:",epoch)
        value_list=[]
        state_list=[]
        policy_model=load_model("./model/policy_model.h5")
        model1 = load_model("./model/best.h5")
        model2 = load_model("./model/latest.h5")
        print("start")
        #1エポックにつき100000ゲームする
        for game in range(5000):
            if game%50==0:
                print("game",game)

            #何手目まで適当に進めるか選ぶ
            hand_num=random.randint(2,30)
            #print(hand_num)
            temp_state=sl.selfplay(nowstate=None,play_num=hand_num)
            if temp_state is None:
                print("invalid game",epoch,game)
                continue
            _,leagal=temp_state.possible_state()
            '''if len(leagal)==0:
                print("No valid hand")
                continue
            '''
            state_list.append([np.where(temp_state.state == 1, 1, 0),
                              np.where(temp_state.state == 2, 1, 0)])
            #random_action=temp_state.random_action()
            #policy_list.append(random_action)
            final_state=sl.SLpolicy_selfplay(temp_state,policy_model)
            #print("win or lose",final_state.is_win())
            if(final_state is None):
                print("No valid final game")
                continue
            value_list.append(final_state.is_win())
        
        state_list= np.ravel(state_list)
        value_list= np.ravel(value_list)
        state_list=np.array(state_list)
        value_list=np.array(value_list)
        np.savetxt("./data/state.txt",state_list)
        np.savetxt("./data/value.txt",value_list)
        #policy_list = np.array(policy_list)
        print(state_list.shape,value_list.shape)
        print(value_list)
        x=state_list
        y=value_list
        #dn.train_network(state_list, value_list)
        #dn.train_network(state_list,value_list)
        #もし勝ち越したら今のモデルをベストモデルとして保存
        #if(sl.SLpolicy_compete_selfplay(model2,model1)):
            #print("勝ち越し")
        #model1.save("./model/best.h5")

if __name__=='__main__':
    main()


# %%
import numpy as np
k = np.loadtxt('./data/state.txt')
g = np.loadtxt('./data/value.txt')
k= k.reshape([5000,2,8,8])
print(k[0])
print(g)
# %%

#dn.train_network(x_1, y_1)
# %%
model_2=load_model("./model/latest.h5")
for index in range(1):
    temp_state=sl.selfplay(play_num=10)
    state = np.array([np.where(temp_state.state == 1, 1, 0),
               np.where(temp_state.state == 2, 1, 0)])
    state=state[np.newaxis,:,:,:]
    print(state)
    state=state.transpose(0,2,3,1)
    res=model_2.predict(state)
    temp_state.str_show()
    print(res)
# %%
model2 = load_model("./model/latest.h5")

temp_state = sl.selfplay(play_num=5)
'''
hand_made = np.array([[1, 1, 1, 1, 1, 1, 1, 0],
                      [1, 1, 1, 1, 1, 1, 1, 1],
                      [1, 1, 1, 1, 1, 1, 1, 1],
                      [1, 1, 1, 1, 2, 1, 1, 1],
                      [1, 1, 1, 1, 1, 1, 1, 1],
                      [1, 1, 1, 1, 1, 1, 1, 1],
                      [1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1, 1, 1, 1]])
'''
#temp_state=cm.State(1,hand_made)
state = np.array([np.where(temp_state.state == 1, 1, 0),
                    np.where(temp_state.state == 2, 1, 0)])
state=state[np.newaxis,:,:,:]
state=state.transpose(0,2,3,1)
res=model2.predict(state)
print(res)
plt.rcParams['axes.facecolor'] = 'g'
plt.rcParams['text.color'] = 'w'
plt.rcParams['xtick.color'] = 'w'
plt.rcParams['ytick.color'] = 'w'
SIZE = 8
line_width = 2
plt.figure(figsize=(6, 6), facecolor='k')
for y_pos in range(SIZE):
    plt.axhline(y_pos-.5, color='k', lw=line_width)
    for x_pos in range(SIZE):
        plt.axvline(x_pos-.5, color='k', lw=line_width)

plt.xlim([-.5, 8-.5])
plt.ylim([-.5, 8-.5])
for y_pos in range(SIZE):
    for x_pos in range(SIZE):
        if temp_state.state[y_pos][x_pos] == 1:
            plt.scatter(y_pos, x_pos, color='white',
                        marker='o', zorder=2, s=200)
        if temp_state.state[y_pos][x_pos] == 2:
            plt.scatter(y_pos, x_pos, color='black',
                        marker='o', zorder=2, s=200)
print(temp_state.piece_num())
#print(g[num])
plt.show()
# %%
train=np.array(k)
value=np.array(g)
print(train.shape,value.shape)
dn.train_network(train,value)
# %%

