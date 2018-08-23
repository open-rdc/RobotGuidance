# RobotGuidance

### 研究発表
Theerapap Pasin、林原 靖男，”強化学習を用いた移動ロボットの自律化に関する研究”，3E3-07，SI2017 (2017)  
[予稿集](https://docs.google.com/a/p.chibakoudai.jp/viewer?a=v&pid=sites&srcid=cC5jaGliYWtvdWRhaS5qcHxyb2JvdC1kZXNpZ24tYW5kLWNvbnRyb2wtbGFifGd4Ojc1OGY4YTE1M2FlMWVhMjY)

ティーラパップ・パシン、林原靖男、上田隆一，”強化学習を用いた移動ロボットの自律化に関する研究　一定の間隔で人を追従する行動の獲得に関する検討”，日本機械学会ロボティクス・メカトロニクス講演会'18，1A1-M11 (2018)  
[予稿集](https://docs.google.com/a/p.chibakoudai.jp/viewer?a=v&pid=sites&srcid=cC5jaGliYWtvdWRhaS5qcHxyb2JvdC1kZXNpZ24tYW5kLWNvbnRyb2wtbGFifGd4OjI1ODBkMWM0ZDMwNWE3NTE)

学習の様子  
https://youtu.be/YmjjVK531ms

### インストール
[ROS Kinetic](http://wiki.ros.org/ja/kinetic/Installation/Ubuntu)

How to run
```
roslaunch robot_guidance interaction_robot_sim.launch # or interaction_robot.launch for real robot
roslaunch robot_guidance uvc_camera_node0.launch # or 'node1' for /dev/video1
rosrun rosserial_python serial_node.py
rosrun robot_guidance robot_move.py
rosrun robot_guidance guidance_reward.py
rosrun robot_guidance robot_guidance_node.py
```

一つにまとめた
```
roslaunch robot_guidance robot_guidance.launch
```

Bagファイルを取る。
```
rosbag record -a
```

Bagファイルのデータを.csvにエクスポートする。
```
roscore
rostopic echo -b FILE.bag -p /TOPIC_NAME > FILE.csv
```


