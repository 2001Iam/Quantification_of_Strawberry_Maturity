import cv2
import numpy as np

img = cv2.imread('test.png')
height,width= img.shape[:2]
print(width,height)
cls = []
with open('test.txt', 'r') as file:
    for line in file:
        line_list = line.split(' ')
        cls.append(line_list[0])
        points = []
        for i in range(1, len(line_list), 2):
            x = float(line_list[i]) * width
            # x = int(x * 1008)
            y = float(line_list[i + 1]) * height
            # y = int(y * 756)
            points.append([x, y])
        points_array = np.array(points, dtype=np.int32)
        polygon = points_array.reshape((-1, 1, 2))
        cv2.polylines(img, [polygon], True, (0, 255, 0), 2)
        points.clear()

cv2.imwrite('/home/xplv/fenghao/demo/res.png', img)
