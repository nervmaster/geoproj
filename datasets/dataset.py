from abc import ABC, abstractmethod

class Dataset(ABC):
    self.__data = []
    self.__label = []

    def __init__(self, csvFileName = False):
        # Checks if has a csvFileName
        # if not parse files
        # if yes load the csv
        pass


    def getData(self):
        return self.__data
        

    def getDataWithLabel(self):
        return self.__data, self.__label

    @abstractmethod
    def parseFiles(self):
        pass

    def writeCsv(self, csvFileName):
        pass
    
    def readCsv(self, csvFileName):
        pass