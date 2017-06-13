import cv2
import argparse
import numpy as np
from numpy import array
from matplotlib import pyplot as plt

images = []
titles = []

#increase contrast to get the text
def increase_contrast(image_todo):
	array_alpha = np.array([1.99])
	array_beta = np.array([-100.0])
	cv2.add(image_todo, array_beta, image_todo)
	cv2.add(image_todo, array_alpha, image_todo)
	images.append(image_todo.copy())
	titles.append('Contrast Increased')
	return image_todo

#threshen to extract text from binarization and apply gaussian blur for antialiaing-ish effect
def thresh_and_smoothen(image_todo):
	ret,mask = cv2.threshold(image_todo, 2, 256, cv2.THRESH_BINARY)
	mask = cv2.GaussianBlur(mask, (5, 5), 0)
	images.append(image_todo.copy())
	titles.append('Threshed and Smoothened')
	return mask

#inpaint over text
def inpaint_text(image_todo, mask):
	final = cv2.inpaint(image_todo, mask, 0, cv2.INPAINT_TELEA)
	titles.append('Inpaint text')
	images.append(final.copy())
	return final

# find black bars by finding perfectly horizontal edges using HoughLines
def find_black_bar_and_draw_lines_on_black_image(img, gray, ip_try):
	edges = cv2.Canny(gray,50,150,apertureSize = 3) #find edges
	limits = [] #limits of upper and lower black bar
	lines = cv2.HoughLines(edges,1,np.pi/180,350)
	lines = np.squeeze(lines)
	for rho,theta in lines:
		a = np.cos(theta)
		b = np.sin(theta)
		if int(b) == 1:
			x0 = a*rho
			y0 = b*rho
			# drawing white lines over mask to inpaint over later
			x1 = int(x0 + 1000*(-b))
			y1 = int(y0 + 1000*(a))
			x2 = int(x0 - 1000*(-b))
			y2 = int(y0 - 1000*(a))
			cv2.line(ip_try,(x1,y1),(x2,y2),(255,255,255),3)
			limits.append(int(y0))
	limits.sort()
	return limits

#recolor black parts
def remove_black_bars(img, limits):
	for i in np.arange (limits[0], limits[1]):
		for j in np.arange(width):
			img[i][j][0] = (img[i][j][0] * 2.52)
			img[i][j][1] = (img[i][j][1] * 2.52)
			img[i][j][2] = (img[i][j][2] * 2.42)
	titles.append('Restore bar color')
	images.append(img.copy())
	return img

#inpaint again over the hard edges of the black bars
def inpaint_again(img, mask):
	final = cv2.inpaint(img, mask, 0, cv2.INPAINT_TELEA)
	return final

# read images

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--img", required = True, help = "Path to the image")
args = vars(ap.parse_args())
img = cv2.imread(args["img"])

#noise vanished due to resizing?
img = cv2.resize(img, (640, 1184), interpolation = cv2.INTER_CUBIC)
cv2.imwrite('example_resize.png', img)
height, width = img.shape[:2]

# resize

# get full black image
ret, ip_try = cv2.threshold(img.copy(), 255, 256, cv2.THRESH_BINARY)
ip_try= cv2.cvtColor(ip_try, cv2.COLOR_BGR2GRAY) #black image

# convert to B/W
bw_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#find black bar limits and draw lines on black image
limits = find_black_bar_and_draw_lines_on_black_image(img, bw_img, ip_try)

#get black bar
black_bar = img[limits[0]:limits[1], 0:width]
bw_black_bar = cv2.cvtColor(black_bar, cv2.COLOR_BGR2GRAY)

#remove text
cont_black_bar = increase_contrast(bw_black_bar)
mask = thresh_and_smoothen(cont_black_bar)
final_bar = inpaint_text(black_bar, mask)

#put back in image
img[limits[0]:limits[1], 0:width] = final_bar

#remove the black bars
img = remove_black_bars(img, limits)

#refine edges of black bar
img = inpaint_again(img, ip_try)

cv2.imwrite('corrected.png', img)

titles.append('Final')
images.append(img.copy())


for i in np.arange(len(images)):
	plt.subplot(2, 4,i+1),plt.imshow(images[i],'gray')
	plt.title(titles[i])
	plt.xticks([]),plt.yticks([])

# plt.show()