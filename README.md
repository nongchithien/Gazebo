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


### Using Xacro to clean up your code
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
The xacro program runs all of the macros and outputs the result. Typical usage looks something like this:
```bash xacro model.xacro > model.urdf ```
## RVIZ
In order to visualize your urdf file in Rviz, you must let robot_state_publisher publish urdf file. Then Rviz will listen to this topic and visualize it in the Rviz GUI.\
Also, if you are using a continuous joint type, you must run joint_state_publisher , by doing this Rviz can understand the transform of this file.
In your launch file :
```python
Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            parameters=[{
                'use_sim_time': use_sim_time,
                "robot_description": robot_desc,   # Getting urdf file with file path
                'frame_prefix': PythonExpression(["'", frame_prefix, "/'"]),
            }],
        ),
 Node(
            package="joint_state_publisher",
            executable="joint_state_publisher"
        ),
        
Node(
            package='rviz2',
            executable='rviz2',
            arguments=[' -d', rviz_path] # Rviz configuration pre-setting
     ,
```


## Using Gazebo

### Installing Gazabo Classic (Gazebo11) on ROS2 humble

Use this link :   https://gazebosim.org/docs/latest/install_gz11_side_by_side/

 The most common error while using Gazebo is the mesh file config.
 For using STL model in Gazebo use this configuration:
```xml
      <geometry>
        <mesh filename="file:///home/thien123/ROS2WS/robocon_ws/install/robot_description/share/robot_description/mesh/sensors/lds.stl" scale="0.001 0.001 0.001"/>
      </geometry>
```
In the Classic Gazebo, you have to launch the Gazebo Server, Client and Spawn Entity to spawn your robot on Gazebo.
Gazebo Server can be run with a world file.


### Package.xml
```xml
  <exec_depend>gazebo_ros</exec_depend>
  <depend>gazebo_ros_pkg</depend>
```
### CMakeLists.txt
```cmake
find_package(gazebo_ros_pkgs REQUIRED)
install(
  DIRECTORY urdf launch rviz2 mesh world
  DESTINATION share/${PROJECT_NAME}/
)
ament_export_dependencies(gazebo_ros_pkgs)
```





