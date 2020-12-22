import os
import shutil
from PIL import Image
import cv2


def each_file(e_filepath, c_filepath, dst_filepath):
    c_dirs = os.listdir(c_filepath)  # 读取目录下的文件或文件夹
    for c_dir in c_dirs:  # 进行循环
        e = os.path.join('%s/%s' % (e_filepath, c_dir))  # 构造路径
        c = os.path.join('%s/%s' % (c_filepath, c_dir))
        dst = os.path.join('%s/%s' % (dst_filepath, c_dir))
        if os.path.isfile(e):  # 如果是文件类型就执行转移操作
            edge = cv2.imread(e)
            # edge = 255 - edge
            color = cv2.imread(c)
            c_gray = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)
            ret, mask = cv2.threshold(c_gray, 5, 255, cv2.THRESH_BINARY)
            mask_inv = cv2.bitwise_not(mask)
            edge_bg = cv2.bitwise_and(edge, edge, mask=mask_inv)
            destination = cv2.add(edge_bg, color)
            cv2.imwrite(dst, destination)


if __name__ == '__main__':
    # add edge and c
    e_path = "./E/train/"
    c_path = "./C/train/"
    dst_path = "./CE/train/"
    each_file(e_path, c_path, dst_path)
