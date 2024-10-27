import cv2
import numpy as np
from utils.image_processing import apply_erosion, apply_dilation


class LaserDetector:
    def __init__(self, red_lower, red_upper, brightness_threshold, min_area, max_area, focal_length=500):
        self.red_lower = red_lower
        self.red_upper = red_upper
        self.brightness_threshold = brightness_threshold
        self.min_area = min_area
        self.max_area = max_area
        self.focal_length = focal_length  # 校准用的焦距（以像素为单位）

    def detect(self, frame):
        # 转换为HSV颜色空间
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # 根据颜色范围提取红色激光
        mask = cv2.inRange(hsv, self.red_lower, self.red_upper)
        mask = apply_erosion(mask)
        mask = apply_dilation(mask)

        # 寻找轮廓并过滤符合面积阈值的区域
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if self.min_area <= area <= self.max_area:
                x, y, w, h = cv2.boundingRect(contour)
                coordinates = (x + w // 2, y + h // 2)  # 中心坐标
                distance = self.calculate_distance(w)  # 根据宽度估算距离
                return True, coordinates, (x, y, w, h), distance

        return False, None, None, None  # 未检测到激光

    def calculate_distance(self, width):
        # 使用焦距和物体宽度估算距离，假设激光点宽度已知
        known_width = 0.01  # 假设激光的真实宽度为 1 厘米
        distance = (known_width * self.focal_length) / width
        return round(distance, 2)  # 返回米，保留两位小数
