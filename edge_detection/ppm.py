# 17- ppm compress
import os


compressor = r'../icme-20/ppm/ppm_compressor/build/compressor'


def ppm_compress(i):
    config = [
        '-c',
        i
    ]
    line = ' '.join([compressor] + config)
    print(line)
    os.system(line)


def ppm_decompress(i, o):
    config = [
        '-d',
        i,
        o
    ]
    line = ' '.join([compressor] + config)
    print(line)
    os.system(line)
