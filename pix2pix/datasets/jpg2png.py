import os

'''要重命名的图片路径'''
file_path = "/home/lab315/workzyf/pix2pix_demo/datasets/edges2face/B/train"
files = os.listdir(file_path)
for file in files:
    if file.endswith('jpg'):
        # 要指明重命名之后的路径
        src = os.path.join(file_path, file)
        r_name = file.split('.')[0] + '.png'
        dct = os.path.join(file_path, r_name)
        os.rename(src, dct)
