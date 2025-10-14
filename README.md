# Gazebo on ROS2

## Using Gazebo

### Installing Gazabo Classic (Gazebo11) on ROS2 humble

Use this link :   https://gazebosim.org/docs/latest/install_gz11_side_by_side/
 
 For using STL model in Gazebo use this configuration:
```xml
      <geometry>
        <mesh filename="file:///home/thien123/ROS2WS/robocon_ws/install/robot_description/share/robot_description/mesh/sensors/lds.stl" scale="0.001 0.001 0.001"/>
      </geometry>
```
