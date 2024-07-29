import os
import cv2 as cv
import matplotlib.pyplot as plt
from collections import Counter
import glob

path = r'/home/xplv/fenghao/demo/output_20240724_1/*.jpg'
files = glob.iglob(path)
for file in files:
    ID = file.split('/')[6].split('_')[2].split('.')[0]
    new_path = f'/home/xplv/fenghao/demo/output_20240724_2/hsv_{ID}_mean-h+31:*.jpg'
    new_files = glob.iglob(new_path)
    for new_file in new_files:
        mean_h = new_file.split('/')[6].split(':')[1].split('.')[0]
        new_file_2 = new_file
    img1 = cv.imread(file)
    img2 = cv.imread(new_file_2)
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]
    if img1.shape != img2.shape:
        img1 = cv.resize(img1, (w2,h2),interpolation=cv.INTER_NEAREST)
    combined_img_horizontal = cv.hconcat([img1, img2])
    cv.imwrite(f'/home/xplv/fenghao/demo/output_20240724/combined_{ID}_mean-h+31:{mean_h}.jpg', combined_img_horizontal)
