#!/usr/bin/env python
# -*- coding: utf-8 -*-
from toolbox import *
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import normalize
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier

all_set = read_param_from_csv_file()
labels = read_labels_from_csv_file()

#matrix de confusao
verd_list = list()
pred_list = list()

all_set = np.asarray(all_set)
counter = 0

correct = 0
incorrect = 0

naive_c = 0
naive_err = 0

for i in range(0,100):

	t_set = all_set[:]
	t_labels = labels[:]

	#Criar o traning set
	sets = make_training_sets(t_set, t_labels)

	knn = KNeighborsClassifier(n_neighbors=1)
	knn.fit(sets['training'], sets['labels'])

	clf = GaussianNB()
	clf.fit(sets['training'], sets['labels'])

	#verificar com o algoritmo de Vizinho Mais Proximo
	for j in range(0, len(sets['new_entry_set'])):
		verd = sets['new_entry_labels'][j]
		counter += 1

		# kNN CLASSIFIER
		pred = knn.predict(sets['new_entry_set'][j].reshape(1,-1))
		if verd == pred:
			correct += 1

		# NAIVE BAYES CLASSIFIER
		pred = clf.predict(sets['new_entry_set'][j].reshape(1,-1))
		if verd == pred:
			naive_c += 1





#Matrix de confusao
#print confusion_matrix(verd_list, pred_list, labels = list(set(make_aligholi_training_label())))
print 'arg dim', len(all_set[0])
print 'kNN', float(float(correct)/float(counter))*100.0, '%'
print 'naive: ', float(float(naive_c)/float(counter))*100.0, '%'
