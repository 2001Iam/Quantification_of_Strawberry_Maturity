import cv2
import numpy as np
import glob

path = r'/home/xplv/fenghao/demo/input_20240724/images/*.jpg'
files = glob.iglob(path)
sorted_files=sorted(files)
for file in sorted_files:
    img = cv2.imread(file)
    h, w = img.shape[:2]
    original_img = img
    ID = file.split('/')[7].split('_')[1].split('.')[0]
    label_path = f'/home/xplv/fenghao/demo/input_20240724/labels/label_{ID}.txt'
    index = 0
    cls = []
    with open(label_path, 'r') as file:
        for line in file:
            img = original_img
            line_list = line.split(' ')
            cls.append(line_list[0])
            points = []
            x_min = w
            y_min = h
            x_max = 0
            y_max = 0
            for i in range(1, len(line_list), 2):
                x = float(line_list[i]) * w
                # x = int(x * 1008)
                y = float(line_list[i + 1]) * h
                # y = int(y * 756)
                points.append([x, y])
                if x < x_min:
                    x_min = x
                if y < y_min:
                    y_min = y
                if x > x_max:
                    x_max = x
                if y > y_max:
                    y_max = y
            points_array = np.array(points, dtype=np.int32)
            polygon = points_array.reshape((-1, 1, 2))
            mask = np.zeros(img.shape[:2], dtype=np.uint8)
            cv2.fillPoly(mask, [points_array], 255)
            points.clear()
            masked_img = cv2.bitwise_and(img, img, mask=mask)
            black_pixels_mask = mask == 0
            masked_img[black_pixels_mask] = [0, 0, 0]
            # label=""
            if cls[index] =='0':
                label="Ripe"
            elif cls[index] =='1':
                label="Ripe7"
            elif cls[index] =='2':
                label="Ripe4"
            elif cls[index] =='3':
                label="Ripe2"
            elif cls[index] =='4':
                label="Unripe"
            cv2.imwrite(f'/home/xplv/fenghao/demo/polygon_crop_20240724/{label}_{ID}_{index:02d}.png',masked_img)
            index += 1
