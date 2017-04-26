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


def multi_run_wrapper(args):
    return train(*args)


def makecsv(argv):
    if len(argv) < 1:
        print 'missing <filename>'
        exit(1)
    filename = argv[0]
    arq, writer = make_csv(filename)
    iterate_alligholli_dataset(arq, writer, param=param)
    arq.close()


def cross_validation(argv):
    if len(argv) < 2:
        print 'missing csv data file to read from and number of workers'
        exit(1)
    filename = argv[0]
    nworkers = int(argv[1]) if int(argv[1]) > 0 else 1

    with open('results.csv', 'w') as csvfile:
        fieldnames = ['param', 'random', 'kNN', 'dtree']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        m = Manager()
        linhas = m.Queue()

        pool = Pool(nworkers)
        args = list()

        for i in range(1, len(singles) + 1):
            for sub in itertools.combinations(singles, i):
                args.append((linhas, sub, filename))
            break
            

        mpr = [pool.apply_async(train, arg) for arg in args]
        pool.close()
        
        while True:
            try:
                [r.get(timeout = 1) for r in mpr]
                break
            except:
                writer.writerow(linhas.get())
        

        
        print 'escrevendo'
        while not linhas.empty():
            writer.writerow(linhas.get())


def maketraincsv(argv):
    if len(argv) < 1:
        print 'missing filepath to save to'
        exit(1)
    filename = argv[0]
    arq, writer = make_csv(filename)
    iterate_gathered_data(arq, writer, param)
    arq.close()


def debug(datafile, testfile):
    # will change this whole function
    with open('evaluate_results.csv', 'w') as csvfile:
        fieldnames = ['param', 'kNN', 'dtree']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        m = Manager()
        linhas = m.Queue()

        for i in range(1, len(singles) + 1):
            for sub in itertools.combinations(singles, i):
                evaluate(linhas, sub, datafile, testfile)

        print 'escrevendo'
        while not linhas.empty():
            writer.writerow(linhas.get())


def main(argv):
    if len(argv) < 1:
        print 'Missing function call'
        exit(1)
    if argv[1] == 'makecsv':
        print 'creating csv'
        makecsv(argv[2:])
    elif argv[1] == 'train':
        print 'training data'
        cross_validation(argv[2:])
    elif argv[1] == 'debug':
        print 'debug'
        debug(argv[2:])
    elif argv[1] == 'maketraincsv':
        print 'make csv train'
        maketraincsv(argv[2:])
    else:
        'invalid arg'


if __name__ == '__main__':
    main(sys.argv)
