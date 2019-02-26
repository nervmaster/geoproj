from abc import ABC, abstractmethod
from tools.param_enum import Param
import tools.toolbox as tb
import csv
from multiprocessing import Pool, cpu_count, Manager
from datasets.units.unit import Unit
import itertools

class Dataset(ABC):
    def __init__(self, csvFileName = None, paramNames = None):
        self._units = []
        self._paramNames = paramNames
        self._csvFileName = csvFileName

    def getData(self):
        all_data = []
        for unit in self._units:
            single_data = []
            unit_data = unit.getData()
            unit_label = unit.getLabel()
            if(Param.AVERAGE in unit_data):
                single_data.append(unit_data[Param.AVERAGE])
            flatten_data = [item for sublist in single_data for item in sublist]
            all_data.append((unit_label, flatten_data))
        return all_data
         


    @abstractmethod
    def parseFiles(self):
        pass

    def extractInfo(self):
        for unit in self._units:
            unit.extract(Param.AVERAGE)

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
