#!/usr/bin/env python
# -*- coding: utf-8 -*-
from toolbox import *
from sklearn import neural_network,linear_model,svm,naive_bayes,neighbors, metrics, tree
import numpy as np, scipy.stats as st
import csv
import itertools
import sys
from training import train
from multiprocessing import Process, Lock, Queue, Pool, Manager
from functools import partial

param = ['xpl', 'pleoc', 'biref', 'ppl', 'tex', 'opa']

def makecsv():
	all_set, labels = iterate_alligholli_dataset(param = param, normalize = False, pairs = 2)
	data_conf = make_confidence_interval(all_set, labels)
	make_csv(all_set, labels)

def train():
	with open('results.csv', 'w') as csvfile:
		fieldnames = ['param','random','kNN','naive','linear','svm','sgdc','dtree','ann']
		writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
		writer.writeheader()


		lock = Lock()
		m = Manager()
		linhas = m.Queue()
		args = list()
		workers = Pool(4)
		for L in range(0, len(param) + 1):
			if L < 1:
				continue
			pp = list()
			for subset in itertools.combinations(param, L):
				args.append(subset)

			func = partial(train, linhas)
			workers.map(func, args)
			workers.close()
			workers.join()

		while not linhas.empty():
			writer.writerow(linhas.get())


def main(argv):
	if len(argv) < 2:
		print 'Argumentos insuficientes'
		exit(1)
	if argv[1] == 'makecsv':
		print 'creating csv'
		makecsv()
	elif argv[1] == 'train':
		print 'training data	'
		train()

	else:
		'invalid arg'


if __name__ == '__main__':
	main(sys.argv)
