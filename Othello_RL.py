# ヘルパーライブラリのインポート
import numpy as np
import matplotlib.pyplot as plt
import random
from tensorflow.keras.models import Model, load_model
#Othelloライブラリ
import Othello_SL as sl
import Othello_common as cm
import Othello_dualnetwork as dn
EPOCHS=10


def main():
    for epoch in range(EPOCHS):
        print("EPOCH:",epoch)
        value_list=[]
        policy_list=[]
        state_list=[]
        model1 = load_model("./model/best.h5")
        for game in range(500):
            if game%50==0:
                print(game/5,' percent completed')
            hand_num=random.randint(2,13)
            temp_state=sl.selfplay(nowstate=None,play_num=hand_num)
            #print(temp_state.str_show())
            if temp_state is None:
                print("invalid game",epoch,game)
                continue
            _,leagal=temp_state.possible_state()
            if len(leagal)==0:
                print("No valid game")
                continue
            random_action=temp_state.random_action()
            policy_list.append(random_action)
            final_state=sl.SLpolicy_selfplay(temp_state,model1)
            if(final_state is None):
                print("No valid final game")
                continue
            value_list.append(final_state.is_win())
        state_list=np.array(state_list)
        value_list=np.array(value_list)
        policy_list = np.array(policy_list)
        print(state_list.shape,value_list.shape,policy_list.shape)
        print(value_list)
        dn.train_network(state_list,value_list,policy_list)
        
if __name__=='__main__':
    main()



