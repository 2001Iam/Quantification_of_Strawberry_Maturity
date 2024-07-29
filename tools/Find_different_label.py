import glob
import cv2


def top_n_scores(n, pN):
    ''' returns the n scores from a name:score dict'''
    lot = [(k, v) for k, v in pN.items()]  # make list of tuple from scores dict
    nl = []
    while len(lot) > 0:
        nl.append(max(lot, key=lambda x: x[1]))
        lot.remove(nl[-1])
    return nl[0:n]


path = r'/home/xplv/fenghao/Market/pytorch/train_all/*'
files = glob.iglob(path)
sorted_files = sorted(files)
count = 0
lis = []
for file in sorted_files:
    count += 1
    path_img = file + '/*.jpg'
    files_img = glob.iglob(path_img)
    flag = -1
    num = 0
    mp = {'Ripe': 0, 'Ripe7': 0, 'Ripe4': 0, 'Ripe2': 0, 'Unripe': 0}
    for file_img in files_img:
        key = file_img.split('_')[4]
        mp[key] += 1
        if flag != key:
            flag = key
            num += 1
    if (num > 1):
        new_mp = top_n_scores(2, mp)
        first_key = next(iter(new_mp))
        ID = file.split('/')[7]
        if (first_key[0] == 'Ripe' or first_key[0] == 'Unripe'):
            count = 0
            for pair in new_mp:
                if count == 1:
                    #print(f'{ID},{pair[0]}')
                    lis.append(f'{ID},{pair[0]}')
                else:
                    count += 1



        else:
            #print(f'{ID},{first_key[0]}')
            lis.append(f'{ID},{first_key[0]}')
i = 0
score = 0
print(len(lis))
lis.append('hhh')
with open('Input.txt', 'r') as file:
    for line in file:
        new_line=line.split('\n')[0]
        if new_line == (lis[i]+'_'):
            score += 1
            print(new_line)
            print(lis[i] + '_')
        i += 1
print(score/120)