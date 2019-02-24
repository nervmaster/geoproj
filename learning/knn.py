from learning.machineLearning import MachineLearning
from datasets import dataset
from sklearn import neighbors
from random import shuffle
import numpy as np
import functools



class Knn(MachineLearning):
    def __init__(self, n):
        self._n_neighbors = n

    def crossValidate(self, dataset, n_slices):
        cont = 0
        bingo = 0
        data = dataset.getData()
        shuffle(data)

        units_slice = len(data) // n_slices

        for i in range(n_slices):
            up = (i+1)*units_slice
            down = i*units_slice
            print(down, up)
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

                if(correct == guessed):
                    bingo += 1
        print(cont,bingo)

    def _inst(self):
        return neighbors.KNeighborsClassifier(n_neighbors=self._n_neighbors)