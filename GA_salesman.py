import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import random



def random_state(num):
    return np.random.randint(0,100000,(num,2))

def evaluate(Gene,state):
    res=0.00
    for i in range(len(Gene)-1):
        #print(res)
        u=state[Gene[i+1]]-state[Gene[i]]
        res+=np.linalg.norm(u)
    #u=state[Gene[0]]-state[Gene[len(Gene)-1]]
    res+=np.linalg.norm(u)
    return res
def random_Population(p_num,n_num):
    #print(random.sample([i for i in range(n_num)],n_num))
    res=[random.sample([i for i in range(n_num)],n_num) for j in range(p_num)]
    return res
def TwiceChoice(num,p_list):
    #print(p_list)
    return np.random.choice(num,2,replace=False,p=p_list)

def children(p1,p2):
    n=len(p1)
    templist1=[0]*(n+1)
    templist2=[0]*(n+1)
    chi1=[-1]*len(p1)
    chi2=[-1]*len(p1)
    #print(p1,p2)
    for index,j in enumerate(p1):
        templist1[j]=index
    for index,j in enumerate(p2):
        templist2[j]=index

    ##p1を先にする循環交叉
    flaglist=[0]*(n+1)
    
    now=0
    while(flaglist[now]==0):
        flaglist[now]=1
        chi1[now]=p1[now]
        now=templist1[p2[now]]
    for i in range(len(p1)):
        if(chi1[i]==-1):
            chi1[i]=p2[i]
    ##p1を先にする循環交叉 
    flaglist=[0]*(n+1)
    now=0
    while(flaglist[now]==0):
        flaglist[now]=1
        chi2[now]=p2[now]
        now=templist2[p1[now]]
    for i in range(len(p2)):
        if(chi2[i]==-1):
            chi2[i]=p1[i]
    return chi1,chi2



num=50
p_num=200
m_num=250
g_num=1000
elete=20
state=random_state(num)
print(evaluate(range(num),state))
fig=plt.figure()
ims = []
Population=random_Population(p_num,num)
for index in range(g_num):
    newstate=[[0]*num for i in range(p_num)]
    p_list=np.zeros([p_num])
    for j in range(p_num):
        p_list[j]=1.00/evaluate(Population[j],state)
    #print(p_list)
    p_list/=np.sum(p_list)
    sort_list=[]
    p_list2=[]
    p_sum=0
    for j in range(m_num):
        a,b=TwiceChoice(p_num,p_list)
        c1,c2=children(Population[a],Population[b])
        v1=evaluate(c1,state)
        v2=evaluate(c2,state)
        sort_list.append((v1,c1))
        sort_list.append((v2,c2))
        p_list2.append(v1)
        p_list2.append(v2)
        p_sum+=v1
        p_sum+=v2
    p_list2/=p_sum
    sort_list2=sorted(sort_list,key=lambda x: x[0])
    for i in range(p_num):
        if(i<elete):
            Population[i]=sort_list2[i][1]
        else:
            #print(len(sort_list[:][0]))
            #print(len(p_list2))
            sort_index=np.random.choice(range(len(p_list2)),p=p_list2)
            #print(sort_index)
            Population[i]=sort_list2[sort_index][1]
        if(random.randint(1,10)<=1&i!=0&i!=p_num-1):
            a=random.randint(0,num-1)
            b=random.randint(0,num-1)
            Population[i][a],Population[i][b]= Population[i][b],Population[i][a]
            
    print(index,evaluate(Population[0],state),evaluate(Population[p_num-1],state))
    #print(Population[0])
    connection_x=[]
    connection_y=[]
    for i in range(num):
        connection_x.append(state[Population[0][i]][0])
        connection_y.append(state[Population[0][i]][1])
    #for i in range(num):
    #connection_x.append(state[Population[0][0]][0])
    #connection_y.append(state[Population[0][0]][1])
    s=str(index)+" "+str(evaluate(Population[0],state))
    im=plt.plot(connection_x,connection_y,color="k")
    ims.append(im)
   # plt.show()
ani = animation.ArtistAnimation(fig, ims, interval=100)
ani.save("output.gif", writer="imagemagick")
plt.show()

#print(TwiceChoice(4,[0.1,0.2,0.3,0.4]))
#print(children([1,2,3,4,5,6,7,8,9],[4,1,2,8,7,6,9,3,5]))

# プロット領域(Figure, Axes)の初期化
'''
fig = plt.figure()
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223)
ax4 = fig.add_subplot(224)
ax1.axis([-1.2, 1.2, -1.2, 1.2])
ax2.axis([0, 100, -2, 2]) 

# 棒グラフの作成
s = 1
ims = []

for i in range(10):
        rand = np.random.randn(100)     # 100個の乱数を生成
        im = ax1.plot(rand)             # 乱数をグラフにする
        ims.append(im)                  # グラフを配列 ims に追加
        im = ax2.plot(rand)             # 乱数をグラフにする
        ims.append(im)
        im = ax3.plot(rand)             # 乱数をグラフにする
        ims.append(im)
        im = ax4.plot(rand)             # 乱数をグラフにする
        ims.append(im)

ani = animation.ArtistAnimation(fig, ims, interval=100)
ani.save('anim.gif', writer="imagemagick")
#ani.save('anim.mp4', writer="ffmpeg")
plt.show()
'''