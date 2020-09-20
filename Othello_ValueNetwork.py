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
'''SLpolicyNetwork通り指すことで盤面のvalueを求めていきたい'''
'''教師データを生成'''
EPOCHS = 1
x=[]
y=[]
def main():
    for epoch in range(EPOCHS):
        print("EPOCH:",epoch)
        value_list=[]
        state_list=[]
        print("start")
        #500000ゲームする
        for game in range(500000):
            if game%50==0:
                print("game",game)
            #何手目まで適当に進めるか選ぶ
            hand_num=random.randint(20,31)
            temp_state=sl.selfplay(nowstate=None,play_num=hand_num)
            #有効な盤面でなければ飛ばす
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
            #SLpolicyネットワークを利用して終局まで指す
            final_state=sl.selfplay_vsSLpolicy(temp_state)
            #有効な盤面でなければ飛ばす
            if(final_state is None):
                print("No valid final game")
                continue
            value_list.append(final_state.is_win())
            print(value_list)
        #保存するために平滑化
        state_list= np.ravel(state_list)
        value_list= np.ravel(value_list)
        state_list=np.array(state_list)
        value_list=np.array(value_list)
        np.savetxt("./data/state.txt",state_list)
        np.savetxt("./data/value.txt",value_list)
        print(state_list.shape,value_list.shape)
        print(value_list)

if __name__=='__main__':
    main()


# %%
'''準備した生データを加工'''
import numpy as np
k = np.loadtxt('./data/state.txt')
g = np.loadtxt('./data/value.txt')
k = k.reshape([-1, 2, 8, 8])
res=[]
print(k.shape)
print(g.shape)

'''絶対にひっくりかえせない盤面'''
for index in range(len(k)):
    res1 = np.zeros([8, 8])
    res2 = np.zeros([8, 8])
    state=k[index][0]
    for rotate_num in range(4):
        for h in range(8):
            if state[h][0] != 1:
                break
            for w in range(8):
                if (h != 0) and (res1[h-1][w] != 1):
                    break
                if state[h][w] != 1:
                    break
                res1[h][w] = 1
        res1 = np.rot90(res1)
        state = np.rot90(state)
    state = k[index][1]
    for rotate_num in range(4):
        for h in range(8):
            if state[h][0] != 1:
                break
            for w in range(8):
                if (h != 0) and (res2[h-1][w] != 1):
                    break
                if state[h][w] != 1:
                    break
                res2[h][w] = 1
        res2 = np.rot90(res2)
        state = np.rot90(state)
    res.append([res1,res2])
res=np.array(res)

print(res[11][0])
print(res[11][1])
print(k[11])
print(g)

'''置くことのできる盤面'''
def possible_state(state_1, state_2):
    dx = [1, 1, 1, 0, -1, -1, -1, 0]
    dy = [-1, 0, 1, 1, 1, 0, -1, -1]
    possible_1 = np.zeros([8, 8])
    possible_2 = np.zeros([8, 8])
    state = np.zeros([8, 8])
    for i in range(8):
        for j in range(8):
            if state_1[i][j] == 1:
                state[i][j] = 1
            elif state_2[i][j] == 1:
                state[i][j] = 2
    num = 1
    for h in range(8):
        for w in range(8):
            if(state[h][w] != 0):
                continue
            for lx, ly in zip(dx, dy):
                nowh = h+lx
                noww = w+ly
                flag = False
                possible_lists = []
                while(True):
                    if((nowh < 0) | (nowh >= 8) | (noww < 0) | (noww >= 8)):
                        break
                    if(state[nowh][noww] == num):
                        if(len(possible_lists) >= 1):
                            flag = True
                        break
                    elif(state[nowh][noww] == 3-num):
                        possible_lists.append(nowh*8+noww)
                    else:
                        break
                    nowh += lx
                    noww += ly
                if(flag):
                    break
            if(flag):
                possible_1[h][w] = 1
    num = 2
    for h in range(8):
        for w in range(8):
            if(state[h][w] != 0):
                continue
            for lx, ly in zip(dx, dy):
                nowh = h+lx
                noww = w+ly
                flag = False
                possible_lists = []
                while(True):
                    if((nowh < 0) | (nowh >= 8) | (noww < 0) | (noww >= 8)):
                        break
                    if(state[nowh][noww] == num):
                        if(len(possible_lists) >= 1):
                            flag = True
                        break
                    elif(state[nowh][noww] == 3-num):
                        possible_lists.append(nowh*8+noww)
                    else:
                        break
                    nowh += lx
                    noww += ly
                if(flag):
                    break
            if(flag):
                possible_2[h][w] = 1
    return possible_1, possible_2
