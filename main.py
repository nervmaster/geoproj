#!/usr/bin/env python
# -*- coding: utf-8 -*-
from toolbox import *
from sklearn import neural_network,linear_model,svm,naive_bayes,neighbors, metrics, tree
import numpy as np, scipy.stats as st
import csv
import itertools
from ann import build_ann
from training import train
from multiprocessing import Process, Lock, Queue, Pool, Manager
from functools import partial

param = ['xpl', 'pleoc', 'biref', 'ppl', 'tex', 'opa']
# all_set, labels = iterate_alligholli_dataset(param = param, normalize = False, pairs = 1)
# # data_conf = make_confidence_interval(all_set, labels)
# make_csv(all_set, labels)
# exit(1)

with open('results.csv', 'w') as csvfile:
	fieldnames = ['param','random','kNN','naive','linear','svm','sgdc','dtree','ann']
	writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
	writer.writeheader()

	# Code block for setting ANN
	#r = read_from_csv('data.csv', param)
	#build_ann(r['entries'], r['labels'])
	#print 'built'
	#exit(1)

	lock = Lock()
	m = Manager()
	linhas = m.Queue()
	args = list()
	workers = Pool(5)
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


		# 	p = Process(target = train, args = (subset, linhas, lock))
		# 	p.start()
		# 	pp.append(p)
		#
		# for p in pp:
		# 	p.join()
