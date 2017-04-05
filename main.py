#!/usr/bin/env python
# -*- coding: utf-8 -*-
from toolbox import *
from sklearn import neural_network, linear_model, svm, naive_bayes, neighbors, metrics, tree
import numpy as np
import scipy.stats as st
import csv
import itertools
import sys
from training import train
from multiprocessing import Process, Lock, Queue, Pool, Manager
from functools import partial

param = ['xpl', 'pleoc', 'biref', 'ppl', 'tex', 'opa']
singles = ['xpl', 'ppl', 'tex', 'opa']


def makecsv():
    arq, writer = make_csv('newdata.csv')
    iterate_alligholli_dataset(arq, writer, param = param, normalize = False)
    arq.close()
    return

    all_set, labels = iterate_alligholli_dataset(param=param, normalize=False)
    # data_conf = make_confidence_interval(all_set, labels)
    make_csv(all_set, labels)


def cross_validation():
    with open('results.csv', 'w') as csvfile:
        fieldnames = ['param', 'random', 'kNN', 'dtree']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        m = Manager()
        linhas = m.Queue()

        for i in range(1, len(singles)+1):
            for sub in itertools.combinations(singles, i):
                train(linhas, sub)

        print 'escrevendo'
        while not linhas.empty():
            writer.writerow(linhas.get())


def debug():
    folder_names = ['Quartzo', 'ortoclásio', 'microclínio']
    crop_geo_set(folder_names)
    r = read_from_csv('./data.csv', param)

    knn = neighbors.KNeighborsClassifier(n_neighbors=1)
    knn.fit(r['entries'], r['labels'])

    dtree = tree.DecisionTreeClassifier()
    dtree.fit(r['entries'], r['labels'])

    gdata, glabels = iterate_gathered_data(param)

    counter = 0
    knn_c = 0

    for i in range(0, len(gdata)):
        verd = glabels[i]
        counter += 0

        print 'target', verd
        # knn
        print 'knn', knn.predict(gdata[i].reshape(1, -1))

        # dtree
        print 'dtree', dtree.predict(gdata[i].reshape(1, -1))


def main(argv):
    if len(argv) < 2:
        print 'Argumentos insuficientes'
        exit(1)
    if argv[1] == 'makecsv':
        print 'creating csv'
        makecsv()
    elif argv[1] == 'train':
        print 'training data'
        cross_validation()
    elif argv[1] == 'debug':
        print 'debug'
        debug()

    else:
        'invalid arg'


if __name__ == '__main__':
    main(sys.argv)
