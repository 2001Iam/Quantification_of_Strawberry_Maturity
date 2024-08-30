import os
import cv2 as cv
import matplotlib.pyplot as plt
from collections import Counter
import glob
import numpy as np

threshold = 17
threshold_fun = 14


def calchist_for_rgb(img, frame, num, label):
    h, s, v = cv.split(frame)  # 分离hsv三个通道
    h_c, h_r = h.shape
    area = 0
    red_area = 0
    xy = np.argwhere(img != [0, 0, 0]) # xy中选取的是所有r！=0 and g！=0 and b！=0的像素点
    print("hhh")
    for coordinate in xy:
        i = coordinate[0]
        j = coordinate[1]
        if s[i][j] > 0 and v[i][j] > 0:
            area += 1
            if h[i][j] > 150 or h[i][j] < threshold:
                red_area += 1
    red_proporation = (red_area / area) * 100
    return red_proporation


def calchist_for_rgb_fun(img, frame, num, label):
    h, s, v = cv.split(frame)  # 分离hsv三个通道
    h_c, h_r = h.shape
    area = 0
    red_area = 0
    xy = np.argwhere(img != [0, 0, 0])
    print("hhh")
    for coordinate in xy:
        i = coordinate[0]
        j = coordinate[1]
        if s[i][j] > 0 and v[i][j] > 0:
            area += 1
            if h[i][j] > 150 or h[i][j] < threshold_fun:
                red_area += 1
            elif h[i][j] >= threshold_fun and h[i][j] < 17:
                red_area = red_area + (17-h[i][j])/3
    red_proporation = (red_area / area) * 100
    return red_proporation


if __name__ == '__main__':
    path = r'/home/xplv/fenghao_2/Quantification_of_Strawberry_Maturity/polygon_crop_aiwei/*.png'
    files = glob.iglob(path)
    index = 0
    for file in files:
        print(file)
        label = file.split('/')[6].split('_')[0]
        photos_num = file.split('/')[6].split('_')[1] + '_' + file.split('/')[6].split('_')[2].split('.')[0]
        # photos_num = file.split('/')[6].split('_')[1] + '_' + file.split('/')[6].split('_')[2]
        img = cv.imread(file)
        hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)

        # cv.imshow('frame', frame)
        # cv.waitKey(0)
        red_proporation = calchist_for_rgb(img, hsv_img, photos_num, label)
        cv.imwrite(
            f'/home/xplv/fenghao_2/test/{label}_{photos_num}_red_proporation:{red_proporation:.2f}%.jpg',
            img)
