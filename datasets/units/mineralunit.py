from datasets.units.unit import Unit
import cv2
import numpy as np
from tools.param_enum import Param

class MineralUnit(Unit):

    def __init__(self,label):
        super().__init__(label = label)
        self._xpl = None
        self._ppl = None

    def readXpl(self, path):
        self._xpl = cv2.imread(path)

    def readPpl(self, path):
        self._ppl = cv2.imread(path)

    def extract(self, paramName):
        if paramName == Param.AVERAGE:
            self.__calculateAverage()

    def __calculateAverage(self):
        data = self._data
        avg = Param.AVERAGE
        data[avg] = []
        data[avg].append(np.average(np.average(self._ppl)))
        data[avg].append(np.average(np.average(self._xpl)))
        self._data = data
