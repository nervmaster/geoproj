#!/usr/bin/env python
# -*- coding: utf-8 -*-
from toolbox import *
from sklearn import neural_network,linear_model,svm,naive_bayes,neighbors, metrics, tree
import numpy as np, scipy.stats as st
import csv
import itertools
from ann import build_ann

param = ['xpl', 'pleoc', 'biref', 'ppl', 'tex', 'ext', 'opa']
#all_set = iterate_alligholli_dataset(param = param, normalize = False)
#labels = make_aligholi_training_label(numbers = True)
#data_conf = make_confidence_interval(all_set, labels)
#make_csv(all_set, labels)


with open('results.csv', 'w') as csvfile:
	fieldnames = ['param','random','kNN','naive','linear','svm','sgdc','dtree','ann']
	writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
	writer.writeheader()
	for L in range(0, len(param) + 1):
		for subset in itertools.combinations(param, L):
			if(len(subset) < 1):
				continue
			linha = dict()
			linha['param'] = subset
			r = read_from_csv('data.csv', subset)

			#matrix de confusao
			verd_list = list()
			pred_list = list()

			counter = 0

			rnd_c = 0
			knn_c = 0
			naive_c = 0
			ln_c = 0
			svm_c = 0
			sgdc_c = 0
			dtree_c = 0
			ann_c = 0

			#build ANN
			for i in range(0,100):


				t_set = r['entries'][:]
				t_labels = r['labels'][:]

				#Criar o traning set
				#targets = [61,62,25,75,]
				#sets = select_training_sets(t_set, t_labels, targets)
				sets = make_training_sets(t_set, t_labels)
				X = sets['training']
				y = sets['labels']

				knn = neighbors.KNeighborsClassifier(n_neighbors=1)
				knn.fit(X,y)

				clf = naive_bayes.GaussianNB()
				clf.fit(X,y)

				ln = linear_model.LassoLars()
				ln.fit(X,y)

				svm_clf = svm.LinearSVC()
				svm_clf.fit(X,y)

				sgdc = linear_model.SGDClassifier(loss = 'hinge')
				sgdc.fit(X,y)

				dtree = tree.DecisionTreeClassifier()
				dtree.fit(X,y)

				ann = neural_network.MLPClassifier(max_iter = 200)
				ann.fit(X,y)

				#build_ann(r['entries'],r['labels'])
				#exit(1)
				for j in range(0, len(sets['new_entry_set'])):
					verd = sets['new_entry_labels'][j]
					counter += 1

					# RANDOM CLASSIFIER
					pred = r['labels'][randint(0,len(r['labels'])-1)]
					if verd == pred:
						rnd_c += 1

					# kNN CLASSIFIER
					pred = knn.predict(sets['new_entry_set'][j].reshape(1,-1))
					if verd == pred:
						knn_c += 1

					# NAIVE BAYES CLASSIFIER
					pred = clf.predict(sets['new_entry_set'][j].reshape(1,-1))
					if verd == pred:
						naive_c += 1

					# LINEAR CLASSIFIER
					pred = ln.predict(sets['new_entry_set'][j].reshape(1,-1))
					pred = min(r['labels'], key=lambda x:abs(x-pred))
					if verd == pred:
						ln_c += 1

					# SVM CLASSIFIER
					pred = svm_clf.predict(sets['new_entry_set'][j].reshape(1,-1))
					if verd == pred:
						svm_c += 1

					# SGD CLASSIFIER
					pred = sgdc.predict(sets['new_entry_set'][j].reshape(1,-1))
					if verd == pred:
						sgdc_c += 1

					# DECISION TREE CLASSIFIER
					pred = dtree.predict(sets['new_entry_set'][j].reshape(1,-1))
					if verd == pred:
						dtree_c += 1

					# Neural Network CLASSIFIER
					pred = ann.predict(sets['new_entry_set'][j].reshape(1,-1))
					if verd == pred:
						ann_c += 1

			#Matrix de confusao
			#print metrics.confusion_matrix(verd_list, pred_list, labels = list(set(make_aligholi_training_label())))
			#print 'arg dim', len(r['entries'][0])
			linha['random'] = float(float(rnd_c)/float(counter))*100.0
			#print 'random', float(float(rnd_c)/float(counter))*100.0, '%'
			linha['kNN'] = float(float(knn_c)/float(counter))*100.0
			#print 'kNN', float(float(knn_c)/float(counter))*100.0, '%'
			linha['naive'] = float(float(naive_c)/float(counter))*100.0
			#print 'naive:', float(float(naive_c)/float(counter))*100.0, '%'
			linha['linear'] = float(float(ln_c)/float(counter))*100.0
			#print 'linear:', float(float(ln_c)/float(counter))*100.0, '%'
			linha['svm'] = float(float(svm_c)/float(counter))*100.0
			#print 'svm:', float(float(svm_c)/float(counter))*100.0, '%'
			linha['sgdc'] = float(float(sgdc_c)/float(counter))*100.0
			#print 'sgdc:', float(float(sgdc_c)/float(counter))*100.0, '%'
			linha['dtree'] = float(float(dtree_c)/float(counter))*100.0
			#print 'dtree:', float(float(dtree_c)/float(counter))*100.0, '%'
			linha['ann'] = float(float(ann_c)/float(counter))*100.0
			#print 'ann:', float(float(ann_c)/float(counter))*100.0, '%'
			#print '\n\n\n\n'
			writer.writerow(linha)
