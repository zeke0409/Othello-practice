# %%
import matplotlib.pyplot as plt
import Othello_common
from tensorflow.keras.models import Model, load_model
import math
#from graphviz import Digraph
import copy
import Othello_SL as sl
'''
モンテカルロ木探索部、MCTSの中でNodeクラスを生成
'''
# %%
def UCB(w,n,t):#UCB1アルゴリズム
    return w/n+math.sqrt(2*math.log(t)/n)
MOD=1e5+7
model1 = load_model("./model/latest2.h5")
def MCTS(state,play_num,update_num):
    #G = Digraph(format='png')
    #G.attr('node', shape='circle')
    class Node:
        def __init__(self,state):
            self.n=0
            self.w=0
            self.state=copy.copy(state)
            self.child_list=[]
        def unique_num(self):#Node毎にユニークな値を返す.デバッグ用
            res=0
            for i in range(8):
                for j in range(8):
                    res+=self.state.state[i][j]*pow(2,int(i*8+j),int(MOD))
            return res
        def expand(self):
            _,possibles=self.state.possible_state()
            #手がないときは拡張しない
            if len(possibles)==0:
                return
            for hand in possibles:
                new_state=self.state.next_state(hand)
                new_state=Othello_common.State(3-self.state.turn,new_state)
                NewNode=Node(new_state)
                #G.edge(str(self.unique_num()), str(NewNode.unique_num()))
                self.child_list.append((hand,NewNode))
        # ->int(evaluate value)
        def evaluate(self):
            #葉の時
            if len(self.child_list)==0:
                #規定値より大きいければ拡張
                if self.n>=update_num:
                    self.expand()
                #現在の状態を取得
                result=self.state.playout_policy(model1)
                result=(result-1)*3
                #自分の番=敵が選ぶ->正負逆転
                if(self.state.turn==1):
                    result*=-1
                self.w+=result
                self.n+=1
                #正負逆転した状態を渡す
                return -result
            else:
                result=self.UCBmaxNode().evaluate()
                self.w+=result
                self.n+=1
                return -result
        #->Node
        def UCBmaxNode(self):
            for _,child_node in self.child_list:
                #一回も探索していない子は最優先で探索
                if child_node.n==0:
                    return child_node
            
            score_list=[]
            for _,child_node in self.child_list:
                score_list.append(UCB(child_node.w,child_node.n,self.n))
            return self.child_list[score_list.index(max(score_list))][1]
    root_Node=Node(state)
    #rootノードは無条件に拡張
    root_Node.expand()
    
    root_Node.n+=1
    playindex=1
    for index in range(play_num):
        if(index>(play_num//20)*playindex):
            print('processing... : {:.0%}'.format(playindex*5/100))
            playindex += 1
        root_Node.evaluate()
    finalscore_list=[]
    for _,childNode in root_Node.child_list:
        childNode.state.str_show()
        print(childNode.n)
        print(childNode.w/childNode.n)
        print(root_Node.n)
        print(childNode.state.playout_policy(model1))
        print(UCB(childNode.w, childNode.n, root_Node.n))
        finalscore_list.append(childNode.n)
    #G.render("graphs")
    
    #print(node_num)
    return root_Node.child_list[finalscore_list.index(max(finalscore_list))][0]

# %%
import numpy as np
if __name__=='__main__':
    #nowstate=sl.selfplay(play_num=20)
    hand_made = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 2, 0, 0, 0, 0],
                          [0, 0, 0, 1, 2, 1, 1, 1],
                          [0, 0, 0, 1, 2, 2, 2, 2],
                          [0, 0, 0, 1, 2, 2, 2, 0],
                          [0, 0, 0, 1, 2, 2, 0, 0]])
    nowstate=Othello_common.State(1,hand_made)
    res=MCTS(nowstate,300,10)
    '''
    #print(res)
    plt.rcParams['axes.facecolor'] = 'g'
    plt.rcParams['text.color'] = 'w'
    plt.rcParams['xtick.color'] = 'w'
    plt.rcParams['ytick.color'] = 'w'
    SIZE=8
    line_width = 2
    plt.figure(figsize=(6, 6), facecolor='k')
    for y_pos in range(SIZE):
        plt.axhline(y_pos-.5, color='k', lw=line_width)
        for x_pos in range(SIZE):
            if nowstate.state[y_pos][x_pos]==1:
                plt.plot(color='w',marker='o')
            plt.axvline(x_pos-.5, color='k', lw=line_width)
    
    plt.xlim([-.5, 8-.5])
    plt.ylim([-.5, 8-.5])
    for y_pos in range(SIZE):
        for x_pos in range(SIZE):
            if nowstate.state[y_pos][x_pos] == 1:
                plt.scatter(y_pos,x_pos,color='white', marker='o', zorder=2,s=200)
            if nowstate.state[y_pos][x_pos] == 2:
                plt.scatter(y_pos, x_pos, color='black',
                            marker='o', zorder=2, s=200)
    print(res)
    plt.scatter(res//8, res%8, color= 'yellow',marker='x', zorder=2, s=200)
    plt.show()
    '''
