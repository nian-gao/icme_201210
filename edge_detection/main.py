import cv2
import numpy as np
import os
from edge_detection.fed import new_edge_detection
from edge_detection.b2s import bin2svg, svg2img
from edge_detection.color_mask import generate_color_mask
from edge_detection.color_layer import get_color_data
import time
import shutil
import random
import albumentations as A


def encode(path):
    f_list = get_file_list(path)
    rand = random.randint(0, 100)
    test_list = [f_list[rand]]
    for index in range(400):  # len(f_list)
        f = f_list[index]
        mycopyfile(f, train_images_B_path + f.split("/")[-1])
        img_gray = cv2.imread(f, 0)
        img = cv2.imread(f)
        # strong_img = augmentation(img)
        edges = new_edge_detection(img_gray)
        cv2.imwrite("out.bmp", edges)
        bin2svg("out.bmp", "out.svg")
        # ppm_compress('out.svg')
        colors = get_color_data("out.svg", img)
        # print(len(colors))
        # -- decode --
        # ppm_decompress("out.svg.xdg", "out_d.svg")
        # os.remove("out.svg.xdg")
        svg2img("out.svg", "e.png")
        e = cv2.imread("e.png")
        train_images_E_path = "../pix2pix/datasets/E/train/"
        train_images_M_path = "../pix2pix/datasets/M/train/"
        train_images_C_path = "../pix2pix/datasets/C/train/"
        name = f.split("/")[-1]
        name = name.split(".")[0]
        cv2.imwrite(train_images_E_path + name + ".png", e)
        m, c = generate_color_mask("out.svg", colors)
        # cv2.imwrite("color.png", c)
        cv2.imwrite(train_images_M_path + name + ".png", m)
        cv2.imwrite(train_images_C_path + name + ".png", c)
        os.remove("out.svg")
        if index % 100 == 99:
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), str(index) + "/400")


def mycopyfile(srcfile, dstfile):
    if not os.path.isfile(srcfile):
        print("%s not exist!" % srcfile)
    else:
        fpath, fname = os.path.split(dstfile)  # 分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)  # 创建路径
        shutil.copyfile(srcfile, dstfile)  # 复制文件
        if fname.endswith('jpg'):
            # 要指明重命名之后的路径
            r_name = fname.split('.')[0] + '.png'
            dct = os.path.join(fpath, r_name)
            os.rename(dstfile, dct)


def new_image(width, height):
    binary = np.zeros((height, width), dtype=np.uint8)
    return cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)


def get_file_list(root_path):
    file_list = []
    files = os.listdir(root_path)
    for file in files:
        file_path = os.path.join(root_path, file)
        file_list.append(file_path)
    return file_list


def augmentation(input_image):
    transform = A.Compose([
        A.CLAHE(clip_limit=4.0, tile_grid_size=(4, 4), p=0.9)
    ])

    # Read an image with OpenCV and convert it to the RGB colorspace
    # image = cv2.imread("image.jpg")
    image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)

    # Augment an image
    transformed = transform(image=image)
    img = transformed["image"]
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)


if __name__ == '__main__':
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "start")
    train_images_B_path = "../pix2pix/datasets/B/train/"
    train_images_ori_path = "../pix2pix/datasets/ori/train"
    encode(train_images_ori_path)
