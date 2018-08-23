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


