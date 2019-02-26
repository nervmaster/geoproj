from sklearn import tree
from learning.machineLearning import MachineLearning
import random

class RandomClassifier(MachineLearning):
    def __init__(self):
        self._y = None
        super().__init__('Random Classifier')

    def _inst(self):
        return self
    
    def fit(self,X,y):
        self._y = y
    
    def predict(self,a):
        return self._y[random.randint(0, len(self._y)-1)]