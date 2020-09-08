import Othello_common
import math
def UCB(w,n,t):
    return w/n+math.sqrt(2*math.log(t)/n)
def MCTS(state,play_num,update_num):
    class Node:
        def __init__(self,state):
            self.n=0
            self.w=0
            self.state=state
            self.child_list=[]
        def expand(self):
            _,possibles=state.possible_state_list()
            for hand in possibles:
                new_state=state.next_state(Othello_common.State(3-self.state.turn),hand)
                NewNode=Node(new_state)
                self.child_list.append((hand,NewNode))
        def evaluate(self):
            if len(self.child_list)==0:
                if self.n>=update_num:
                    self.expand()
                result=state.playout_policy()
                self.w+=result
                self.n+=1
                return -result
            else:
                result=self.UCBmaxNode().evaluate()
                self.w+=result
                self.n+=1
                return -result
        def UCBmaxNode(self):
            for _,child_node in self.child_list:
                if child_node.n==0:
                    return child_node
            score_list=[]
            for child_node in self.child_list:
                score_list.append(UCB(self.w,child_node.n,self.n))
            return self.child_list[score_list.index(max(score_list))]
    root_Node=Node(state)
    #rootノードは無条件に拡張
    root_Node.expand()
    root_Node.n+=1
    playindex=1
    for index in range(play_num):
        if(index>(play_num//20)*playindex):
            playindex+=1
            print("#",end="")
        root_Node.evaluate()
    finalscore_list=[]
    for childNode in root_Node.child_list:
        finalscore_list.append(childNode.n)
    return root_Node.child_list[finalscore_list.index(max(finalscore_list))][0]