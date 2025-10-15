# Gazebo on ROS2

## URDF files:

Urdf file structure 
```xml
<!-- Define for file type-->
<?xml version="1.0" encoding="UTF-8"?>
< robot name="your_robot_name">
<!-- Define colors-->
<material></material>
<!-- Define links-->
<link></link>
<!-- Define joints-->
<joint></joint>
<!-- Gazebo plugins-->
<gazebo></gazebo>
</robot>
```

Include mesh file to your urdf :
```xml
<geometry>
     <mesh filename="file:///home/thien123/ROS2WS/robocon_ws/install/robot_description/share/robot_description/mesh/sensors/lds.stl" scale="0.001 0.001 0.001"/>
</geometry>
```


### Xacro
Writing URDF files with xacro for easily file managing and editing.
We can separate our urdf robot model in to components such as: color, body/base , camera, lidar. And all of these can be combined into a main file to build a complete robot.
Main file structure :
 ```xml
<?xml version="1.0" encoding="UTF-8"?>
<robot name ="thien_robot" xmlns:xacro="http://www.ros.org/wiki/xacro">
    <xacro:include filename="urdf_file_name.xacro"/>
    <xacro:include filename="urdf_file_name2.xacro"/>
</robot>
```
Using xacro property namespace is a method to shorten your urdf file.

Sub file structure : 
```xml
<?xml version="1.0" encoding="UTF-8"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro">
    <!-- var using xacro--> 
    <xacro:property name="base_length" value="0.3" />
    <xacro:property name="base_width" value="0.19" />
    <xacro:property name="base_height" value="0.12" />
    <!-- Define links -->
   <link name="base_link"></link>
   <joint name="base_joint" type="fixed"></joint>
```



## Using Gazebo

### Installing Gazabo Classic (Gazebo11) on ROS2 humble

Use this link :   https://gazebosim.org/docs/latest/install_gz11_side_by_side/
 
 For using STL model in Gazebo use this configuration:
```xml
      <geometry>
        <mesh filename="file:///home/thien123/ROS2WS/robocon_ws/install/robot_description/share/robot_description/mesh/sensors/lds.stl" scale="0.001 0.001 0.001"/>
      </geometry>
```
