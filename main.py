from datasets.cdmas import CDMas
from datasets.cdgeo import CDGeo
from datasets.cdmas_simple import CDMasSimple
from learning.knn import Knn
from learning.dtree import DTree
from learning.random import RandomClassifier
from tools.enumerators import ColorFormat, LightType, Param

def runAll(ds):
    for i in range(1,10,2):
        knn = Knn(i)
        knn.crossValidate(ds,10)
    dtree = DTree()
    dtree.crossValidate(ds,10)
    random = RandomClassifier()
    random.crossValidate(ds,10)    

print("Hello World!")
ds = CDMasSimple(color = ColorFormat.HSV, light_type = LightType.XPL)
ds.parseFiles()
ds.extractInfo()
ds.plot()
print('------------------ RGB')
ds = CDMas(ColorFormat.RGB)
ds.parseFiles()
ds.extractInfo()
ds.plot()
runAll(ds)
print('------------------ LAB')
ds = CDMas(ColorFormat.LAB)
ds.parseFiles()
ds.extractInfo()
ds.plot()
runAll(ds)
print('------------------ HSV')
ds = CDMas(ColorFormat.HSV)
ds.parseFiles()
ds.extractInfo()
ds.plot()
runAll(ds)