#!/usr/bin/env python
# -*- coding: utf-8 -*-
from toolbox import *
from sklearn import neural_network,linear_model,svm,naive_bayes,neighbors, metrics, tree
import numpy as np, scipy.stats as st
import csv


def make_csv(data, labels):
	with open('data.csv', 'w') as csvfile:
		writer = csv.writer(csvfile, delimiter = ';')
		header = list()
		header.append('label')
		header.append('xpl_l', 'xpl_a', 'xpl_b')
		header.append('ppl_l', 'ppl_a', 'ppl_b')
		header.append('biref_l', 'biref_a', 'biref_b')
		header.append('pleoc_l', 'pleoc_a', 'pleoc_b')
		header.append('ext')
		header.append('tex_1', 'tex_2', 'tex_3')
		header.append('opa_1')
		writer.writerow(header)
		for i in range(0,len(labels)-1):
			writer.writerow(np.append(labels[i], data[i]))



all_set = iterate_alligholli_dataset(param = ['xpl', 'pleoc', 'biref', 'ppl', 'tex', 'ext', 'opa'], normalize = False)
labels = make_aligholi_training_label(numbers = False)

make_csv(all_set, labels)
exit(1)

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

for i in range(0,10):

	print 'iteração', i+1

	t_set = all_set[:]
	t_labels = labels[:]

	#Criar o traning set
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

	ann = neural_network.MLPClassifier(max_iter = 400)
	ann.fit(X,y)

	#verificar com o algoritmo de Vizinho Mais Proximo
	for j in range(0, len(sets['new_entry_set'])):
		verd = sets['new_entry_labels'][j]
		counter += 1

		# RANDOM CLASSIFIER
		pred = labels[randint(0,len(labels)-1)]
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
		pred = min(labels, key=lambda x:abs(x-pred))
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
print 'arg dim', len(all_set[0])
print 'random', float(float(rnd_c)/float(counter))*100.0, '%'
print 'kNN', float(float(knn_c)/float(counter))*100.0, '%'
print 'naive:', float(float(naive_c)/float(counter))*100.0, '%'
print 'linear:', float(float(ln_c)/float(counter))*100.0, '%'
print 'svm:', float(float(svm_c)/float(counter))*100.0, '%'
print 'sgdc:', float(float(sgdc_c)/float(counter))*100.0, '%'
print 'dtree:', float(float(dtree_c)/float(counter))*100.0, '%'
print 'ann:', float(float(ann_c)/float(counter))*100.0, '%'
