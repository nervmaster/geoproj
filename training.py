from toolbox import *
from sklearn import neural_network, linear_model, svm, naive_bayes, neighbors, metrics, tree
import numpy as np
import scipy.stats as st
import csv
import itertools
from random import shuffle

def evaluate(linhas, param_set, datafile, testfile):
    linha = dict()
    linha['param'] = param_set
    r = read_from_csv(datafile, param_set)

    #matrix de confusao
    verd_list = list()
    pred_list = list()

    counter = 0
    
    knn_c = 0
    dtree_c = 0

    X = r['entries']
    y = r['labels']

    knn = neighbors.KNeighborsClassifier(n_neighbors=1)
    knn.fit(X,y)

    dtree = tree.DecisionTreeClassifier()
    dtree.fit(X,y)

    r = read_from_csv(testfile, param_set)

    for i in range(len(r['labels'])):
        verd = r['labels'][i]
        counter += 1

        pred = knn.predict(r['entries'][i].reshape(1,-1))
        if(pred == verd):
            knn_c += 1
        
        pred = dtree.predict(r['entries'][i].reshape(1,-1))
        if(pred == verd):
            dtree_c += 1



    # Matrix de confusao
    # print metrics.confusion_matrix(verd_list, pred_list, labels = list(set(make_aligholi_training_label())))
    # print 'arg dim', len(r['entries'][0])
    # linha['random'] = float(float(rnd_c) / float(counter)) * 100.0
    # print 'random', float(float(rnd_c)/float(counter))*100.0, '%'
    linha['kNN'] = float(float(knn_c) / float(counter)) * 100.0
    # print 'kNN', float(float(knn_c)/float(counter))*100.0, '%'
    # linha['naive'] = float(float(naive_c)/float(counter))*100.0
    # #print 'naive:', float(float(naive_c)/float(counter))*100.0, '%'
    # linha['linear'] = float(float(ln_c)/float(counter))*100.0
    # #print 'linear:', float(float(ln_c)/float(counter))*100.0, '%'
    # linha['svm'] = float(float(svm_c)/float(counter))*100.0
    # #print 'svm:', float(float(svm_c)/float(counter))*100.0, '%'
    # linha['sgdc'] = float(float(sgdc_c)/float(counter))*100.0
    # print 'sgdc:', float(float(sgdc_c)/float(counter))*100.0, '%'
    linha['dtree'] = float(float(dtree_c) / float(counter)) * 100.0
    # print 'dtree:', float(float(dtree_c)/float(counter))*100.0, '%'
    # linha['ann'] = float(float(ann_c)/float(counter))*100.0
    # print 'ann:', float(float(ann_c)/float(counter))*100.0, '%'
    # print '\n\n\n\n'
    linhas.put(linha)
    print param_set


def train(linhas, param_set, filename):
    linha = dict()
    linha['param'] = param_set
    r = read_from_csv(filename, param_set)

    # matrix de confusao
    verd_list = list()
    pred_list = list()

    counter = 0

    rnd_c = 0
    knn_c = 0
    dtree_c = 0
    
    # Shuffle entries with its label
    data = list()
    for entry, label in zip(r['entries'], r['labels']):
        data.append((entry,label))
    shuffle(data)
    part = len(data) / 10

    for i in range(10):
        up = (i+1)*part
        down = i*part
        if i < 9:
            X = [item[0] for item in (data[:down] + data[up:])]
            y = [item[1] for item in (data[:down] + data[up:])]
        
            new = data[down:up]
        else:
            # Ultima iteracao pegar todo o resto
            X = [item[0] for item in data[:down]]
            y = [item[1] for item in data[:down]]
            up = len(data)
            new = data[down:] 

        print down, up 

        knn = neighbors.KNeighborsClassifier(n_neighbors=1)
        knn.fit(X,y)

        dtree = tree.DecisionTreeClassifier()
        dtree.fit(X,y)

        for n in new:
            verd = n[1]
            counter += 1

            # RANDOM CLASSIFIER
            pred = data[randint(0, len(r['labels']) - 1)][1]
            if verd == pred:
                rnd_c += 1

            # kNN CLASSIFIER
            pred = knn.predict(n[0].reshape(1, -1))
            if verd == pred:
                knn_c += 1

            # DECISION TREE CLASSIFIER
            pred = dtree.predict(n[0].reshape(1, -1))
            if verd == pred:
                dtree_c += 1

    # Matrix de confusao
    # print metrics.confusion_matrix(verd_list, pred_list, labels = list(set(make_aligholi_training_label())))
    # print 'arg dim', len(r['entries'][0])
    linha['random'] = float(float(rnd_c) / float(counter)) * 100.0
    # print 'random', float(float(rnd_c)/float(counter))*100.0, '%'
    linha['kNN'] = float(float(knn_c) / float(counter)) * 100.0
    # print 'kNN', float(float(knn_c)/float(counter))*100.0, '%'
    # linha['naive'] = float(float(naive_c)/float(counter))*100.0
    # #print 'naive:', float(float(naive_c)/float(counter))*100.0, '%'
    # linha['linear'] = float(float(ln_c)/float(counter))*100.0
    # #print 'linear:', float(float(ln_c)/float(counter))*100.0, '%'
    # linha['svm'] = float(float(svm_c)/float(counter))*100.0
    # #print 'svm:', float(float(svm_c)/float(counter))*100.0, '%'
    # linha['sgdc'] = float(float(sgdc_c)/float(counter))*100.0
    # print 'sgdc:', float(float(sgdc_c)/float(counter))*100.0, '%'
    linha['dtree'] = float(float(dtree_c) / float(counter)) * 100.0
    # print 'dtree:', float(float(dtree_c)/float(counter))*100.0, '%'
    # linha['ann'] = float(float(ann_c)/float(counter))*100.0
    # print 'ann:', float(float(ann_c)/float(counter))*100.0, '%'
    # print '\n\n\n\n'
    linhas.put(linha)
    print param_set
