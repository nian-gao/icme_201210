import os
import shutil
from PIL import Image


def each_file(filepath, new_filepath):
    """
    读取每个文件夹，将遇到的指定文件统统转移到指定目录中
    :param filepath: 想要获取的文件的目录
    :param new_filepath: 想要转移的指定目录
    :return:
    """
    global length
    l_dir = os.listdir(filepath)  # 读取目录下的文件或文件夹
    for one_dir in l_dir:  # 进行循环
        full_path = os.path.join('%s/%s' % (filepath, one_dir))  # 构造路径
        new_full_path = os.path.join('%s/%s' % (new_filepath, str(length)+".jpg"))
        if os.path.isfile(full_path):  # 如果是文件类型就执行转移操作
            if one_dir.split('.')[1] == 'jpg':  # 只转移txt文件，修改相应后缀就可以转移不同的文件
                img = Image.open(full_path)
                # if 235 < img.size[0] < 265 and 235 < img.size[1] < 265:  # train_big_set
                if 210 < img.size[0] < 290 and 210 < img.size[1] < 290:  # test_big_set
                    length += 1
                    shutil.copy(full_path, new_full_path)
        else:  # 不为文件类型就继续递归
            each_file(full_path, new_filepath)  # 如果是文件夹类型就有可能下面还有文件，要继续递归


if __name__ == '__main__':
    path = "/home/lab315/workzyf/vggface2-test"
    new_path = "datasets/edges2face/ori/test"
    length = 0
    each_file(path, new_path)
    print(length)
