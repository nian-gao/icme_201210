#  14-post process in pix2pix
#  Binarize the edge maps and discard trivial edges which less than 10 pixels
#  denoise is necessary or not?
import cv2
import scipy.ndimage


def post_process(i):
    # or cv2.ADAPTIVE_THRESH_MEAN_C
    # mean_c and gaussian_c are similar. choose one.
    o = cv2.adaptiveThreshold(i, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 0)
    o = scipy.ndimage.median_filter(o, (5, 5))
    o = scipy.ndimage.median_filter(o, (5, 5))
    return o
