from sklearn import tree
from learning.machineLearning import MachineLearning

class DTree(MachineLearning):
    def __init__(self):
        super().__init__('Decicion Tree Classifier')

    def _inst(self):
        return tree.DecisionTreeClassifier()