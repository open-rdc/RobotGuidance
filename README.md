# RobotGuidance

RobotGuidance関連の写真・動画  
https://goo.gl/photos/rMGQ5qAvPw3LWZHn7

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

中村くんの研究
```
#中村くんのPC(server)
以下の２つのコマンドを、各terminalで必ず最初に実行すること
export ROS_MASTER_URI=http://[中村くんのPCのIP]:11311 # 例 export ROS_MASTER_URI=http://192.168.0.39:11311
export ROS_IP=[中村くんのPCのIP] # 例 export ROS_IP=192.168.0.39


roslaunch robot_guidance interaction_robot_sim.launch # or interaction_robot.launch for real robot
roslaunch robot_guidance uvc_camera_node0.launch # or 'node1' for /dev/video1
rosrun rosserial_python serial_node.py
rosrun robot_guidance robot_move.py
rosrun robot_guidance guidance_reward.py

#学習PC
以下の２つのコマンドを、各terminalで必ず最初に実行すること
export ROS_MASTER_URI=http://[中村くんのPCのIP]:11311 # 例 export ROS_MASTER_URI=http://192.168.0.39:11311
export ROS_IP=[学習PCのIP] # 例 export ROS_IP=192.168.0.53


rosrun robot_guidance robot_guidance_node.py
```
