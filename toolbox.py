#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import csv
import cv2
import operator
import numpy as np
from random import randint
from sklearn import preprocessing
from skimage.feature import greycomatrix, greycoprops
from colormath.color_diff import delta_e_cie2000
from colormath.color_objects import LabColor
import scipy.stats as st

def make_csv(data, labels):
	with open('data.csv', 'w') as csvfile:
		writer = csv.writer(csvfile, delimiter = ';')
		header = list()
		header.append('label')
		header.extend(('xpl_l', 'xpl_a', 'xpl_b'))
		header.extend(('ppl_l', 'ppl_a', 'ppl_b'))
		header.extend(('biref_l', 'biref_a', 'biref_b'))
		header.extend(('pleoc_l', 'pleoc_a', 'pleoc_b'))
		header.append('ext')
		header.extend(('tex_1', 'tex_2', 'tex_3'))
		header.append('opa_1')
		writer.writerow(header)
		for i in range(0,len(labels)-1):
			writer.writerow(np.append(labels[i], data[i]))

def conf_interval_dict(sample):
	result = dict()
	conf = 0.95
	result['xpl_l'] = st.norm.interval(conf, loc = np.mean(sample[:,0:1]), scale = np.std(sample[:,0:1]))
	result['xpl_a'] = st.norm.interval(conf, loc = np.mean(sample[:,1:2]), scale = np.std(sample[:,1:2]))
	result['xpl_b'] = st.norm.interval(conf, loc = np.mean(sample[:,2:3]), scale = np.std(sample[:,2:3]))
	result['ppl_l'] = st.norm.interval(conf, loc = np.mean(sample[:,3:4]), scale = np.std(sample[:,3:4]))
	result['ppl_a'] = st.norm.interval(conf, loc = np.mean(sample[:,4:5]), scale = np.std(sample[:,4:5]))
	result['ppl_b'] = st.norm.interval(conf, loc = np.mean(sample[:,5:6]), scale = np.std(sample[:,5:6]))
	result['biref_l'] = st.norm.interval(conf, loc = np.mean(sample[:,6:7]), scale = np.std(sample[:,6:7]))
	result['biref_a'] = st.norm.interval(conf, loc = np.mean(sample[:,7:8]), scale = np.std(sample[:,7:8]))
	result['biref_b'] = st.norm.interval(conf, loc = np.mean(sample[:,8:9]), scale = np.std(sample[:,8:9]))
	result['pleoc_l'] = st.norm.interval(conf, loc = np.mean(sample[:,9:10]), scale = np.std(sample[:,9:10]))
	result['pleoc_a'] = st.norm.interval(conf, loc = np.mean(sample[:,10:11]), scale = np.std(sample[:,10:11]))
	result['pleoc_b'] = st.norm.interval(conf, loc = np.mean(sample[:,11:12]), scale = np.std(sample[:,11:12]))
	result['ext'] = st.norm.interval(conf, loc = np.mean(sample[:,12:13]), scale = np.std(sample[:,12:13]))
	result['tex_1'] = st.norm.interval(conf, loc = np.mean(sample[:,13:14]), scale = np.std(sample[:,13:14]))
	result['tex_2'] = st.norm.interval(conf, loc = np.mean(sample[:,14:15]), scale = np.std(sample[:,14:15]))
	result['tex_3'] = st.norm.interval(conf, loc = np.mean(sample[:,15:16]), scale = np.std(sample[:,15:16]))
	result['opa_1'] = st.norm.interval(conf, loc = np.mean(sample[:,16:17]), scale = np.std(sample[:,16:17]))
	return result


def make_confidence_interval(data, labels):
	result = dict()
	current = labels[0]
	sample = list()
	for i in range(0, len(labels)):
		if(current == labels[i]):
			sample.append(data[i])
		else:
			sample = np.asarray(sample)
			if(len(sample) > 1):
				result[current] = conf_interval_dict(sample)
			else:
				pass
			current = labels[i]
			sample = list()
	result[current] = dict()
	sample = np.asarray(sample)
	result[current] = conf_interval_dict(sample)
	return result


