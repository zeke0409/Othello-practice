import Othello_MCTS as mcts
import Othello_common as cm

import matplotlib.pyplot as plt
def show(nowstate):
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
            if nowstate.state[y_pos][x_pos] == 1:
                plt.plot(color='w', marker='o')
            plt.axvline(x_pos-.5, color='k', lw=line_width)

    plt.xlim([-.5, 8-.5])
    plt.ylim([-.5, 8-.5])
    for y_pos in range(SIZE):
        for x_pos in range(SIZE):
            if nowstate.state[y_pos][x_pos] == 1:
                plt.scatter(y_pos, x_pos, color='white',
                            marker='o', zorder=2, s=200)
            if nowstate.state[y_pos][x_pos] == 2:
                plt.scatter(y_pos, x_pos, color='black',
                            marker='o', zorder=2, s=200)
    plt.show()


if __name__=='__main__':
    nowstate=cm.State(1)
    p_flag=False
    while(1):
        show(nowstate)
        print("My turn..")
        if nowstate.is_possible_hand():
            if p_flag:
                break
            p_flag=True
            print("PASS!!")
        else:
            p_flag=False
            res=mcts.MCTS(nowstate,1000,10)
            nowstate=nowstate.next_state(res)
            nowstate=cm.State(2,nowstate)
        show(nowstate)
        print("yout turn..")
        _,possible_hand=nowstate.possible_state()
        if nowstate.is_possible_hand():
            if p_flag:
                break
            p_flag = True
            print("YOU PASS!!")
        else:
            p_flag = False
            hand=0
            while True:
                print("Y X")
                a = list(map(int, input().split()))
                your_y = a[0]
                your_x = a[1]
                hand=your_y*8+your_x
                if hand in possible_hand:
                    break
            nowstate = nowstate.next_state(hand)
            nowstate = cm.State(1, nowstate)
    print("FINISHed")
    if nowstate.is_win()==1:
        print("hahaha")
    elif nowstate.is_win()==0:
        print("you win")
    else:
        print("draw")
