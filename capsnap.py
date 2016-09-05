import cv2
import numpy as np
from numpy import array, arange, uint8 
from matplotlib import pyplot as plt


images = []

def increase_contrast(image_todo):
	array_alpha = np.array([1.99])
	array_beta = np.array([-100.0])
	cv2.add(image_todo, array_beta, image_todo)
	cv2.add(image_todo, array_alpha, image_todo)
	# images.append(image_todo)
	return image_todo

def thresh_and_smoothen(image_todo):
	ret,mask = cv2.threshold(image_todo, 2, 256, cv2.THRESH_BINARY)
	# images.append(mask)
	mask = cv2.GaussianBlur(mask, (3, 3), 50)
	# images.append(mask)
	return mask

def inpaint_original(image_todo, mask):
	final = cv2.inpaint(image_todo, mask, 0, cv2.INPAINT_TELEA)
	images.append(final)
	return final


img = cv2.imread('lena_only_caption.png', cv2.IMREAD_COLOR)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
bw_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

images.append(img)
# images.append(bw_img)

cont_img = increase_contrast(bw_img.copy())
mask = thresh_and_smoothen(cont_img.copy())
final = inpaint_original(img.copy(), mask)


# titles = ['Original Image', 'Thresh and Blurred', 'INPAINTED']
titles = ['Original Image', 'INPAINTED']
 
for i in xrange(len(images)):
    plt.subplot(2, 1,i+1),plt.imshow(images[i],'gray')
    # plt.title(titles[i])
    plt.xticks([]),plt.yticks([])

plt.show()