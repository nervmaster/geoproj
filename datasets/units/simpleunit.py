from datasets.units.unit import Unit
import cv2
import numpy as np
from tools.param_enum import Param, LightType, ColorFormat

class SimpleUnit(Unit):

    def __init__(self,label, color):
        super().__init__(label = label, color_format=color)
        self._image = None

    def readImage(self, path):
        image = cv2.imread(path)
        image = np.float32(image)
        image = image / 255.0
        self._image = image

    def extract(self, paramName):
        if paramName == Param.AVERAGE:
            self.__calculateAverage()
        elif paramName == Param.OPACITY:
            self.__calculateAverage()

    def __calculateAverage(self):
        data = self._data
        avg = Param.AVERAGE
        data[avg] = []
        data[avg].append(np.mean(np.mean(self._image, axis=0), axis=0))
        self._data = data