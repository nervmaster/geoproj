#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
from skimage.feature import greycomatrix, greycoprops

#Função de calcular os parâmetros de Textura
def texture_param(image):
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	hist = greycomatrix(image, [1], [0], 256)
	result = list()
	props = ['contrast','homogeneity','energy','ASM']

	for p in props:
		result.append(greycoprops(hist, p))

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
