from abc import ABC, abstractmethod
import csv

class Dataset(ABC):
    def __init__(self, paramNames, csvFileName = None):
        self._data = []
        self._label = []
        self._paramNames = paramNames 
        self._csvFileName = csvFileName


    def getData(self):
        return self._data, self._label

    @abstractmethod
    def parseFiles(self):
        pass

    def __createCsvWriter(self, csvFileName, headerList):
        if csvFileName is None:
            csvFileName = self._csvFileName
        if headerList is None:
            headerList = self._paramNames
        
        try:
            arq = open(csvFileName, 'w')
        except Exception as e:
            return e
        
        writer = csv.writer(arq, delimiter=';')
        writer.writerow(headerList)
        arq.flush()

        return arq, writer

    def writeCsv(self, labelColumnName = 'label' ,csvFileName = None, headerList = None):
        if csvFileName is None:
            csvFileName = self._csvFileName
        if headerList is None:
            headerList = self._paramNames
        
        with csv.writer(csvFileName, delimiter=';') as writer:
            writer.writerow([labelColumnName].extend(self.__paramNames))
            for label, data in zip(self._label, self._data):
                row = []
                row.append(label)
                for elem in data:
                    row.append(elem)
                writer.writerow(row)
        
    
    def readCsv(self, labelColumnName = 'label', csvFileName = None, headerList = None):
        if csvFileName is None:
            csvFileName = self._csvFileName
        if headerList is None:
            headerList = self._paramNames

        with open(csvFileName, 'r') as csvFile:
            reader = csv.DictReader(csvFile, delimiter=';')
            for row in reader:
                newData = list()
                for columnName, value in row.items() :
                    if columnName == labelColumnName:
                        self._label.append(value)
                    else:
                        newData.append(value)
            self._data.append(newData)
