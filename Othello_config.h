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
class Othello_config {
   private:
    int H;
    int W;
    int turn = 0;
    int mynum;
    vector<vector<int>> field;
    vector<int> candidate;
    int dx4[4] = {-1, 0, 1, 0};
    int dy4[4] = {0, -1, 0, 1};
    int dx8[8] = {-1, -1, -1, 0, 1, 1, 1, 0};
    int dy8[8] = {-1, 0, 1, 1, 1, 0, -1, -1};
    bool can_process(int y, int x);  //そのマスが8*8内か？
    vector<vector<int>> temp_res(int y,int x);
   public:
    Othello_config(int my_turn);
    vector<int> Othello_candidate();  //次打てるマスを返す
    void show();                      //今の盤面を見せる
    int predict();
    int evaluate(vector<vector<int>> &nowfield);
};