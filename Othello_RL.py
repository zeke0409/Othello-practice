# ヘルパーライブラリのインポート
import numpy as np
import matplotlib.pyplot as plt
import random

#Othelloライブラリ
import Othello_SL as sl
import Othello_common as cm
import Othello_dualnetwork as dn
EPOCHS=100


def main():
    for epoch in range(EPOCHS):
        print("EPOCH:",epoch)
        value_list=[]
        policy_list=[]
        state_list=[]
        for game in range(10):
            if game%30==0:
                print('*',end='')
            hand_num=random.randint(1,15)
            temp_state=sl.selfplay(play_num=hand_num)
            if temp_state is None:
                print("invalid game",epoch,game)
                continue
            _,leagal=temp_state.possible_state()
            if len(leagal):
                print("No valid game")
                continue
            state_list.append(temp_state.state)
            random_action=temp_state.random_action
            policy_list.append(random_action)
            final_state=sl.selfplay()
            value_list.append(final_state.is_win())
        





