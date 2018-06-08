from .dataset import Dataset
import tools.toolbox as tb
from multiprocessing import Pool, cpu_count, Manager
import os

def parseFolder(path, label, param, dataList, labelList):
    ppl = list()
    xpl = list()

    photos_folders = os.listdir(path)
    folderList = []
    for folder in photos_folders:
        if '.JPG' in folder or '.png' in folder:
            continue
        lista = xpl
        folderList.append(folder)

        if 'N' in folder or 'np' in folder:
            lista = ppl
        
        photosPath = path + folder + '/'
        photos = os.listdir(photosPath)
        for photo in photos:
            img = tb.readImage(photosPath + photo)
            lista.append(img)
    
    if(len(xpl) == 0 or len(ppl) == 0):
        print(path ,folderList)
    for x, y in ppl:
        data = []
        data.append(tb.extractParams(param, x))
        data.append(tb.extractParams(param, y))
        dataList.append(data)
        labelList.append(label)
    



class CDGeo(Dataset):
    def __init__(self, paramNames = None, csvFileName = None):
        super().__init__(paramNames = paramNames, csvFileName= csvFileName)

    def __get_mineral_name_number(self, str):
        if "Biotita" in str:
            return 3
        elif "Quartzo" in str:
            return 11
        elif "Ortoclasio" in str:
            return 13
        elif "Microclínio" in str:
            return 14
        elif "Plagiocl" in str:
            return 12
        elif "Mica" in str:
            return 14

    def __isImage(self, name):
        return '.JPG' in name or '.png' in name

    def parseFiles(self):
        with Manager() as manager:
            labelList = manager.list()
            dataList = manager.list()
            threads = []
            base_path = './Banco de dados Final/'
            root = os.listdir(base_path)
            pool = Pool()
            isImage = self.__isImage

            for mineral_thin_section in root:
                if isImage(mineral_thin_section):
                    continue

                thinSectionPath = base_path + mineral_thin_section + '/'
                minerals = os.listdir(thinSectionPath)

                for mineral in minerals:
                    if isImage(mineral):
                        continue

                    mineralPath = thinSectionPath + mineral + '/'
                    single_minerals = os.listdir(mineralPath)

                    for single_mineral in single_minerals:
                        if isImage(single_mineral):
                            continue
                        
                        singleMineralPath = mineralPath + single_mineral + '/'
                        finalFolders = os.listdir(singleMineralPath)

                        for finalFolder in finalFolders:
                            if isImage(finalFolder):
                                continue

                            finalPath = singleMineralPath + finalFolder + '/'
                            threads.append(pool.apply_async(parseFolder, (finalPath, mineral, self._paramNames, dataList, labelList)))
            pool.close()
            [t.wait() for t in threads]
