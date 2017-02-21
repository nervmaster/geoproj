#!/usr/bin/env python
# -*- coding: utf-8 -*-
from toolbox import *
from sklearn import neural_network,linear_model,svm,naive_bayes,neighbors, metrics, tree
import numpy as np, scipy.stats as st
import csv
import itertools
from ann import build_ann
from training import train
from multiprocessing import Process, Lock

param = ['xpl', 'pleoc', 'biref', 'ppl', 'tex']
#all_set, labels = iterate_alligholli_dataset(param = param, normalize = False, pairs = 2)
#data_conf = make_confidence_interval(all_set, labels)
#make_csv(all_set, labels)
#exit(1)

with open('results.csv', 'w') as csvfile:
	fieldnames = ['param','random','kNN','naive','linear','svm','sgdc','dtree']
	writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
	writer.writeheader()

	# Code block for setting ANN
	#r = read_from_csv('data.csv', param)
	#build_ann(r['entries'], r['labels'])
	#print 'built'
	#exit(1)

	lock = Lock()
	for L in range(0, len(param) + 1):
		print L
		if L < 1:
			continue
		pp = list()
		for subset in itertools.combinations(param, L):
			p = Process(target = train, args = (subset, writer, lock))
			p.start()
			pp.append(p)

		for p in pp:
			p.join()
		csvfile.flush()
		break
