## Define a custom srv and msg files 

Create new package using```ament_cmake``` .\
Create ```srv/ImageAnalysis.srv``` folder that contains msg/srv configuration files.\ 
To convert the interfaces you defined into language-specific code (like C++ and Python) so that they can be used in those languages, add the following lines to ```CMakeList.txt``` :
```cmake 
find_package(geometry_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "srv/ImageAnalysis.srv"
  DEPENDENCIES geometry_msgs # Add packages that above messages depend on
)
ament_export_dependencies(rosidl_default_runtime)
```
Add build tool to the ``package.xml`` for generating language-specific code:
```xml
<depend>geometry_msgs</depend>
<buildtool_depend>rosidl_default_generators</buildtool_depend>
<exec_depend>rosidl_default_runtime</exec_depend>
<member_of_group>rosidl_interface_packages</member_of_group>
```
Now you can confirm that your interface creation worked by using the `ros2 interface show` command. The output you see in your terminal should look similar to the following:

<img width="1687" height="356" alt="image" src="https://github.com/user-attachments/assets/3d552796-f61a-4b1d-ad53-c0a6ee65d458" />

## Import custom srv type into your package

In your new packages that are in the same workspace as the Interfaces define package. Add the dependencies in your `package.xml`:
```xml
  <depend>rclpy</depend>
  <depend>sensor_msgs</depend>
  <depend>std_msgs</depend>
  <depend>cv_bridge</depend>
  <depend>robocon_interfaces</depend>
```

## 🛠 How It Works

The system consists of two main nodes:

- **Server Node (`camera_server`)**
  - Provides services for analyzing images.
  - Handles requests for:
    - **Brightness analysis** – calculates the average brightness of the image.
    - **Motion detection** – detects motion by comparing pixel differences.

- **Client Node (`client`)**
  - Sends service requests to the server.
  - Behavior depends on parameters:
    - `analyze=True` → requests brightness analysis.
    - `detect=True` → requests motion detection.

### 🔄 Sequence of Events

1. Launch file starts both `camera_server` and `client` nodes.  
2. The client reads its parameters (`analyze`, `detect`) from the launch arguments.  
3. The client sends a request to the server:  
   - If `analyze=True`, server responds with average brightness value.  
   - If `detect=True`, server responds with motion detection result.  
4. The server processes the image using OpenCV and returns the result to the client.  
5. The client outputs or logs the received response.


## Using Gazebo

### Installing Gazabo Classic (Gazebo11) on ROS2 humble

Use this link :   https://gazebosim.org/docs/latest/install_gz11_side_by_side/
 
 For using STL model in Gazebo use this configuration:
```xml
      <geometry>
        <mesh filename="file:///home/thien123/ROS2WS/robocon_ws/install/robot_description/share/robot_description/mesh/sensors/lds.stl" scale="0.001 0.001 0.001"/>
      </geometry>
```
