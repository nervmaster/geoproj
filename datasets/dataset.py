from abc import ABC, abstractmethod
import csv

class Dataset(ABC):
    def __init__(self, paramNames, csvFileName = None):
        # ParamNames must be passed as arg for the desired parameters
        # Checks if has a csvFileName
        # if not parse files
        # if yes load the csv
        self.__data = [] 
        self.__label = [] 
        self.__paramNames = paramNames 
        self.__csvFileName = csvFileName


    def getData(self):
        return self.__data, self.__label

    @abstractmethod
    def parseFiles(self):
        pass

    def __createCsvWriter(self, csvFileName, headerList):
        if csvFileName is None:
            csvFileName = self.__csvFileName
        if headerList is None:
            headerList = self.__paramNames
        
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
            csvFileName = self.__csvFileName
        if headerList is None:
            headerList = self.__paramNames
        
        with csv.writer(csvFileName, delimiter=';') as writer:
            writer.writerow([labelColumnName].extend(self.__paramNames))
            for label, data in zip(self.__label, self.__data):
                row = []
                row.append(label)
                for elem in data:
                    row.append(elem)
                writer.writerow(row)
        
    
    def readCsv(self, labelColumnName = 'label', csvFileName = None, headerList = None):
        if csvFileName is None:
            csvFileName = self.__csvFileName
        if headerList is None:
            headerList = self.__paramNames

        with open(csvFileName, 'r') as csvFile:
            reader = csv.DictReader(csvFile, delimiter=';')
            for row in reader:
                newData = list()
                for columnName, value in row.items() :
                    if columnName == labelColumnName:
                        self.__label.append(value)
                    else:
                        newData.append(value)
            self.__data.append(newData)
