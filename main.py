#!/usr/bin/env python
# -*- coding: utf-8 -*-
from toolbox import *
from sklearn import neural_network, linear_model, svm, naive_bayes, neighbors, metrics, tree
import numpy as np
import scipy.stats as st
import csv
import itertools
import sys
from training import train, evaluate
from multiprocessing import Process, Lock, Queue, Pool, Manager
from functools import partial

param = ['xpl', 'pleoc', 'biref', 'ppl', 'tex', 'opa']
singles = ['xpl', 'ppl', 'tex', 'opa']
teste = ['xpl', 'ppl', 'tex', 'opa']


def makecsv(filename):
    arq, writer = make_csv(filename)
    iterate_alligholli_dataset(arq, writer, param = param, normalize = False)
    arq.close()


def cross_validation(filename):
    with open('results.csv', 'w') as csvfile:
        fieldnames = ['param', 'random', 'kNN', 'dtree']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        m = Manager()
        linhas = m.Queue()

        for i in range(1, len(singles)+1):
            for sub in itertools.combinations(singles, i):
                train(linhas, sub, filename)

        print 'escrevendo'
        while not linhas.empty():
            writer.writerow(linhas.get())

def maketraincsv(filename):
    arq, writer = make_csv(filename)
    iterate_gathered_data(arq, writer, param)
    arq.close()

def debug(datafile, testfile):
    with open('evaluate_results.csv', 'w') as csvfile:
        fieldnames = ['param', 'kNN', 'dtree']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        m = Manager()
        linhas = m.Queue()

        for i in range(1, len(singles)+1):
            for sub in itertools.combinations(singles, i):
                evaluate(linhas, sub, datafile, testfile)

        print 'escrevendo'
        while not linhas.empty():
            writer.writerow(linhas.get())
   
def main(argv):
    if len(argv) < 3:
        print 'Argumentos insuficientes'
        exit(1)
    if argv[1] == 'makecsv':
        print 'creating csv'
        makecsv(argv[2])
    elif argv[1] == 'train':
        print 'training data'
        cross_validation(argv[2])
    elif argv[1] == 'debug':
        print 'debug'
        debug(argv[2], argv[3])
    elif argv[1] == 'maketraincsv':
        print 'make csv train'
        maketraincsv(argv[2])

    else:
        'invalid arg'


if __name__ == '__main__':
    main(sys.argv)
