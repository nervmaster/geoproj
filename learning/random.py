from sklearn import dummy
from learning.machineLearning import MachineLearning

class RandomClassifier(MachineLearning):
    def __init__(self, type = None):
        self._type = None
        super().__init__('Random Classifier')

    def _inst(self):
        if(self._type != None):
            return dummy.DummyClassifier(self._type)
        return dummy.DummyClassifier()