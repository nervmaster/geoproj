from abc import ABC, abstractmethod
from tools.param_enum import Param
import tools.toolbox as tb
import csv

def extractGeoParams(paramNames, xplList, pplList, pairType='all'):
    for xpl in xplList:
        for ppl in pplList:
            if Param.AVERAGE in paramNames:
                data.append()
                


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

        with open(csvFileName,'w') as arq:
            writer = csv.writer(arq, delimiter=';')
            header = [labelColumnName]
            [header.append(x) for x in self._paramNames]
            writer.writerow(header)
            for label, data in zip(self._label, self._data):
                row = []
                row.append(label)
                for elem in data:
                    row.append(elem.tolist())
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
