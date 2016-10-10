#!/usr/bin/env python
# -*- coding: utf-8 -*-
from toolbox import *
from random import randint
import numpy as np
import os
import cv2
import operator
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import normalize


#Criando uma array das labels
def make_aligholi_training_label():
	training_labels = list()
	for i in range(0,5):
		training_labels.append('Anthophilite')
	for i in range(5, 11):
		training_labels.append('Augite')
	for i in range(11, 17):
		training_labels.append('Olivine')
	for i in range(17,31):
		training_labels.append('Biotite')
	for i in range(31,34):
		training_labels.append('Muscovite')
	for i in range(34,39):
		training_labels.append('Calcite')
	for i in range(39,44):
		training_labels.append('Brown hornblende')
	for i in range(44,54):
		training_labels.append('Green hornblende')
	for i in range(54,57):
		training_labels.append('Chlorite')
	for i in range(57,59):
		training_labels.append('Opx')
	for i in range(59,60):
		training_labels.append('Apatite')
	for i in range(60,67):
		training_labels.append('Quartz')
	for i in range(67,71):
		training_labels.append('Plagioclase')
	for i in range(71,76):
		training_labels.append('Orthoclase')
	for i in range(76,77):
		training_labels.append('Microcline')
	for i in range(77,79):
		training_labels.append('Sanidine')
	for i in range(79,81):
		training_labels.append('Lucite')
	for i in range(81,83):
		training_labels.append('Garnet')

	return training_labels

#dentro de um diretorio
#iterar os arquivos XPL
#fazer media geral xpl
def make_avg_color(folder, light_type):
	images = list()
	for filename in os.listdir(folder):
		if filename.startswith(light_type):
			im = cv2.imread(folder + filename)
			images.append(extract_info(np.average, im))
	return merge_array(np.average, images)

def make_pleochroism_color(folder, light_type):
	images = list()
	min_l = [200] * 3
	max_l = [0] * 3
	for filename in os.listdir(folder):
		if filename.startswith(light_type):
			im = cv2.imread(folder + filename)
			im = extract_info(np.average, im)
			if(im[0] < min_l[0]):
				min_l = im
			if(im[0] > max_l[0]):
				max_l = im
	return np.subtract(max_l, min_l)

def make_training_sets(collection, labels):
	size = len(collection) / 10
	result = dict()
	result['new_entry_set'] = list()
	result['new_entry_labels'] = list()
	for i in range(0,size):
		target = randint(0, len(collection)-1)
		result['new_entry_set'].append(collection[target])
		result['new_entry_labels'].append(labels[target])
		del collection[target]
		del labels[target]
	result['labels'] = list()
	result['labels'] = labels

	result['training'] = list()
	result['training'] = collection

	return result

def make_texture_param(folder):
	images = list()
	for filename in os.listdir(folder):
		if filename.endswith('.png'):
			im = cv2.imread(folder + filename)
			images.append(texture_param(im))

	result = np.zeros((len(images),4), dtype = np.float32)
	for i in range(len(images[0])):
		for j in range(len(images)):
			result[j][i] = images[j][i]
	res = np.average(result,axis=0)
	return res

def extinction_class(folder):
	images = list()
	for filename in os.listdir(folder):
		if filename.startswith('x'):
			im = cv2.imread(folder + filename)
			images.append(im)
	pos =  get_extinction_pos(images)
	pos = pos*5
	ext = -1
	if(0 <= pos <= 5 or 85 <= pos <= 90):
		ext = 1
	elif(10 <= pos <= 20 or 70 <= pos <= 80):
		ext = 2
	elif(25 <= pos <= 35 or 55 <= pos <= 65):
		ext = 3
	else:
		ext = 4

	return ext

def make_opacity_param(folder):
	images = list()
	for filename in os.listdir(folder):
		if filename.startswith('p'):
			im = cv2.imread(folder + filename)
			images.append(im)
	result = opacity_param(images)

	images = list()
	for filename in os.listdir(folder):
		if filename.startswith('x'):
			im = cv2.imread(folder + filename)
			images.append(im)

	return np.append(result, opacity_param(images))


# Cria as labels
labels = make_aligholi_training_label()

#Itera o dataset
base_path = './MIfile/MI'
all_set = list()
for i in range(1, 84):
	folder = base_path + str(i) + '/'

	xpl = make_avg_color(folder, 'x')
	ppl = make_avg_color(folder, 'p')
	biref = make_pleochroism_color(folder, 'x')
	pleoc = make_pleochroism_color(folder, 'p')
	tex = make_texture_param(folder)
	ext = extinction_class(folder)
	opa = make_opacity_param(folder)

	args = np.append(biref, xpl)
	args = np.append(args, ppl)
	args = np.append(args, pleoc)
	args = np.append(args, tex)
	args = np.append(args, ext)
	args = np.append(args, opa)

	args = normalize(args[:, np.newaxis], axis = 0).ravel()

	all_set.append(args)
#matrix de confusao
verd_list = list()
pred_list = list()

counter = 0
correct = 0
incorrect = 0

for i in range(0,1000):

	t_set = all_set[:]
	t_labels = labels[:]

	#Criar o traning set
	sets = make_training_sets(t_set, t_labels)

	#verificar com o algoritmo de Vizinho Mais Proximo
	for j in range(0, len(sets['new_entry_set'])):
		pred = nn_classify(sets['training'], sets['labels'], sets['new_entry_set'][j])
		verd = sets['new_entry_labels'][j]
		if verd == pred:
			correct += 1
		else:
			incorrect += 1
		counter += 1
		pred_list.append(pred)
		verd_list.append(verd)

#Matrix de confusao
#print confusion_matrix(verd_list, pred_list, labels = list(set(make_aligholi_training_label())))
print float(float(correct)/float(counter))*100.0, '%'
print 'dim', len(all_set[0])
