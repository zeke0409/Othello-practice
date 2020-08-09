#include "Othello_config.h"

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
#include <vector>
using namespace std;
Othello_config::Othello_config(int myturn) {
    field.resize(8, vector<int>(8, -1));
    //-1無し0先手1後手
    mynum=myturn;
}
bool Othello_config::can_process(int y, int x) {
    if (y < 8 && x < 8 && y >= 0 && x >= 0) {
        return true;
    }
    return false;
}

vector<int> Othello_config::Othello_candidate() {
    //自分0
    vector<int> res;
    for (int h = 0; h < 8; h++) {
        for (int w = 0; w < 8; w++) {
            for (int way = 0; way < 8; way++) {
                int nowh = h + dy8[way];
                int noww = w + dx8[way];
                if (!can_process(nowh, noww) || field[nowh][noww] != 1) {
                    continue;
                }
                while (can_process(nowh, noww)) {
                    if(field[nowh][noww]==0){
                        res.push_back(h*8+w);
                        break;
                    }
                    if (field[nowh][noww] == -1) {
                        break;
                    }
                    nowh+=dy8[way];
                    noww+=dx8[way];
                }
            }
        }
    }
    sort(res.begin(),res.end());
    candidate=res;
    return res;
}
vector<vector<int>> Othello_config::temp_res(int y,int x){
    int zip=y*H+x;
    if(binary_search(candidate.begin(),candidate.end(),zip)){
        cout<<"実行時エラー　temp_res内"<<endl;
        return field;
    }
    for(int way=0;way<8;way++){
        bool reverse=false;
        vector<int> temp_reverse;
        int nowh=y+dy8[way];
        int noww=x+dx8[way];
        if (!can_process(nowh, noww) || field[nowh][noww] != 1) {
            continue;
        }
        while (can_process(nowh, noww)) {
            if (field[nowh][noww] == 0) {
                reverse=true;
                break;
            }
            if (field[nowh][noww] == -1) {
                break;
            }
            nowh += dy8[way];
            noww += dx8[way];
        }
        if(reverse){

        }
    }
}
void Othello_config::show() {
    for (auto i : field) {
        for (auto j : i) {
            if (j == 0) {
                cout << "0 ";
            } else {
                cout << "1 ";
            }
        }
        cout << endl;
    }
}