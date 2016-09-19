# capsnap
CapSnap is a tool to remove captions off Snapchat images and restore the original image.


#####Work still in progress.

##Comparision of Original and Corrected Image

![image](http://i.imgur.com/VY0XF5z.png)

##How it works

1. The image is read an converted to B/W to execute operations upon
2. We then find the black bars of the caption to be replaced using [Hough Line Transform](http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html). We check the conditions where the line returned by this transform has `cos(theta) = 0` which implies that the edge is perfectly horizonatal. Credits to a SO answer [here](http://stackoverflow.com/questions/7227074/horizontal-line-detection-with-opencv)
3. After we have the black caption bar, we simply extract that part out from the image to work upon. This reduces the load on the algorithms 
4. This caption bar has [Contrast Enhancement](http://docs.opencv.org/2.4/doc/tutorials/core/basic_linear_transform/basic_linear_transform.html) applied on it so that the text comes out upfront and should be easy to inpaint. We use the principle that *every pixel can be transformed as X = aY + b where a and b are scalars and control the contrast and brightness*. Have a look at the reference article on SO [here](http://stackoverflow.com/questions/19363293/whats-the-fastest-way-to-increase-color-image-contrast-with-opencv-in-python-c).
5. Having gotten the text now, we simply apply [Binary Thresholding](http://docs.opencv.org/trunk/d7/d4d/tutorial_py_thresholding.html) to obtain the mask for [Inpainting](http://docs.opencv.org/2.4/modules/photo/doc/inpainting.html) the text.
6. After inpainting the text, we have tried and reconstructed that part of the image hidden away behind the text. Now, we multiply every pixel value in this black caption bar by a constant `2.52/2.42` to attempt and restore the original color of the image.
7. Having done this, we finally inpaint over the edges of the image obtained after recoloring the image. This should ensure a smooth and uniform image as the output.
8. The final image with a removed caption is obtained.

####Steps described are shown below
![image](http://i.imgur.com/L3SPmW5.png)

##Usage

####Dependencies: `cv, numpy, matplotlib, argparse`

To run: `python capsnap.py --img /pathtoimage/imagename.format`




