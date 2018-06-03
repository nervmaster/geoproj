from abc import ABC, abstractmethod

class Dataset(ABC):
    self.__data 
    self.__label 
    self.__paramNames 
    self.__csvFileName 

    def __init__(self, paramNames, csvFileName = None):
        # ParamNames must be passed as arg for the desired parameters
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
        writer.writerow(header)
        arq.flush()

        return arq, writer

    @abstractmethod
    def writeCsv(self, csvFileName = None, headerList = None):
        pass
        
    
    def readCsv(self, labelColumnName, csvFileName = None, headerList = None):
        try:
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
        except Exception as e:
            return e