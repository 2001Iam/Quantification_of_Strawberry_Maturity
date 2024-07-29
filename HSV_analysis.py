import os
import cv2 as cv
import matplotlib.pyplot as plt
from collections import Counter
import glob

threshold = 80  # 区分度阈值


# 计算彩色图的直方图
def calchist_for_rgb(frame, num):
    h, s, v = cv.split(frame)  # 分离hsv三个通道
    hsv_H = cv.calcHist([h], [0], None, [256], [1, 255])
    hsv_S = cv.calcHist([s], [0], None, [256], [1, 255])
    # hsv_V = cv.calcHist([v], [0], None, [256], [0, 255])
    # ---------------- hsv均值 -----------------------
    hsv_sum = 0
    h_c, h_r = h.shape
    area = 0
    for i in range(h_c):
        for j in range(h_r):
            if h[i][j] != 0:
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

    plt.plot(hsv_H, color="r")
    plt.plot(hsv_S, color="g")
    # plt.plot(hsv_V, color="b")
    plt.savefig(f'/home/xplv/fenghao/demo/output_20240723_2/result_hsv{num}_mean-h:{mean_h:.2f}.jpg')
    plt.close()


# 色彩占比分析
def color_sort(frame, num):
    c = []
    for x in range(frame.shape[0]):
        for y in range(frame.shape[1]):
            c.append(str(frame[x, y][0]) + ',' + str(frame[x, y][1]) + ',' + str(frame[x, y][2]))  # 遍历图片所有bgr值
    temp = Counter(c)
    most = temp.most_common(500)  # 按重复次数排序，抽取排在前500的元素
    count = 1  # 状态值，记录是否是第一个被加入的元素，1代表是
    color = []  # 储存主色彩
    color_num = []  # 储存各主色彩的数量
    for i in most:
        b_i, g_i, r_i = i[0].split(',')  # 待加入色彩
        if count == 1:
            # 第一个被加入的色彩
            color.append(str(b_i) + ',' + str(g_i) + ',' + str(r_i))
            count = 0
            color_num.append(1)
        state = False  # 状态量，若变更为Ture为新颜色，决定加入color内
        for j in color:
            b_o, g_o, r_o = j.split(',')  # 已加入色彩
            # 计算待加入色彩和已加入色彩的区分度，若过为区分度超过阈值则视为要加入的新色彩
            dis = (int(b_o) - int(b_i)) ** 2 + (int(g_o) - int(g_i)) ** 2 + (int(r_o) - int(r_i)) ** 2
            if dis <= threshold:  # 区分度过小，视为列表内已经存在该色彩
                color_num[color.index(j)] += 1
                break
            else:
                state = True  # 修改状态量加入新色彩
            if state and j == color[len(color) - 1]:  # 若所有已有颜色都遍历后state仍为True则加入该色彩
                color.append(str(b_i) + ',' + str(g_i) + ',' + str(r_i))
                color_num.append(1)
                # print(color)
                # print(color_num)
    color_draw(frame, color, color_num, num)  # 绘制色彩占比图


# 绘制色彩占比图
def color_draw(frame, color, color_num, num):
    start = 0
    Height = frame.shape[0]
    Width = frame.shape[1]
    image = cv.resize(frame, (Width, int(Height * 1.125)))  # 创建新画布
    image[0:Height, 0:Width] = frame  # 在新画布上部分填充原图像
    for i in range(len(color)):
        # 遍历所有主色彩，
        # print(color[i])
        # print(float(color_num[i] / 5), '%')  # 计算百分比，因抽取500个颜色故此处除5便可计算百分比
        b, g, r = color[i].split(',')
        f = int(color_num[i]) * Width / 500  # 计算当前色彩应在画布上的宽度
        image[Height:int(Height * 1.125), start:start + int(f)] = [b, g, r]  # 上色
        start = start + int(f)
    image = cv.cvtColor(image, cv.COLOR_HSV2BGR)
    # cv.imshow(f'result_{num}' , image)
    cv.imwrite(f'/home/xplv/fenghao/demo/output_20240723_1/result_{num}.jpg', image)


def getfiles():
    file_path = '/Users/fbz/Desktop/City_Color/Photos'  # 文件夹路径
    file_names = os.listdir(file_path)
    print(file_names)
    return file_names, file_path


if __name__ == '__main__':
    path = r'/home/xplv/fenghao/demo/polygon_crop/*.png'
    files = glob.iglob(path)
    index = 0
    photos_num = 0
    for file in files:
        print(file)
        photos_num += 1
        img = cv.imread(file)
        hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        # cv.imshow('frame', frame)
        # cv.waitKey(0)
        calchist_for_rgb(hsv_img, photos_num)  # 第一个参数改为img可以获取BGR直方图
        color_sort(hsv_img, photos_num)  # 第一个参数改为img可以获取BGR直方图
