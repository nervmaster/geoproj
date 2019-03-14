from datasets.units.unit import Unit
import cv2
import numpy as np
from tools.enumerators import Param, LightType, ColorFormat

class SimpleUnit(Unit):

    def __init__(self,label, color):
        super().__init__(label = label, color_format=color)
        self._image = None

    def readImage(self, path):
        image = cv2.imread(path)
        image = np.float32(image)
        image = image / 255.0
        if(self._color_format == ColorFormat.LAB):
            image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        elif(self._color_format == ColorFormat.HSV):
            image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        if(self._color_format == ColorFormat.RGB):
            self._image = image
        else:
            self._image = image[:,:,1:3]

    def extract(self, paramName):
        if paramName == Param.AVERAGE:
            self.__calculate(np.average)
        elif paramName == Param.MEDIAN:
            self.__calculate(np.median)
        elif paramName == Param.MEAN:
            self.__calculate(np.mean)

    def __calculate(self, func):
        data = self._data
        avg = Param.AVERAGE
        data[avg] = []
        data[avg].append(func(func(self._image, axis=0), axis=0))
        self._data = data