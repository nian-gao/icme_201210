#  13-fast edge detection based on structured forests
import cv2
import numpy as np


def fast_edge_detection(i):
    detector = cv2.ximgproc.createStructuredEdgeDetection('./model.yml')
    src = cv2.cvtColor(i, cv2.COLOR_BGR2RGB)
    o = detector.detectEdges(np.float32(src) / 255.0)  # contains normalization
    o *= 255.0  # back to [0,255]
    o = o.astype(np.uint8)
    return o


def new_edge_detection(i):
    kernel = np.ones((3, 3), np.uint8)
    dilate = cv2.dilate(i, kernel, iterations=1)
    canny1 = cv2.Canny(dilate, 25, 100)
    return canny1
