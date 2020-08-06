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
class Otello_config{
    private:
    int H;
    int W;
    int turn=0;
    int mynum;
    vector<vector<int>> field;
    public:
    vector<int> Othello_candidate();
};