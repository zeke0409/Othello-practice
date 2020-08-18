#define EIGEN_NO_DEBUG          // コード内のassertを無効化．
#define EIGEN_DONT_VECTORIZE    // SIMDを無効化．
#define EIGEN_DONT_PARALLELIZE  // 並列を無効化．
#define EIGEN_MPL2_ONLY  // LGPLライセンスのコードを使わない．
#include "common.h"
#include <random>
double MulLayer::forward(double x,double y){
    self_x=x;
    self_y=y;
    return x*y;
}
std::pair<double,double> MulLayer::backward(double out) {
    double dx=out*self_x;
    double dy=out*self_y;
    std::pair<double,double> res={dx,dy};
    return res;
}
double Relu::forward(double x){
    mask=(x<=0);
  //  double out=
};
TwoLayerNet::TwoLayerNet(int input_size, int hidden_size, int output_size,int weight_init_std = 0.01) {
    params["W1"]=Vector2d(input_size,hidden_size);
    params["B1"]=Vector2d(1,hidden_size);
    params["W2"]=Vector2d(hidden_size,output_size);
    params["B2"]=Vector2d(1,output_size);

}

Vector2d TwoLayerNet::predict(Vector2d x) {
    Vector2d a1=x*params["W1"]+params["B1"];

}
double TwoLayerNet::loss(Vector2d x, Vector2d t){
    Vector2d y=predict(x);
}
Vector2d TwoLayerNet::numerical_gradient(Vector2d x, Vector2d t){
    
}