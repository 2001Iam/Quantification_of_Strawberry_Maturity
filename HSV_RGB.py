import cv2
import glob
import numpy as np
import  os
# def create_folders(folders):
#     for folder in folders:
#


path = r'/home/xplv/fenghao/demo/polygon_crop/*.png'
files = glob.iglob(path)
for file in files:
    img = cv2.imread(file)
    label = file.split('/')[6].split('_')[0]
    photos_num = file.split('/')[6].split('_')[1] + '_' + file.split('/')[6].split('_')[2].split('.')[0]
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv_img)  # 分离hsv三个通道
    h_c, h_r = h.shape
    for i in range(h_c):
        for j in range(h_r):
            if ((h[i][j]>=0 and h[i][j]<=30) or (h[i][j]>=151 and h[i][j]<=180)) and s[i][j]>100 and v[i][j]>200:
                hue = h[i][j]
                # count = 0
                count = int(hue//5)+1
                r, g, b = img[i][j]
                color = (r, g, b)
                rgb_image = np.full((110, 110, 3), color, dtype=np.uint8)
                folder = f"/home/xplv/fenghao/demo/0{count}"
                if not os.path.exists(folder):
                    os.makedirs(folder)
                cv2.imwrite(f'{folder }/{h[i][j]:03d}_{s[i][j]:03d}_{v[i][j]:03d}.jpg', rgb_image)
