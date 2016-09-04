import cv2
import numpy as np
from matplotlib import pyplot as plt


def increase_contrast(image):
	maxIntensity = 255.0 # depends on dtype of image data
	x = arange(maxIntensity) 

	# Parameters for manipulating image data
	phi = 1
	theta = 1

	# Increase intensity such that
	# dark pixels become much brighter, 
	# bright pixels become slightly bright
	contasted_image = (maxIntensity/phi)*(image/(maxIntensity/theta))**0.5
	contasted_image = array(contasted_image,dtype=uint8)

	cv2.imshow('contasted_image',contasted_image)
	return contasted_image

img = cv2.imread('only_caption.jpg',0)
#img = increase_contrast(img)
ret,thresh1 = cv2.threshold(img,50,255,cv2.THRESH_BINARY)

mask = thresh1
dst = cv2.inpaint(img,mask,3,cv2.INPAINT_TELEA)
 
titles = ['Original Image','BINARY THRESH','INPAINTED']
images = [img, thresh1, dst]
 
for i in xrange(3):
    plt.subplot(2,3,i+1),plt.imshow(images[i],'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])

plt.show()