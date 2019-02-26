from abc import ABC, abstractmethod
from random import shuffle
import numpy as np

class MachineLearning(ABC):
    def __init__(self,name):
        self._name = name
    
    @abstractmethod
    def _inst(self):
        pass

    def crossValidate(self, dataset, n_slices):
        cont = 0
        bingo = 0
        data = dataset.getData()
        shuffle(data)

        units_slice = len(data) // n_slices

        for i in range(n_slices):
            up = (i+1)*units_slice
            down = i*units_slice
            labels = np.array(data[0])
            info = np.array(data[1])
            if i < n_slices-1:
                X = [item[1][0] for item in (data[:down] + data[up:])]
                y = [item[0] for item in (data[:down] + data[up:])]
                to_be_guessed = data[down:up]
            else:
                X = [item[1][0] for item in data[:down]]
                y = [item[0] for item in data[:down]]
                to_be_guessed = data[down:]
            
            impl = self._inst()
            impl.fit(X,y)
            
            for i in to_be_guessed:
                cont += 1
                correct = i[0]
                guessed = impl.predict(i[1])

                if correct in guessed:
                    bingo += 1
        print(self._name,bingo/cont*100,'%')