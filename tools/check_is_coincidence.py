import cv2
import glob
import numpy as np

path1 = r'/home/xplv/fenghao/Self-Supervised-Leaf-Segmentation/modify_Input_num164/img_*.jpg'
files1 = glob.iglob(path1)
sorted_files1 = sorted(files1)
path2 = r'/home/xplv/fenghao/Self-Supervised-Leaf-Segmentation/modify_Output_num164/truth_*.png'
files2 = glob.iglob(path2)
sorted_files2 = sorted(files2)

for i in range(0, 163):
    print(sorted_files1[i])
    print(sorted_files2[i])
    img1 = cv2.imread(sorted_files1[i], -1)
    img2 = cv2.imread(sorted_files2[i], -1)*255
    img2 = np.expand_dims(img2, axis=-1).astype(np.uint8)
    combine = img1 // 2 + img2 // 2
    cv2.imwrite(f'Output_163/combine_{i}.png',combine)