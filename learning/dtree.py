from sklearn import tree
from learning.machineLearning import MachineLearning

class DTree(MachineLearning):
    def __init__(self):
        super().__init__('Decision Tree Classifier')

    def _inst(self):
        return tree.DecisionTreeClassifier()