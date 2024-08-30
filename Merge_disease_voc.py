import os

import cv2
import numpy as np
import glob


def overlay_image_opencv(background_path, overlay, output_path, scale_percent, num, cls):
    """
    将缩放后的图像叠加到背景图像上。

    :param background_path: 背景图像文件路径
    :param overlay_path: 叠加图像文件路径
    :param output_path: 输出图像保存路径
    :param scale_percent: 缩放比例（百分比）
    :param position: 叠加图像的位置（x, y）
    """

    # 读取图像
    background = cv2.imread(background_path)
    back_h, back_w = background.shape[:2]
    position = (int(back_w / 2), int(back_h / 2))
    # 计算缩放尺寸
    width = int(overlay.shape[1] * scale_percent / 100)
    height = int(overlay.shape[0] * scale_percent / 100)
    new_size = (width, height)
    # scale_points =[]
    # for new_point in new_points:
    #     x,y=new_point
    #     x=int(x*scale_percent / 100)
    #     y=int(y*scale_percent / 100)
    #     scale_points.append([x,y])
    # 缩放叠加图像
    overlay_resized = cv2.resize(overlay, new_size, interpolation=cv2.INTER_LINEAR)
    back_mask = np.zeros((back_h, back_w, 3), dtype=np.uint8)
    mask = cv2.cvtColor(overlay_resized, cv2.COLOR_BGR2GRAY)
    mask[mask == 0] = 1
    mask[mask > 1] = 0
    # mask_3channel = cv2.merge([mask, mask, mask])
    # 确保背景图像有足够的大小
    x, y = position

    if x + width > background.shape[1] or y + height > background.shape[0]:
        x = 50
        y = 50

        # raise ValueError("叠加图像超出了背景图像的范围")
    # 提取 alpha 通道
    # if overlay_resized.shape[2] == 4:
    #     alpha = overlay_resized[:, :, 3] / 255.0
    #     overlay_resized = overlay_resized[:, :, :3]
    # else:
    #     alpha = np.ones((height, width))

    # 叠加图像
    # for c in range(3):
    #     background[y:y + height, x:x + width, c] = (
    #             alpha * overlay_resized[:, :, c] + (1 - alpha) * background[y:y + height, x:x + width, c])
    # background = np.multiply(background[y:y + height, x:x + width, :], mask_3channel)
    for c in range(3):
        background[y:y + height, x:x + width, c] = (
                (1 - mask) * overlay_resized[:, :, c] + mask * background[y:y + height, x:x + width, c])
    alpha = np.ones((height, width))
    for c in range(3):
        back_mask[y:y + height, x:x + width, c] = (
                alpha * overlay_resized[:, :, c] + (1 - alpha) * back_mask[y:y + height, x:x + width, c])
    # 保存输出图像
    output_path = output_path + f'/disease_voc_{num:02d}.png'
    cv2.imwrite(output_path, background)
    cv2.imwrite(f'/home/xplv/fenghao/Merge_disease_voc_59images/mask/disease_voc_{num:02d}.png', back_mask)
    print(f"图像已保存到 {output_path}")

    # 将图像转换为灰度图像
    gray = cv2.cvtColor(back_mask, cv2.COLOR_BGR2GRAY)
    # 应用二值化或边缘检测
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)

    # 查找轮廓
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 文件路径
    label_path = f'/home/xplv/fenghao/Merge_disease_voc_59images/labels/disease_voc_{num:02d}.txt'

    # 写入归一化后的轮廓数据到 TXT 文件
    with open(label_path, 'w') as file:
        file.write(f'{cls}')
        for i, contour in enumerate(contours):
            for point in contour:
                # 点的坐标是 [x, y]，point[0] 是轮廓点的坐标
                x, y = point[0]
                # 归一化坐标
                x_normalized = x / back_w
                y_normalized = y / back_h
                file.write(f' {x_normalized:.15f} {y_normalized:.15f}')
        file.write('\n')

    print(f'归一化的轮廓数据已成功写入到 "{label_path}"')
    # res_points = []
    # for scale_point in scale_points:
    #     scale_x, scale_y = scale_point
    #     res_x = (x + scale_x) / back_w
    #     res_y = (y + scale_y) / back_h
    #     res_points.append([res_x, res_y])
    # label_path = f'/home/xplv/fenghao/Merge_disease_voc_59images/labels/disease_voc_{num:02d}.txt'
    # with open(label_path, 'w', encoding='utf-8') as file:
    #     line = str(cls)
    #     for res_point in res_points:
    #         # 将标签信息格式化为字符串并写入文件
    #         x, y = res_point
    #         line = line + ' ' + str(x) + ' ' + str(y)
    #     line = line + '\n'
    #     file.write(line)


# 示例用法
background_path = r'/home/xplv/fenghao/VOC_59images/*'
background_files = list(sorted(glob.iglob(background_path)))
print()
save_path = '/home/xplv/fenghao/Merge_disease_voc_59images/images'
scale_percent = 50  # 缩放比例为 50%
# position = (100, 100)  # 叠加位置 (x, y)
path = r'/home/xplv/fenghao/near_disease_3/images/*'
files = glob.iglob(path)
num = 0
for file in files:
    img = cv2.imread(file)
    h, w = img.shape[:2]
    original_img = img
    file_name = file.split('/')[6][:-4]
    # file_name = file.split('/')[7].split('.')[0]
    label_path = f'/home/xplv/fenghao/near_disease_3/labels/{file_name}.txt'
    index = 0
    cls = []
    with open(label_path, 'r') as file:
        for line in file:
            img = original_img
            line_list = line.split(' ')
            # if line_list[0]!='6':
            #     continue
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
            # new_points = []
            # for point in points:
            #     x, y = point
            #     new_points.append([x - x_min, y - y_min])
            points_array = np.array(points, dtype=np.int32)
            polygon = points_array.reshape((-1, 1, 2))
            mask = np.zeros(img.shape[:2], dtype=np.uint8)
            cv2.fillPoly(mask, [points_array], 255)
            points.clear()
            masked_img = cv2.bitwise_and(img, img, mask=mask)
            black_pixels_mask = mask == 0
            masked_img[black_pixels_mask] = [0, 0, 0]
            imgCrop = masked_img[int(y_min):int(y_max), int(x_min):int(x_max)].copy()
            overlay_image_opencv(background_files[num], imgCrop, save_path, scale_percent, num, cls[index])
            index += 1
            num += 1
