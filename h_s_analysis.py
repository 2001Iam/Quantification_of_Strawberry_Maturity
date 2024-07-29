import glob
import cv2

path=r'/home/xplv/fenghao/demo/output_20240724_2/*.jpg'
files = glob.iglob(path)
Ripe = []
Ripe2 = []
Ripe4 = []
Ripe7 = []
Unripe = []
for file in files:
    label = file.split('/')[6].split('_')[0]
    ID=  file.split('/')[6].split('_')[1]+'_'+file.split('/')[6].split('_')[2]
    mean_h= file.split('/')[6].split(':')[1].split('_')[0]
    mean_s=file.split('/')[6].split(':')[2].split('.')[0]
    if label =='Ripe':
        Ripe.append((ID,mean_h,mean_s))
    elif label =='Ripe2':
        Ripe2.append((ID,mean_h,mean_s))
    elif label =='Ripe4':
        Ripe4.append((ID,mean_h,mean_s))
    elif label =='Ripe7':
        Ripe7.append((ID,mean_h,mean_s))
    elif label =='Unripe':
        Unripe.append((ID,mean_h,mean_s))
for res in Ripe:
    print(f'Ripe:{res}')
for res in Ripe7:
    print(f'Ripe7:{res}')
for res in Ripe4:
    print(f'Ripe4:{res}')
for res in Ripe2:
    print(f'Ripe2:{res}')
for res in Unripe:
    print(f'Unripe:{res}')