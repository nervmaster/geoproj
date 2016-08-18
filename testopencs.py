import argparse
import cv2
import numpy as np

refPt = []
cropping = False
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
		cv2.imshow("image", image)
# Pega a imagem
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

# Seta as chamadas de funcao dos eventos
image = cv2.imread(args["image"])
clone = image.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)

# Motor da  janela
while True:
	cv2.imshow("image", image)
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
	# min_value = np.min(roi.ravel())
	# max_value = np.min(roi.ravel())
	# print min_value, max_value
	roi = roi / 255.0

	roi = cv2.cvtColor(roi, cv2.COLOR_BGR2LAB)

	# iterar os pixels
	height, width, depth = roi.shape
	print height, width, depth
	for i in range (0, height):
		for j in range(0, width):
			# print roi[i,j]
			pass

	# roi = cv2.cvtColor(roi, cv2.COLOR_LAB2BGR)
	# cv2.imshow("ROI",roi)
	cv2.waitKey(0)

cv2.destroyAllWindows()