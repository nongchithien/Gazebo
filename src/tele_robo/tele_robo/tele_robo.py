import os, sys, select, termios, tty, rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from rclpy.qos import QoSProfile

BURGER_MAX_LIN_VEL = 0.5
BURGER_MAX_ANG_VEL = 2.84
LIN_VEL_STEP_SIZE = 0.05
ANG_VEL_STEP_SIZE = 0.1

msg = """
Control Your Robot!
---------------------------
Moving around:
        w
   a    s    d
        x

space key, s : stop
CTRL-C to quit
"""

class TeleopNode(Node):
    def __init__(self):
        super().__init__('teleop_node')
        qos = QoSProfile(depth=10)
        self.pub = self.create_publisher(Twist, 'cmd_vel', qos)

        self.settings = termios.tcgetattr(sys.stdin)
        print(msg)
        self.main_loop()

    def main_loop(self):
        target_lin = target_ang = 0.0
        while True:
            key = self.get_key()
            if key == 'w':
                target_lin = min(target_lin + LIN_VEL_STEP_SIZE, BURGER_MAX_LIN_VEL)
            elif key == 'x':
                target_lin = max(target_lin - LIN_VEL_STEP_SIZE, -BURGER_MAX_LIN_VEL)
            elif key == 'a':
                target_ang = min(target_ang + ANG_VEL_STEP_SIZE, BURGER_MAX_ANG_VEL)
            elif key == 'd':
                target_ang = max(target_ang - ANG_VEL_STEP_SIZE, -BURGER_MAX_ANG_VEL)
            elif key in [' ', 's']:
                target_lin = target_ang = 0.0
            elif key == '\x03':
                break

            twist = Twist()
            twist.linear.x = target_lin
            twist.angular.z = target_ang
            self.pub.publish(twist)

    def get_key(self):
        tty.setraw(sys.stdin.fileno())
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        key = sys.stdin.read(1) if rlist else ''
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)
        return key


def main(args=None):
    rclpy.init(args=args)
    node = TeleopNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
