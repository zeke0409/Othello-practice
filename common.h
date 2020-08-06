#define EIGEN_NO_DEBUG          // コード内のassertを無効化．
#define EIGEN_DONT_VECTORIZE    // SIMDを無効化．
#define EIGEN_DONT_PARALLELIZE  // 並列を無効化．
#define EIGEN_MPL2_ONLY  // LGPLライセンスのコードを使わない．
#include <Eigen/Dense>
#include <random>
#include <map>
#include <iostream>
using namespace Eigen;
using namespace std;
class MulLayer {
   private:
    double self_x = 0;
    double self_y = 0;

   public:
    double forward(double x, double y);
    pair<double, double> backward(double out);
};
class AddLayer {
   private:
    double self_x = 0;
    double self_y = 0;

   public:
    double forward(double x, double y);
    pair<double, double> backward(double out);
};
class Relu {
   private:
    bool mask = 0;

   public:
    double forward(double x);
    double backward(double out);
};
class TwoLayerNet {
    private:
     map<string,Vector2d> params;
    public:
     TwoLayerNet(int input_size, int hidden_size, int out_putsize,
                 int weight_init_std = 0.01);
     Vector2d predict(Vector2d x);
     double loss(Vector2d x, Vector2d t);
     double accuracy(Vector2d x, Vector2d t);
     Vector2d numerical_gradient(Vector2d x, Vector2d t);
};