#!/usr/bin/env python
# -*- coding: utf-8 -*-
from toolbox import *
import numpy as np

#Iterar as pastas do dataset ALIGHOLLI

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


#Pegar a media de cor de cada chapa

#verificar com o algoritmo de Vizinho Mais Proximo

#randomizar testes para matriz de confusao