p1=[]
p2=[]
print(k.shape)
for i in range(len(k)):
    t1,t2=possible_state(k[i][0],k[i][1])
    p1.append(t1)
    p2.append(t2)
p1=np.array(p1)
p2=np.array(p2)
print(p1.shape)
print(p2.shape)
num=11
print("1")
print(res[num][0])
print("2")
print(res[num][1])
print(k[num])
final_res=[]
for i in range(len(k)):
    final_res.append([k[i][0],k[i][1],res[i][0],res[i][1],p1[i],p2[i]])
final_res=np.array(final_res)
print(final_res.shape)
original_len = len(final_res)
final_res = np.resize(final_res, (len(final_res)*8,6, 8, 8))
action_list = np.resize(g, len(g)*8)
print(final_res.shape, action_list.shape)

#回転して新しい状態を作る

for index in range(original_len):
    now_value = g[index]
    for k in range(8):
        action_list[index+original_len*k] = now_value
    for l in range(6):
        now_state = final_res[index][l].copy()
        for k in range(3):
            now_state = np.rot90(now_state).copy()
            final_res[index+original_len*(k+1)][l] = now_state
    for l in range(6):
        now_state = np.fliplr(final_res[index][l]).copy()
        final_res[index+original_len*4][l] = now_state
        for k in range(3):
            now_state = np.rot90(now_state).copy()
            final_res[index+original_len*(k+5)][l] = now_state
print(final_res.shape, action_list.shape)


# %%
num = 10007
print(final_res[num][0])
print(final_res[num][1])
print(final_res[num][2])
print(final_res[num][3])
print(final_res[num][4])
print(final_res[num][5])
print(action_list[num])
# %%

train = np.array(final_res)
value = np.array(action_list)
print(train.shape, value.shape)

dn.train_network(train, value)
# %%
'''実際にバリューネットワークを試してみる'''
model2 = load_model("./model/latest2.h5")
def inturnable(state):
    res1 = np.zeros([8, 8])
    res2 = np.zeros([8, 8])
    for rotate_num in range(4):
        for h in range(8):
            if state[h][0] != 1:
                break
            for w in range(8):
                if (h != 0) and (res1[h-1][w] != 1):
                    break
                if state[h][w] != 1:
                    break
                res1[h][w] = 1
        res1 = np.rot90(res1)
        state = np.rot90(state)
    for rotate_num in range(4):
        for h in range(8):
            if state[h][0] != 2:
                break
            for w in range(8):
                if (h != 0) and (res2[h-1][w] != 2):
                    break
                if state[h][w] != 2:
                    break
                res2[h][w] = 1
        res2 = np.rot90(res2)
        state = np.rot90(state)
    return res1,res2


#temp_state = sl.selfplay(play_num=30)
hand_made = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 2, 0],
                    [0, 0, 0, 0, 0, 0, 1, 0],
                    [0, 0, 0, 0, 2, 1, 0, 0],
                    [0, 0, 0, 0, 2, 2, 2, 2]])

#for hoge in range(1000):
    #if hoge%50==0:
        #print(hoge)
estimate=0
for i in range(8):
    temp_state = cm.State(1, hand_made)
    res1, res2 = inturnable(hand_made)
    p1, p2 = possible_state(np.where(temp_state.state == 1, 1, 0),
                            np.where(temp_state.state == 2, 1, 0))
    state = np.array([np.where(temp_state.state == 1, 1, 0), np.where(
        temp_state.state == 2, 1, 0), res1, res2, p1, p2])
    state = state[np.newaxis, :, :, :]
    state = state.transpose(0, 2, 3, 1)
    res=model2.predict(state)
    print(res)
    estimate+=res
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
            if hand_made[y_pos][x_pos] == 1:
                plt.scatter(y_pos, x_pos, color='white',
                            marker='o', zorder=2, s=200)
            if hand_made[y_pos][x_pos] == 2:
                plt.scatter(y_pos, x_pos, color='black',
                            marker='o', zorder=2, s=200)
            if p1[y_pos][x_pos]==1:
                plt.scatter(y_pos, x_pos, color='white',
                            marker='1', zorder=2, s=500)
            if p2[y_pos][x_pos] == 1:
                plt.scatter(y_pos, x_pos, color='black',
                            marker='2', zorder=2, s=500)
    print(temp_state.piece_num())
    #print(g[num])
    plt.show()
    hand_made=np.rot90(hand_made).copy()
    if i==3:
        hand_made = np.rot90(hand_made).copy()
        hand_made = np.fliplr(hand_made).copy()
print(estimate/8)

# %%

# %%


