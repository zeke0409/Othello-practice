//遺伝的アルゴリズムの練習としてナップサック問題を解きます
#include <algorithm>
#include <bitset>
#include <cassert>
#include <cmath>
#include <deque>
#include <functional>
#include <iomanip>
#include <iostream>
#include <map>
#include <queue>
#include <set>
#include <stack>
#include <string>
#include <utility>
#include <random>
#include <vector>
using namespace std;
//#define int long long
template <class T>
bool chmax(T& a, const T& b) {
    if (a < b) {
        a = b;
        return 1;
    }
    return 0;
}
template <class T>
bool chmin(T& a, const T& b) {
    if (b < a) {
        a = b;
        return 1;
    }
    return 0;
}
vector<int> weight;
vector<int> value;
int N,M,Wlimit,population_size;
tuple<vector<int>,vector<int>> generate_random(int n,int min=0,int max=100){
    vector<int> random_weight(n);
    vector<int> random_value(n);
    random_device seed_gen;
    mt19937 engine((int)time(0));
    uniform_int_distribution<> rand(min, max);
    for(int i=0;i<n;i++){
        random_weight[i] = rand(engine);
    }
    for (int i = 0; i < n; i++) {
        random_value[i] = rand(engine);
    }
    return make_tuple(random_weight,random_value);
}
int evaluate(vector<bool>& gene){
    int resvalue=0;
    int resweight=0;
    for(int i=0;i<gene.size();i++){
        if(gene[i]){
            resvalue+=value[i];
            resweight+=value[i];
        }
    }
    if(resweight>Wlimit){
        return 0;
    }
    return resvalue;
}
inline void InitRand() { srand((unsigned int)time(NULL)); }
vector<vector<bool>> ChoiceRoulette(vector<vector<bool>> &Chromo){
    vector<vector<bool>> res(population_size);
    vector<int> accumulate_value(population_size+1);
    for(int i=0;i<population_size;i++){
        int value=evaluate(Chromo[i]);
        accumulate_value[i+1]=accumulate_value[i]+value;
    }
    srand((int)time(NULL));
    vector<pair<int, vector<bool>>> children;
    for(int i=0;i<M;i++){
        vector<bool> newGene1(N);
        vector<bool> newGene2(N);
        int k1=rand()%accumulate_value[population_size];
        int k2 = rand() % accumulate_value[population_size];
        //int state1=lower_bound(accumulate_value.begin(),accumulate_value.end(),k1)-accumulate_value.begin();
        //int state2=lower_bound(accumulate_value.begin(),accumulate_value.end(),k2)-accumulate_value.begin();
        int breaker_point=rand()%N;
        int state1=rand();
        int state2=rand();
        state1%=population_size;
        state2%=population_size;
       // cout<<"choice"<<state1<<" "<<state2<<" "<<breaker_point<<endl;
        for(int j=0;j<N;j++){
            if(j<breaker_point){
                newGene1[j]=Chromo[state1][j];
                newGene2[j]=Chromo[state2][j];
            }else{
                newGene1[j] = Chromo[state2][j];
                newGene2[j] = Chromo[state1][j];
            }
        }
       // cout<<"middle"<<endl;
        children.push_back({evaluate(newGene1),newGene1});
        children.push_back({evaluate(newGene2), newGene2});
       // cout << evaluate(newGene1) << " " << evaluate(newGene2)<<endl;
    }
   // cout<<"finished"<<endl;
    sort(children.begin(),children.end());
    reverse(children.begin(),children.end());
    //cout<<"finished2"<<children.size()<<" "<<population_size<<" "<<res.size()<< endl;
    for(int i=0;i<population_size;i++){
       // cout<<"fini"<<i<<endl;
       if(i<0.5*population_size){
           res[i] = children[i].second;
       }else{
           res[i]=children[rand()%population_size].second;
       }
    }
    cout << children[0].first << " " << children.back().first << endl;
    //cout<<"return!"<<endl;
    return res;
}
int DynamicPlanning(){
    vector<int> dp(Wlimit+1);
    for(int i=0;i<N;i++){
        for(int j=Wlimit;j>=0;j--){
            if(j+weight[i]>Wlimit){
                continue;
            }
            chmax(dp[j+weight[i]],dp[j]+value[i]);
        }
    }
    int res=0;
    for(int i=0;i<=Wlimit;i++){
        chmax(res,dp[i]);
    }
    return res;
}
signed main(){
    cin>>N>>population_size>>M;
    Wlimit=1e6;
    tuple<vector<int>,vector<int>> rando=generate_random(N);
    srand((int)time(NULL));
    weight=get<0>(rando);
    value = get<1>(rando);
    vector<vector<bool>> Chromo(population_size, vector<bool>(N));
    for (int i = 0; i < population_size; i++) {
        for (int j = 0; j < N; j++) {
            Chromo[i][j] = (rand() % 2 == 0);
        }
    }
    /*for(int i=0;i<population_size;i++){
        for(int j=0;j<N;j++){
            cout<<Chromo[i][j]<<" ";
        }
        cout<<endl;
    }*/
    for(int i=0;i<100;i++){
        cout<<"evaluate: "<<i<<" "<<evaluate(Chromo[1])<<endl;
        Chromo=ChoiceRoulette(Chromo);
    }
    cout<<"answer:"<<DynamicPlanning()<<endl;
}