from abc import ABC, abstractmethod
from tools.param_enum import Param
from multiprocessing import Pool, cpu_count, Manager


class Unit(ABC):
    def __init__(self, label = None, color_format = None):
        self._label = label
        self._data = dict()
        self._color_format = color_format
    
    def getData(self):
        return self._data

    def getLabel(self):
        return self._label
    
    @abstractmethod
    def extract(self, paramName):
        pass
    