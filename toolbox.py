#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import csv
import cv2
import operator
import numpy as np
from random import randint
from skimage.feature import greycomatrix, greycoprops


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

	return np.asarray(training_labels)

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
		target = randint(0, len(collection) -1)
		result['new_entry_set'].append(collection[target])
		result['new_entry_labels'].append(labels[target])
		collection = np.delete(collection, target, 0)
		labels = np.delete(labels, target, 0)

	result['labels'] = labels
	result['training'] = collection
	result['new_entry_set'] = np.asarray(result['new_entry_set'])
	result['new_entry_labels'] = np.asarray(result['new_entry_labels'])
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

def iterate_alligholli_dataset():
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
	return all_set

def read_param_from_csv_file():
	with open('param.csv', 'r') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		all_set = list()
		for row in reader:
			all_set.append([float(i) for i in row])
		return np.asarray(all_set)

def read_labels_from_csv_file():
	with open('labels.csv', 'r') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		labels = list()
		for row in reader:
			labels.append(row[0])
		return np.asarray(labels)


#classifica o minerio de acordo com seu angulo de extincao
def get_extinction_pos(collection):
	menor_l = 9999
	pos = -1

	for i in range(len(collection)):
		l,_,_ = cv2.split(collection[i])

		l = np.average(l, axis=0)
		l = np.average(l, axis=0)

		if(l < menor_l):
			menor_l = l
			pos = i

	return pos

#pega o brilho e seu desvio padrao
def opacity_param(collection):
	all_l = None
	all_stddev = None

	for i in range(len(collection)):
		l,_,_ = cv2.split(collection[i])
		l = np.average(l, axis=0)
		l = np.average(l, axis=0)

		dev = cv2.meanStdDev(collection[i])
		dev = np.average(dev, axis=0)
		dev = dev[0]

		if(all_l == None):
			all_l = l
			all_stddev = dev
		else:
			all_l = np.append(all_l, l)
			all_stddev = np.append(all_stddev, dev)

	l = np.average(all_l, axis=0)
	dev = np.average(all_stddev, axis=0)

	return np.append(l,dev)

#Função de calcular os parâmetros de Textura
def texture_param(image):
	cv2.namedWindow("im")
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	hist = greycomatrix(image, (1,1), [0], 256, symmetric=False, normed=True)
	result = list()
	props = ['contrast','homogeneity','energy','ASM']
	for p in props:
		im_res = greycoprops(hist, p)
		result.append(im_res[0])
	return result

#Função da distância euclidiana em um espaõ n-dimencional
def distance(p0, p1):
	'Computa a disntacia euclidiana ao quadrado'
	return np.sum((p0-p1)**2)

#Algoritmo de vizinho mais proximo
def nn_classify(training_set, training_labels, new_entry):
	dists = np.array([distance(t, new_entry) for t in training_set])
	nearest = dists.argmin()
	return training_labels[nearest]

#Em uma imagem transforma em float e em LAB
def to_float_lab(image):
	image = np.float32(image)
	image = image / 255.0
	image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
	return image

#Extrai as informacoes da imagem
#type -> o tipo de informação a ser extraída
#		- 'avg'
#		- 'min'
#		- 'max'
#func -> funcao np para extrair a informacao
#		- np.average
#		- np.min
#		- np.max
#image -> imagem ou ROI que vai ser extraido
def extract_info(func, image):
	l,a,b = cv2.split(image)

	l = func(l, axis=0)
	l = func(l, axis=0)

	a = func(a, axis=0)
	a = func(a, axis=0)

	b = func(b, axis=0)
	b = func(b, axis=0)

	result = list()
	result.append(l)
	result.append(a)
	result.append(b)

	return result

#func -> funcao np para extrair a informacao
#		- np.average
#		- np.min
#		- np.max
#collection -> colecao de informacoes da imagem
def merge_array(func, collection):
	arr = np.zeros((len(collection), 3), dtype=np.float32)
	for i in range(0, len(collection)):
		arr[i] = collection[i]
	return func(arr, axis=0)
