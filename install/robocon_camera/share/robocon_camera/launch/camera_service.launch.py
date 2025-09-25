from launch  import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    analyze_arg = DeclareLaunchArgument(
        'analyze', default_value='False',
        description=' Analyze brightness ?'
    )
    detect_arg = DeclareLaunchArgument(
        'detect', default_value='False',
        description=' Detect motion ?'
    )
    analyze = LaunchConfiguration('analyze')
    detect = LaunchConfiguration('detect')
    
    
    
    camera_service_node = Node(
            package='robocon_camera',
            executable='camera_server',
            name='cho_image'
            
    )
    minimal_client_async = Node(
            package='robocon_camera',
            executable='client',
            name='xin_image',
            parameters=[{'analyze': analyze,
                         'detect': detect}]
    )
        
    
    return LaunchDescription([
    analyze_arg,
    detect_arg,
    camera_service_node,
    minimal_client_async
])