import os
import glob
import shutil
import cv2 as cv

path = r'/home/xplv/fenghao/Market/pytorch/val/*'
files = glob.iglob(path)
sorted_files = sorted(files)
count_Ripe = 0
count_Ripe7 = 0
count_Ripe4 = 0
count_Ripe2 = 0
count_Unripe = 0
for file in sorted_files:
    new_path = file + "/*.jpg"
    new_files = glob.iglob(new_path)
    new_sorted_files = sorted(new_files)
    for new_file in new_sorted_files:
        print(new_file)
        if 'Ripe_' in new_file:
            count_Ripe += 1
        elif 'Ripe7_' in new_file:
            count_Ripe7 += 1
        elif 'Ripe4_' in new_file:
            count_Ripe4 += 1
        elif 'Ripe2_' in new_file:
            count_Ripe2 += 1
        elif 'Unripe_' in new_file:
            count_Unripe += 1
print(f'count_Ripe:{count_Ripe}')
print(f'count_Ripe7:{count_Ripe7}')
print(f'count_Ripe4:{count_Ripe4}')
print(f'count_Ripe2:{count_Ripe2}')
print(f'count_Unripe:{count_Unripe}')
