#!/usr/bin/env python3
from robocon_interfaces.srv import ImageAnalysis                                                     # Import srv mới
import sys
import rclpy
import argparse
from rclpy.node import Node


class MinimalClientAsync(Node):

    def __init__(self):
        super().__init__('minimal_client_async')
        self.cli = self.create_client(ImageAnalysis, 'image_analysis')       
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = ImageAnalysis.Request()                                 
        self.declare_parameter('analyze', False)   # default = True
        self.declare_parameter('detect',False)  # default = False
        self.analyze_brightness = self.get_parameter('analyze').get_parameter_value().bool_value  # Lấy param từ Launch file
        self.detect_motion = self.get_parameter('detect').get_parameter_value().bool_value

    # def send_request(self): --->>>                   Neu khong dung Launch file thi lay param tu cmd 
    #     self.req.analyze_brightness= bool(int(sys.argv[1])) 
    #     self.req.detect_motion = bool(int(sys.argv[2])) 
    #     self.future = self.cli.call_async(self.req)

    def send_request(self):
        self.req.analyze_brightness= self.analyze_brightness
        self.req.detect_motion = self.detect_motion                          
        self.future = self.cli.call_async(self.req)


def main(args=None):
    rclpy.init(args=args)
    minimal_client = MinimalClientAsync()
    minimal_client.send_request()

    while rclpy.ok():
        rclpy.spin_once(minimal_client)
        if minimal_client.future.done():
            try:
                response = minimal_client.future.result()
            except Exception as e:
                minimal_client.get_logger().info(
                    'Service call failed %r' % (e,))
            else:
                minimal_client.get_logger().info(
                    '\nAverage brightness: %.2f \nMotion Detect     : %s \nAnalysis result   : %s' %                                # CHANGE
                    (response.avg_brightness, response.motion_detected , response.analysis_result ))  # trả về response của server
            break

    minimal_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()