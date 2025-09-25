#!/usr/bin/env python3
from rclpy.node import Node
import cv2
import numpy as np
import time
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from robocon_interfaces.srv import ImageAnalysis


class CameraServer(Node):
    def __init__(self):
        super().__init__('camera_server')
        self.publisher_ = self.create_publisher(Image, 'camera/image', 10)
        self.server_= self.create_service(ImageAnalysis,'image_analysis', self.image_analyzer_callback)
        self.timer = self.create_timer(0.2, self.timer_callback)  
        self.cap = cv2.VideoCapture("/dev/video0")  
        self.bridge = CvBridge()

    def timer_callback(self):
        ret, frame = self.cap.read()
        if ret:
            msg = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
            self.publisher_.publish(msg)
            self.get_logger().info('Published image frame')
        else:
            self.get_logger().error('Failed to capture image')

    def __del__(self):
        self.cap.release()

    def image_analyzer_callback(self, request, response):
        ret, frame = self.cap.read()
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        response.analysis_result = "Not implemented"                    # giá trị mặc định
        response.avg_brightness = 0.0
        response.motion_detected = False
        if not ret :
                self.get_logger().error('Failed to capture image')
                response.analysis_result = "Not implemented"
                return response                                      # return luôn tại đây 
            
        if request.analyze_brightness :
            response.analysis_result = " Analizing success"                         
            response.avg_brightness = float(gray_frame.mean())                   # Chuyen sang mau xam de do brightness
     
        if request.detect_motion:
            self.get_logger().info("Waiting 1 second before capturing final frame...")
            initial_frame = gray_frame.copy()
            time.sleep(2)   # chờ 1 giây
            ret, frame_2 = self.cap.read()
            final_frame = cv2.cvtColor(frame_2, cv2.COLOR_BGR2GRAY)
            if not ret:
                response.analysis_result = "Capture error"
                return response
            diff = cv2.absdiff(final_frame, initial_frame) # giải quyết vấn đề khoảng thời gian mà client muốn detect
            motion_detected = np.any(diff > 30)  # Simple thresholding for motion detection
            response.motion_detected = bool(motion_detected)
            
        return response
            

def main(args=None):
    import rclpy
    rclpy.init(args=args)
    camera_node = CameraServer()
    rclpy.spin(camera_node)
    camera_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()