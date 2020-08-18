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
#include <cstdlib>
#include <fstream>
#include <iostream>
using namespace std;
int main() {
    std::ifstream ifs("./data/OthelloTeacher.txt", ios::in);
    if (!ifs) {
        cerr << "RunTimeError:file deploy" << std::endl;
        exit(1);
        return 0;
    }
    cerr<<"file deploy completed"<<endl;
    vector<vector<vector<int>>> B_data;
    vector<vector<vector<int>>> W_data;
    do{
        vector<vector<int>> field(8,vector<int>(8));
        for(int h=0;h<8;h++){
            for(int w=0;w<8;w++){
                ifs>>field[h][w];
            }
        }
        int handy,handx,remain;
        char turn;
        ifs>>handy>>handx>>turn>>remain;
        if(turn=='B'){
            B_data.push_back(field);
        }else{
            W_data.push_back(field);
        }
    }while(!ifs.eof());
    cerr<<"B_data_size "<<B_data.size()<<endl;
    cerr<<"W_data_size "<<W_data.size()<<endl;
}
