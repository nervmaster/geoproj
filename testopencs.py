import argparse
import cv2
import numpy as np


#classifica o minerio de acordo com seu angulo de extincao
def get_extinction_class(collection):
	menor_l = 9999
	pos = -1

	for i in range(len(collection)):
		l,_,_ = cv2.split(collection[i])

		l = np.average(l, axis=0)

		if(l < menor_l):
			menor_l = l
			pos = i

	print pos
	exit(1)

# Funcao de dist euclidiana
def distance(p0, p1):
	'Computa a disntacia euclidiana ao quadrado'
	return np.sum((p0-p1)**2)

# Algoritmo de vizinho mais proximo
def nn_classify(training_set, training_labels, new_example):
	dists = np.array([distance(t, new_example) for t in training_set])
	nearest = dists.argmin()
	return training_labels[nearest]

#pega coordenadas do crop retangulo
def click_and_crop(event, x, y, flags, param):
	global refPt, cropping

	if event == cv2.EVENT_LBUTTONDOWN:
		refPt.append((x,y))
		cropping = True

	elif event == cv2.EVENT_LBUTTONUP:
		refPt.append((x,y))
		cropping = False

		cv2.rectangle(image, refPt[-2], refPt[-1], (0,255,0), 2)
		cv2.imshow("CROP HERE", image)

#extrai propriedades de cor de uma imagem
def extract_color_input(roi):
	color_input = list()
	for im in roi:
		result = dict()

		# Mudar espaco de cores
		im = np.float32(im)
		im = im / 255.0
		im = cv2.cvtColor(im, cv2.COLOR_BGR2LAB)

		# iterar os pixels
		# cria um array em numpy
		l,a,b = cv2.split(im)

		# valor l
		l = np.average(l, axis=0)
		l = np.average(l, axis=0)

		# valor a
		a = np.average(a, axis=0)
		a = np.average(a, axis=0)

		# valor b
		b = np.average(b, axis=0)
		b = np.average(b, axis=0)

		result['avg'] = list()
		result['avg'].append(l)
		result['avg'].append(a)
		result['avg'].append(b)

		# MIN
		l,a,b = cv2.split(im)

		l = np.min(l, axis=0)
		l = np.min(l, axis=0)

		# valor a
		a = np.min(a, axis=0)
		a = np.min(a, axis=0)

		# valor b
		b = np.min(b, axis=0)
		b = np.min(b, axis=0)

		result['min'] = list()
		result['min'].append(l)
		result['min'].append(a)
		result['min'].append(b)

		# MAX
		l,a,b = cv2.split(im)

		l = np.max(l, axis=0)
		l = np.max(l, axis=0)

		# valor a
		a = np.max(a, axis=0)
		a = np.max(a, axis=0)

		# valor b
		b = np.max(b, axis=0)
		b = np.max(b, axis=0)

		result['max'] = list()
		result['max'].append(l)
		result['max'].append(a)
		result['max'].append(b)

		color_input.append(result)
	#Criando um NP Array para calculo dos canais
	arr = np.zeros((len(color_input), 3), dtype=np.float32)
	for i in range(0,len(color_input)):
		arr[i] = color_input[i]['avg']
	return np.average(arr, axis=0)

#converge as propriedades da colecao
def merge_color_input(collection):
	arr = np.zeros((len(collection), 3), dtype=np.float32)
	for i in range(0, len(collection)):
		arr[i] = collection[i]
	return np.average(arr, axis=0)

#faz a atividade de crop de uma colecao de imagens
def crop_new_image(images):
	global refPt
	global cropping
	global image
	ppllist = list()
	xpllist = list()

	for i in range(0, len(images)):
		# mostra thumbnails da images
		image = images[i]
		cv2.namedWindow("image" + str(i), cv2.WINDOW_NORMAL)
		cv2.imshow("image" + str(i), image)


	for i in range(0, len(images)):
		refPt = []
		cropping = False
		xpl = False
		ppl = False

		# Seta as chamadas de funcao dos eventos
		image = images[i]
		clone = image.copy()
		cv2.namedWindow("CROP HERE", cv2.WINDOW_NORMAL)
		cv2.setMouseCallback("CROP HERE", click_and_crop)

		# Motor da  janela
		while True:
			cv2.imshow("CROP HERE", image)
			key = cv2.waitKey(1) & 0xFF

			if key == ord("r"):
				image = clone.copy()

			elif key == ord("x"):
				xpl = True
				break

			elif key == ord("p"):
				ppl = True
				break

		# Pegou a imagem recortada
		if len(refPt) >= 2:
			# ROI eh um  vetor de imagens recortadas
			roi = list()
			for i in range(0, len(refPt), 2):
				roi.append(clone[refPt[i][1]:refPt[i+1][1], refPt[i][0]:refPt[i+1][0]])
			if(xpl):
				xpllist = xpllist + roi
			else:
				ppllist = ppllist + roi

		cv2.destroyWindow("CROP HERE")
	cv2.destroyAllWindows()
	return xpllist, ppllist
