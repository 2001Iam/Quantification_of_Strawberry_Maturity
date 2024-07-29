import os
import cv2 as cv
import matplotlib.pyplot as plt
from collections import Counter
import glob
import numpy as np
threshold = 80  # 区分度阈值


# 计算彩色图的直方图
def calchist_for_rgb(frame, num,label):
    h, s, v = cv.split(frame)  # 分离hsv三个通道
    hsv_H = cv.calcHist([h], [0], None, [256], [1, 255])
    hsv_S = cv.calcHist([s], [0], None, [256], [1, 255])
    # hsv_V = cv.calcHist([v], [0], None, [256], [0, 255])
    # ---------------- hsv均值 -----------------------
    hsv_sum = 0
    h_c, h_r = h.shape
    area = 0
    xy = np.argwhere(img != [0, 0, 0])
    for coordinate in xy:
        i = coordinate[0]
        j = coordinate[1]
        if h[i][j]>=150:
            h[i][j]=h[i][j]%150
        else:
            h[i][j]+=31
        if s[i][j] > 0 and v[i][j] > 0:
            area += 1
        hsv_sum = hsv_sum + h[i][j]
    mean_h = hsv_sum / area
    # print('mean h =', mean_h)

    hsv_sum = 0
    s_c, s_r = s.shape
    for i in range(s_c):
        for j in range(s_r):
            hsv_sum = hsv_sum + s[i][j]
    mean_s = hsv_sum / area
    # print('mean s =', mean_s)

    hsv_sum = 0
    v_c, v_r = v.shape
    for i in range(v_c):
        for j in range(v_r):
            hsv_sum = hsv_sum + v[i][j]
    mean_v = hsv_sum / area
    # print('mean v =', mean_v)
    # 绘制并保存色彩直方图
    print(type(hsv_H))

    lis = []
    for i in range(150, 181):
        lis.append(hsv_H[i][0])
        hsv_H[i][0] = 0
    for i in range(149, -1, -1):
        hsv_H[i + 31][0] = hsv_H[i]
    for i in range(0, 31):
        hsv_H[i][0] = lis[i]
    plt.plot(hsv_H, color="r")
    plt.plot(hsv_S, color="g")
    # plt.plot(hsv_V, color="b")
    plt.savefig(f'/home/xplv/fenghao/demo/output_20240725_2/{label}_{num}_mean-h:{mean_h:.2f}_mean-s:{mean_s}.jpg')
    plt.close()


if __name__ == '__main__':
    path = r'/home/xplv/fenghao/demo/polygon_crop_aiwei/*.png'
    files = glob.iglob(path)
    index = 0
    for file in files:
        print(file)
        label = file.split('/')[6].split('_')[0]
        photos_num = file.split('/')[6].split('_')[1]+'_'+file.split('/')[6].split('_')[2].split('.')[0]
        #photos_num = file.split('/')[6].split('_')[1] + '_' + file.split('/')[6].split('_')[2]
        img = cv.imread(file)
        hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)

        # cv.imshow('frame', frame)
        # cv.waitKey(0)
        calchist_for_rgb(hsv_img, photos_num,label)  # 第一个参数改为img可以获取BGR直方图
        cv.imwrite(f'/home/xplv/fenghao/demo/output_20240725_1/{label}_{photos_num}.jpg',img)