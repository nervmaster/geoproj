import argparse
import cv2
import numpy as np



# Funcao de dist euclidiana
def distance(p0, p1):
	'Computa a disntacia euclidiana ao quadrado'
	return np.sum((p0-p1)**2)

# Algoritmo de vizinho mais proximo
def nn_classify(training_set, training_labels, new_example):
	dists = np.array([distance(t, new_example) for t in training_set])
	nearest = dists.argmin()
	return training_labels[nearest]



def crop_new_image(images):
	global refPt 
	global cropping 
	global image
	refPt = []
	cropping = False
	for i in range(0, len(images)):
		# mostra thumbnails da images
		image = cv2.imread(images[i])
		cv2.namedWindow("image" + str(i), cv2.WINDOW_NORMAL)
		cv2.imshow("image" + str(i), image)


	for i in range(0, len(images)):
		# Seta as chamadas de funcao dos eventos
		image = cv2.imread(images[i])
		clone = image.copy()
		cv2.namedWindow("CROP HERE", cv2.WINDOW_NORMAL)
		cv2.setMouseCallback("CROP HERE", click_and_crop)

		# Motor da  janela
		while True:
			cv2.imshow("CROP HERE", image)
			key = cv2.waitKey(1) & 0xFF

			if key == ord("r"):
				image = clone.copy()

			elif key == ord("c"):
				break

		# Pegou a imagem recortada
		if len(refPt) == 2:
			roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
			# ROI eh a imagem recortada

			# Mudar espaco de cores
			roi = np.float32(roi)
			roi = roi / 255.0
			roi = cv2.cvtColor(roi, cv2.COLOR_BGR2LAB)

			# iterar os pixels
			# cria um array em numpy
			l,a,b = cv2.split(roi)
			
			# valor l
			l = np.average(l, axis=0)
			l = np.average(l, axis=0)

			# valor a
			a = np.average(a, axis=0)
			a = np.average(a, axis=0)
			
			# valor b
			b = np.average(b, axis=0)
			b = np.average(b, axis=0)

			print 'avg: ',l, a, b

			# MIN
			l,a,b = cv2.split(roi)

			l = np.min(l, axis=0)
			l = np.min(l, axis=0)

			# valor a
			a = np.min(a, axis=0)
			a = np.min(a, axis=0)
			
			# valor b
			b = np.min(b, axis=0)
			b = np.min(b, axis=0)

			print 'min: ',l, a, b

			# MAX
			l,a,b = cv2.split(roi)

			l = np.max(l, axis=0)
			l = np.max(l, axis=0)

			# valor a
			a = np.max(a, axis=0)
			a = np.max(a, axis=0)
			
			# valor b
			b = np.max(b, axis=0)
			b = np.max(b, axis=0)

			print 'max: ',l, a, b

			roi = cv2.cvtColor(roi, cv2.COLOR_LAB2BGR)
			cv2.imshow("ROI",roi)
			cv2.waitKey(0)
		cv2.destroyWindow("CROP HERE") 
	cv2.destroyAllWindows()

#pega coordenadas do crop retangulo
def click_and_crop(event, x, y, flags, param):
	global refPt, cropping

	if event == cv2.EVENT_LBUTTONDOWN:
		refPt = [(x,y)]
		cropping = True

	elif event == cv2.EVENT_LBUTTONUP:
		refPt.append((x,y))
		cropping = False

		cv2.rectangle(image, refPt[0], refPt[1], (0,255,0), 2)
		cv2.imshow("CROP HERE", image)


