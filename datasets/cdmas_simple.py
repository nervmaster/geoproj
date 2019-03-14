from .dataset import Dataset
from multiprocessing import Pool, cpu_count, Manager
from .units.simpleunit import SimpleUnit
from tools.enumerators import LightType


def parseFolder(folder, unitList, label, color_format, light_type):
    for i in range(1, 20):
        unit = SimpleUnit(label, color_format)
        if(light_type == LightType.PPL):
            unit.readImage(folder + 'p' + str(i) + '.png')
        else:
            unit.readImage(folder + 'x' + str(i) + '.png')
        unitList.append(unit)

class CDMasSimple(Dataset):
    def __init__(self, color = None, light_type = LightType.XPL):
        print(color)
        Dataset.__init__(self, color_format=color)
        self._light_type = light_type
        
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
                threads.append(pool.apply_async(parseFolder, (folder, units, label, self._colorFormat, self._light_type)))
            pool.close()
            [t.get() for t in threads]
            self._units = [x for x in units]   