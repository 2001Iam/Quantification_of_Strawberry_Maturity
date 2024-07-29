# Quantification of Strawberry Maturity
## Getting Started
### 1、对在LabelStudio上标注过的草莓图像进行截取
草莓图像数据集有input_aiwei和input_plantfactory
```text
├── input_aiwei/
│   ├── images 
│       ├── img_001.jpg
│		├── labels
│       ├── labe_001.txt
```
以下命令可以实现草莓的截取
```
python draw_polygon.py
```


### 2、草莓HSV图像的色调、饱和度分布可视化以及平均值计算

```
python HSV_no_color_analysis.py
```

### 3、量化草莓成熟度

```
python red_proporation.py
```
## tools
### 检查彩色叶子图像与对应的灰度图（叶子真值）能否重合
```
python check_is_conincidence.py
```
### 根据多个坐标绘制多边形，将所包含的图像进行截取

```
python draw_polygon_function.py
```
### 根据文件名查看不同成熟度的草莓数量各有多少

```
python Find_category_distribution.py
```
### 将两张图像进行拼接

```
python Merge_images.py
```
### 统计图像分辨率的分布情况

```
python width_height_img.py
```
