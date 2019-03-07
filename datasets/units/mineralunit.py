from datasets.units.unit import Unit
import cv2
import numpy as np
from tools.param_enum import Param, LightType, ColorFormat

class MineralUnit(Unit):

    def __init__(self,label, color_format):
        super().__init__(label = label)
        self._xpl = None
        self._ppl = None

    def readImage(self, path, light_type):
        image = cv2.imread(path)
        if(self._color_format != ColorFormat.RGB):
            image = np.float32(image)
            image = image / 255.0
            if(self._color_format == ColorFormat.LAB):
                image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
            elif(self._color_format == ColorFormat.HSV):
                image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV_FULL)
        if(light_type == LightType.XPL):
            self._xpl = image
        else:
            self._ppl = image

    def extract(self, paramName):
        if paramName == Param.AVERAGE:
            self.__calculateAverage()
        elif paramName == Param.OPACITY:
            self.__calculateAverage()

    def __hasLightChannel(self):
        if self._color_format not in [ColorFormat.HSV, ColorFormat.LAB]:
            raise Exception('Color Format:' + self._color_format + 'does not have a lightning channel')
        return True
        
    def __calculateAverage(self):
        data = self._data
        avg = Param.AVERAGE
        data[avg] = []
        data[avg].append(np.average(np.average(self._ppl, axis=0), axis=0))
        data[avg].append(np.average(np.average(self._xpl, axis=0), axis=0))
        self._data = data
