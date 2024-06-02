# 01数据集文本生成制作.py
import os

# 获取当前文件夹下所有文件名
file_name_list = os.listdir('/home/gl/FairMOT/dataset/MOT-15/images')

# 打开train.txt和test.txt文件，如果不存在则创建
train_file = open('train.txt', 'w')

# 设置训练集和测试集的比例为8:2
ratio = 0.8

# 遍历所有文件名，将图片路径写入对应的txt文件中
for i in range(len(file_name_list)):
    # 获取图片路径
    file_path = '/home/gl/FairMOT/dataset/MOT-15/images/' + file_name_list[i]
    # 判断是否为图片文件
    if file_path.endswith('.jpg') or file_path.endswith('.png'):
        # 如果是前80%的图片，则写入train.txt中，否则写入test.txt中
        
            train_file.write(file_path + '\n')
        

# 关闭txt文件
train_file.close()