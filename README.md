#  Othello by zeke

夏休みを利用してオセロAIを制作したよ、是非中身を見ていってね！！

# DEMO

 ![title](/Image/Title.PNG "title")
 ![game](/Image/play.gif "game")

簡単なUIでオセロを遊ぶことができます

# 特徴
AlphaGoをベースとしたオセロAIを書きました

初学者なので、内容に不備があるかもしれません

詳しい説明は[こちら](https://transnt-my.sharepoint.com/:p:/g/personal/zeke_transnt_onmicrosoft_com/EQg5zblqTj1DphUZWgqpmA8BYOimb98m0xl9yG0zlvbIcw?rtime=8znC9JBd2Eg)をご覧ください

# 動作環境

* Windows10 64bit 
* Python 3.6.6
    * tensorflow 2.1.0
    * pygame 1.9.6

で動作確認済み

Python3.8.xだとうまく動かなかったので注意

# 使い方
1.Python3.6.xを入れてください

2.このレポジトリをクローンしてください

3.必要なパッケージを入れてください

4.シェル上で Othello_play.pyを実行してください

# コードの説明

* Othello_common.py:主に雑用を担当
* Othello_dualnetwork.py:モデルの構築など
* Othello_SLpolicy.py:自己対戦など
* Othello_SL.py:方策ネットワークなど
* Othello_MCTS.py:モンテカルロ探索など
* Othello_valueNetwork.py;バリューネットワークなど
* Othello_play.py:オセロUI部

# 作者
* zeke
* KMC,KUB2
* zeke@kmc.gr.jp

何かありましたらご連絡ください
