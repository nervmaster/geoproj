from datasets.cdmas import CDMas
from datasets.cdgeo import CDGeo

print("Hello World!")

ds = CDMas(csvFileName = "hello.csv", paramNames = ['avg_color_xpl', 'avg_color_ppl'])
ds.parseFiles()
ds.extractInfo()
print(ds.getData())

# ds = CDGeo(csvFileName = "cdgeo.csv", paramNames = ['avg_color_xpl', 'avg_color_ppl'])
# ds.parseFiles()
# ds.writeCsv()

# from toolbox import *
# from sklearn import neural_network, linear_model, svm, naive_bayes, neighbors, metrics, tree
# import numpy as np
# import scipy.stats as st
# import csv
# import itertools
# import sys
# from training import train, evaluate
# from multiprocessing import Process, Lock, Queue, Pool, Manager
# from functools import partial

# # Todos os parametros disponiveis para extração
# all_param = ['xpl', 'pleoc', 'biref', 'ppl', 'tex', 'opa']

# # Os parâmetros usados na última iteração
# singles = ['xpl', 'ppl', 'tex', 'opa']

# # Parâmetros para algum teste requisitado
# teste = ['xpl', 'ppl', 'tex', 'opa']

# # Função para criar um CSV com o CDMAS
# # Recebe como argumento O nome do arquivo csv para salvar
# # Chamada: makecsv("arquivo_de_saida.csv")
# def makecsv(argv):
#     if len(argv) < 1:
#         print 'missing <filename>'
#         exit(1)
#     filename = argv[0]
#     arq, writer = make_csv(filename)
#     iterate_alligholli_dataset(arq, writer, param=param)
#     arq.close()

# # Função para criar um CSV com CDGEO
# # Chamada: maketraincsv("arquivo_de_saida.csv")
# def maketraincsv(argv):
#     if len(argv) < 1:
#         print 'missing filepath to save to'
#         exit(1)
#     filename = argv[0]
#     arq, writer = make_csv(filename)
#     iterate_gathered_data(arq, writer, param)
#     arq.close()


# # Faz uma validação cruzada com o dataset CSV indicado como argumento
# # E salva os resultados em arquivo CSV
# # Chamada: cross_validation("arquivo_de_entrada.csv", "arquivo_de_saida.csv")
# def cross_validation(argv):
#     if len(argv) < 2:
#         print 'missing csv data file to read from and number of workers'
#         exit(1)
    
#     filename = argv[0]
    
#     # Caso queira que a validação cruzada seja em paralelo mudar para nworkes para o numero de cores desejados
#     nworkers = 1

#     with open('results.csv', 'w') as csvfile:
#         fieldnames = ['param', 'random', 'kNN', 'dtree']
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         writer.writeheader()
#         m = Manager()
#         linhas = m.Queue()

#         pool = Pool(nworkers)
#         args = list()

#         for i in range(1, len(singles) + 1):
#             for sub in itertools.combinations(singles, i):
#                 args.append((linhas, sub, filename))
#             break #Remova essa linha caso queira todas as combinações possiveis de parâmetros
            

#         mpr = [pool.apply_async(train, arg) for arg in args]
#         pool.close()
        
#         while True:
#             try:
#                 [r.get(timeout = 1) for r in mpr]
#                 break
#             except:
#                 writer.writerow(linhas.get())
        
#         print 'escrevendo'
#         while not linhas.empty():
#             writer.writerow(linhas.get())

# def main(argv):
#     if len(argv) < 1:
#         print 'Missing function call'
#         exit(1)
#     if argv[1] == 'makecsv':
#         print 'creating csv'
#         makecsv(argv[2:])
#     elif argv[1] == 'train':
#         print 'training data'
#         cross_validation(argv[2:])
#     elif argv[1] == 'maketraincsv':
#         print 'make csv train'
#         maketraincsv(argv[2:])
#     else:
#         'invalid arg'

# if __name__ == '__main__':
#     main(sys.argv)
