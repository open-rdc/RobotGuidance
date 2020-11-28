# RobotGuidance

### 研究発表
Theerapap Pasin、林原 靖男，”強化学習を用いた移動ロボットの自律化に関する研究”，3E3-07，SI2017 (2017)  
[予稿集](https://docs.google.com/a/p.chibakoudai.jp/viewer?a=v&pid=sites&srcid=cC5jaGliYWtvdWRhaS5qcHxyb2JvdC1kZXNpZ24tYW5kLWNvbnRyb2wtbGFifGd4Ojc1OGY4YTE1M2FlMWVhMjY)

ティーラパップ・パシン、林原靖男、上田隆一，”強化学習を用いた移動ロボットの自律化に関する研究　一定の間隔で人を追従する行動の獲得に関する検討”，日本機械学会ロボティクス・メカトロニクス講演会'18，1A1-M11 (2018)  
[予稿集](https://docs.google.com/a/p.chibakoudai.jp/viewer?a=v&pid=sites&srcid=cC5jaGliYWtvdWRhaS5qcHxyb2JvdC1kZXNpZ24tYW5kLWNvbnRyb2wtbGFifGd4OjI1ODBkMWM0ZDMwNWE3NTE)

### 学習の様子  
動画  
https://youtu.be/YmjjVK531ms

コンピュータ内での挙動の確認
https://youtu.be/TDZAsw2hM-c

### インストール
１）ROS Kineticのインストール  
http://wiki.ros.org/ja/kinetic/Installation/Ubuntu  

２）orne-navigationのインストール  
以下のインストール用をスクリプトを実行   
https://github.com/open-rdc/orne_navigation/wiki/ORNE%E7%92%B0%E5%A2%83%E3%81%AE%E6%A7%8B%E7%AF%89%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6

### RobotGuidanceのダウンロード・ビルド

```
cd ~
git clone https://github.com/open-rdc/RobotGuidance

cd ~/catkin_ws/src/
ln -s ../../RobotGuidance/ros/robot_guidance/
catkin build

sudo apt-get install python-pip
pip install chainerrl scikit-image gym[atari]

```

### 深層学習の動作確認

```
cd ~/RobotGuidance/chainer_sample
python sample_cart_pole.py
or
python sample_pong.py
```

画像に対する行動選択をコンピュータ内で実行して挙動を確認

```
roslaunch robot_guidance_check robot_guidance_check.launch

launchファイルの説明
robot_guidance_check_all.launch　左右前後移動の学習
robot_guidance_check_fb.launch　左右移動の学習
robot_guidance_check_lr.launch　前後移動の学習
```

### Bagファイルへの保存とCSVへのエクスポート

```
rosbag record -a
roscore
rostopic echo -b FILE.bag -p /TOPIC_NAME > FILE.csv
```
### simple controllerによる学習　20/11/29追加

Deep Learning
```
roslaunch robot_guidance_check robot_guidance_check_dl.launch
```

https://youtu.be/KDSkP_7GAXg

Joystick
```
roslaunch robot_guidance_check robot_guidance_check_joy.launch
```

https://youtu.be/UrEx80zfJ7M
