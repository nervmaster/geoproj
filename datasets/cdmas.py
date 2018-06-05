from .dataset import Dataset
import tools.toolbox as tb
from multiprocessing import Pool, cpu_count, Manager

def parseFolder(folder, label, listLabel, listData):
    for i in range(1, 20):
        x = tb.readImage(folder + 'x' + str(i) + '.png')
        y = tb.readImage(folder + 'p' + str(i) + '.png')
        data = []
        data.append(tb.extractParams('', x))
        data.append(tb.extractParams('', y))
        listLabel.append(label)
        listData.append(data)
            

class CDMas(Dataset):
    def __init__(self, paramNames = None, csvFileName = None):
        Dataset.__init__(self, paramNames = paramNames, csvFileName = csvFileName)
        
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
            labelList = manager.list()
            dataList = manager.list()

            base_path = './MIfile/MI'
            threads = []
            pool = Pool()
            for i in range(1, 84):
                folder = base_path + str(i) + '/'
                label = self.__getLabelFromFolder(i)
                threads.append(pool.apply_async(parseFolder, (folder, label, labelList, dataList)))
            pool.close()
            [t.get() for t in threads]
            for label, data in zip(labelList, dataList):
                self._label.append(label)
                self._data.append(data)
