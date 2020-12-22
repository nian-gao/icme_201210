import os
from data.base_dataset import BaseDataset, get_params, get_transform
from data.image_folder import make_dataset
import cv2
from PIL import Image
import numpy


class MultipleDataset(BaseDataset):
    def __init__(self, opt):
        BaseDataset.__init__(self, opt)
        self.dir_CEMB = os.path.join(opt.dataroot, opt.phase)  # get the image directory
        self.CEMB_paths = sorted(make_dataset(self.dir_CEMB, opt.max_dataset_size))  # get image paths
        assert (self.opt.load_size >= self.opt.crop_size)  # crop_size should be smaller than the size of loaded image
        self.input_nc = self.opt.output_nc if self.opt.direction == 'BtoA' else self.opt.input_nc
        self.output_nc = self.opt.input_nc if self.opt.direction == 'BtoA' else self.opt.output_nc

    def __len__(self):
        return len(self.CEMB_paths)

    def __getitem__(self, index):
        CEMB_path = self.CEMB_paths[index]
        # AB = cv2.open(AB_path).convert('RGB')
        # CEMB = cv2.imread(CEMB_path)
        CEMB = Image.open(CEMB_path).convert('RGB')
        # split CEMB image into C,E,M,B
        w, h = CEMB.size
        w4 = int(w / 4)
        # A = AB.crop((0, 0, w2, h))  # (left, up, right, down) # todo img crop position
        # B = AB.crop((w2, 0, w, h))
        C = CEMB.crop((0, 0, w4, h))
        E = CEMB.crop((w4, 0, w4 * 2, h))
        M = CEMB.crop((w4 * 2, 0, w4 * 3, h))
        B = CEMB.crop((w4 * 3, 0, w, h))
        C = cv2.cvtColor(numpy.asarray(C), cv2.COLOR_RGB2BGR)
        E = cv2.cvtColor(numpy.asarray(E), cv2.COLOR_RGB2BGR)
        M = cv2.cvtColor(numpy.asarray(M), cv2.COLOR_RGB2BGR)
        B = cv2.cvtColor(numpy.asarray(B), cv2.COLOR_RGB2BGR)
        A = cv2.merge([C, E, M])


        # apply the same transform to both B and ori
        transform_params = get_params(self.opt, A.shape)
        A_transform = get_transform(self.opt, transform_params, grayscale=(self.input_nc == 1))
        B_transform = get_transform(self.opt, transform_params, grayscale=(self.output_nc == 1))

        A = A_transform(A)
        B = B_transform(B)

        return {'A': A, 'B': B, 'A_paths': CEMB_path, 'B_paths': CEMB_path}
