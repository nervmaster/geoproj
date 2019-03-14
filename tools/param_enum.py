from enum import Enum
class Param(Enum):
    # Parameters
    AVERAGE = 'avg'
    MEDIAN = 'median'
    MEAN = 'mean'
    ALL = 'all'

class ColorFormat(Enum):
    LAB = 'lab'
    RGB = 'rgb'
    HSV = 'hsv'

class LightType(Enum):
    PPL = 'ppl'
    XPL = 'xpl'