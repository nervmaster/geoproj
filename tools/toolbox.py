import cv2
import numpy as np

def readImage(path):
    return cv2.imread(path)

def averageColor(img):
    avg = np.average(img, axis = 0)
    return np.average(avg, axis = 0)

def extractParams(paramList, img):
    pass

