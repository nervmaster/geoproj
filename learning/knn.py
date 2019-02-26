from learning.machineLearning import MachineLearning
from sklearn import neighbors
import numpy as np
import functools



class Knn(MachineLearning):
    def __init__(self, n):
        self._n_neighbors = n
        super().__init__('Nearest Neighbor Classifier n=' + str(n))

    def _inst(self):
        return neighbors.KNeighborsClassifier(n_neighbors=self._n_neighbors)