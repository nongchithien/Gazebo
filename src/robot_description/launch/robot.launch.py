import os
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.substitutions import PythonExpression
from launch_ros.actions import Node


def generate_launch_description():
    
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    xacro_file = 'my_robot.urdf.xacro'
    urdf_file = 'my_robot.urdf'
    urdf_gz= 'model.sdf'
    pkg_gazebo_ros= get_package_share_directory("gazebo_ros")
    frame_prefix = LaunchConfiguration('frame_prefix', default='')

    # print('urdf_file_name : {}'.format(urdf_file_name))

    # Lấy path file urdf, world ,rviz
    urdf_path_pub = os.path.join(
        get_package_share_directory('robot_description'),
        'urdf',
         urdf_file)
    urdf_path_gz = os.path.join(
        get_package_share_directory('robot_description'),
        'mesh',
        urdf_gz)

    xacro_path = os.path.join(
        get_package_share_directory('robot_description'),
        'urdf',
        xacro_file)
    # urdf_file_name = Command(['xacro ', xacro_path])
        
    with open(urdf_path_pub, 'r') as infp:                  # để  có thể đọc file urdf
        robot_desc = infp.read()
        
    world_path = os.path.join(
        get_package_share_directory("robot_description"),
        "world",
        "house.world"
    )
    rviz_path= os.path.join(get_package_share_directory('robot_description'),'rviz2','config.rviz')
    
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation (Gazebo) clock if true'),
        
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            parameters=[{
                'use_sim_time': use_sim_time,
                "robot_description": robot_desc,   # Lấy file urdf
                'frame_prefix': PythonExpression(["'", frame_prefix, "/'"]),
                
            }],
        ),
        

        #Start Gazebo server
        IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzserver.launch.py')
        ),
        launch_arguments={'world': world_path}.items()
        ),
        #Start Gazebo Client
        IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzclient.launch.py')
        )
        ),
        # Node(
        # package="joint_state_publisher",
        # executable="joint_state_publisher"
        # ),
        
        Node(
        package='rviz2',
        executable='rviz2',
        arguments=[' -d', rviz_path]
        ),
        
        Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=["-file", urdf_path_pub, "-entity", 'thien'
        ]),
    ])
