from abc import ABC, abstractmethod
from random import shuffle
import numpy as np
from sklearn.model_selection import cross_val_score, KFold

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

        impl = self._inst()
        X = [item[1] for item in data]
        y = [item[0] for item in data]
        scores = cross_val_score(impl, X, y, cv=KFold(10, shuffle=True, random_state=0))


        # units_slice = len(data) // n_slices

        # for i in range(n_slices):
        #     up = (i+1)*units_slice
        #     down = i*units_slice
        #     labels = np.array(data[0])
        #     info = np.array(data[1])
        #     if i < n_slices-1:
        #         X = [item[1] for item in (data[:down] + data[up:])]
        #         y = [item[0] for item in (data[:down] + data[up:])]
        #         to_be_guessed = data[down:up]
        #     else:
        #         X = data[:down,1]
        #         y = data[:down,0]
        #         to_be_guessed = data[down:]
            
        #     impl = self._inst()
        #     impl.fit(X,y)
            
        #     for i in to_be_guessed:
        #         cont += 1
        #         correct = i[0]
        #         print(i[1].reshape(-1,1))
        #         guessed = impl.predict(i[1].reshape(-1,1))

        #         if correct in guessed:
        #             bingo += 1
        print(self._name,'accuracy:',scores.mean()*100, '% +/-', scores.std() * 200)