import os
import xml.etree.ElementTree as ET

# 类别列表，根据您的数据集设置类别
classes = ["hat"]  # 根据xml中的类别名称设置


def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    return (x * dw, y * dh, w * dw, h * dh)


# 确保标签目录存在
if not os.path.exists('labels'):
    os.makedirs('labels')

# 读取 ImageSets/Main/train.txt 中的图像编号
image_ids = open('ImageSets/Main/train.txt').read().strip().split()
for image_id in image_ids:
    in_file = open(f'Annotations/{image_id}.xml')  # 打开每个标注文件
    out_file = open(f'labels/{image_id}.txt', 'w')  # 创建对应的 .txt 文件

    tree = ET.parse(in_file)
    root = tree.getroot()

    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    # 遍历标注的对象
    for obj in root.iter('object'):
        cls = obj.find('name').text
        if cls not in classes:  # 如果类别不在指定列表中，跳过
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text),
             float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        out_file.write(f"{cls_id} {' '.join([str(a) for a in bb])}\n")  # 写入YOLO格式标签

    # 如果文件为空，则删除该文件
    out_file.close()
    if os.path.getsize(f'labels/{image_id}.txt') == 0:
        os.remove(f'labels/{image_id}.txt')