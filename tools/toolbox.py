import cv2
import numpy as np

def readImage(path):
    return cv2.imread(path)

def extractParams(paramList, img):
    avg = np.average(img, axis = 0)
    return np.average(avg, axis = 0)
