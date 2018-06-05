from .dataset import Dataset

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

    def __parseFolder(self, folder, label):
        for i in range(1, 10):
            # use toolbox to read the file here
            self._data.append([i])
            self._label.append(label)


    def parseFiles(self):
        base_path = '../MIfile/MI'

        for i in range(1, 84):
            folder = base_path + str(i) + '/'
            label = self.__getLabelFromFolder(i)
            self.__parseFolder(folder, label)



