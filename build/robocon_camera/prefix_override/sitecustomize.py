import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/thien123/ROS2WS/robocon_ws/install/robocon_camera'
