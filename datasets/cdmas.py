from .dataset import Dataset
import tools.toolbox as tb
from multiprocessing import Pool, cpu_count, Manager
from .units.mineralunit import MineralUnit
from tools.param_enum import LightType


def parseFolder(folder, unitList, label, color_format):
    for i in range(1, 20):
        unit = MineralUnit(label, color_format)
        unit.readImage(folder + 'p' + str(i) + '.png', LightType.PPL)
        unit.readImage(folder + 'x' + str(i) + '.png', LightType.XPL)
        unitList.append(unit)

class CDMas(Dataset):
    def __init__(self, color = None):
        Dataset.__init__(self, color_format=color)
        
    def __getLabelFromFolder(self, folder):
        if folder <= 5:
            return 'Anthophilite'
        if folder <= 11:
            return 'Augite'
        if folder <= 17:
            return 'Olivine'
        if folder <= 31:
            return 'Biotite'
        if folder <= 34:
            return 'Muscovite'
        if folder <= 39:
            return 'Calcite'
        if folder <= 44:
            return 'Brown hornblende'
        if folder <= 54:
            return 'Green hornblende'
        if folder <= 57:
            return 'Chlorite'
        if folder <= 59:
            return 'Opx'
        if folder <= 60:
            return 'Apatite'
        if folder <= 67:
            return 'Quartz'
        if folder <= 71:
            return 'PLagioclase'
        if folder <= 76:
            return 'Orthoclase'
        if folder <= 77:
            return 'Microcline'
        if folder <= 79:
            return 'Sanidine'
        if folder <= 81:
            return 'lucite'
        else:
            return 'Garnet'

    def parseFiles(self):
        with Manager() as manager:
            base_path = './MIfile/MI'
            threads = []
            pool = Pool()
            units = manager.list()
            for i in range(1, 84):
                folder = base_path + str(i) + '/'
                label = self.__getLabelFromFolder(i)
                threads.append(pool.apply_async(parseFolder, (folder, units, label, self._colorFormat)))
            pool.close()
            [t.get() for t in threads]
            self._units = [x for x in units]   