#Criando uma array das labels
def make_aligholi_training_label(numbers = False):
	training_labels = list()
	if(numbers == False):
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
	else:
		for i in range(0,5):
			training_labels.append(1)
		for i in range(5, 11):
			training_labels.append(2)
		for i in range(11, 17):
			training_labels.append(3)
		for i in range(17,31):
			training_labels.append(4)
		for i in range(31,34):
			training_labels.append(5)
		for i in range(34,39):
			training_labels.append(6)
		for i in range(39,44):
			training_labels.append(7)
		for i in range(44,54):
			training_labels.append(8)
		for i in range(54,57):
			training_labels.append(9)
		for i in range(57,59):
			training_labels.append(10)
		for i in range(59,60):
			training_labels.append(11)
		for i in range(60,67):
			training_labels.append(12)
		for i in range(67,71):
			training_labels.append(13)
		for i in range(71,76):
			training_labels.append(14)
		for i in range(76,77):
			training_labels.append(15)
		for i in range(77,79):
			training_labels.append(16)
		for i in range(79,81):
			training_labels.append(17)
		for i in range(81,83):
			training_labels.append(18)


	return np.asarray(training_labels)

#dentro de um diretorio
#iterar os arquivos XPL
#fazer media geral xpl
def make_avg_color(folder, light_type):
	images = list()
	for filename in os.listdir(folder):
		if filename.startswith(light_type):
			im = cv2.imread(folder + filename)
			im_lab = to_float_lab(im)
			im_lab = extract_info(np.average, im_lab)
			im = extract_info(np.average, im)
			images.append(im_lab)
	return merge_array(np.average, images)

def make_pleochroism_color(folder, light_type):
	images = list()
	min_l = [200] * 3
	max_l = [0] * 3
	for filename in os.listdir(folder):
		if filename.startswith(light_type):
			im = to_float_lab(cv2.imread(folder + filename), normalize = False)
			im = extract_info(np.average, im)
			if(im[0] < min_l[0]):
				min_l = im
			if(im[0] > max_l[0]):
				max_l = im
	a = LabColor(lab_l = max_l[0], lab_a = max_l[1], lab_b = max_l[2])
	b = LabColor(lab_l = min_l[0], lab_a = min_l[1], lab_b = min_l[2])
	return np.asarray(delta_e_cie2000(a, b))

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
			im = to_float_lab(cv2.imread(folder + filename))
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
			im = to_float_lab(cv2.imread(folder + filename))
			images.append(im)
	result = opacity_param(images)

	images = list()
	for filename in os.listdir(folder):
		if filename.startswith('x'):
			im = to_float_lab(cv2.imread(folder + filename))
			images.append(im)

	return np.append(result, opacity_param(images))

def iterate_alligholli_dataset(param, normalize=False):
	#Itera o dataset
	base_path = './MIfile/MI'
	all_set = list()
	for i in range(1, 84):
 		folder = base_path + str(i) + '/'
		arg = np.empty([0,0])
		if('xpl' in param):
			xpl = make_avg_color(folder, 'x')
			arg = np.append(arg, xpl)
		if('ppl' in param):
			ppl = make_avg_color(folder, 'p')
			arg = np.append(arg, ppl)
		if('biref' in param):
			biref = make_pleochroism_color(folder, 'x')
			arg = np.append(arg, biref)
		if('pleoc' in param):
			pleoc = make_pleochroism_color(folder, 'p')
			arg = np.append(arg, pleoc)
		if('tex' in param):
			tex = make_texture_param(folder)
			arg = np.append(arg, tex)
		if('ext' in param):
			ext = extinction_class(folder)
			arg = np.append(arg, ext)
		if('opa' in param):
			opa = make_opacity_param(folder)
			arg = np.append(arg, opa)

		if(normalize):
			arg = preprocessing.normalize(arg[:, np.newaxis], axis = 0).ravel()

		all_set.append(arg)
	return np.asarray(all_set)

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
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	hist = greycomatrix(image, (1,1), [0], 256, symmetric=False, normed=True)
	result = list()
	props = ['contrast','homogeneity','energy','ASM']
	for p in props:
		im_res = greycoprops(hist, p)
		result.append(im_res[0])
	return result

#Em uma imagem transforma em float e em LAB
def to_float_lab(image, normalize = True):
	image = np.float32(image)
	image = image / 255.0
	image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
	if(normalize):
		image[:,:,0]  = image[:,:,0] / 100.0
		image[:,:,1]  = (image[:,:,1] + 127.0) / 254.0
		image[:,:,2]  = (image[:,:,2] + 127.0) / 254.0

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
	image = func(image, axis=0)
	image = func(image, axis=0)
	return image

#func -> funcao np para extrair a informacao
#		- np.average
#		- np.min
#		- np.max
#collection -> colecao de informacoes da imagem
def merge_array(func, collection):
	arr = np.asarray(collection)
	return func(arr, axis=0)
