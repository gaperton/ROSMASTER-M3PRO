# Image mirroring
There are two types of image mirroring: horizontal and vertical. Horizontal mirroring swaps the

image's pixels around its vertical centerline, essentially swapping the left and right halves. Vertical

mirroring swaps the top and bottom halves around its horizontal centerline.


Transformation principle: Let the width of the image be width and the length be height. (x,y)

is the coordinate after transformation, and (x0,y0) is the coordinate of the original image.


**Horizontal mirror transformation**


Forward Mapping


Its inverse transform is


**Vertical mirror transformation**


Its inverse transform is


Summarize:


During a horizontal mirroring transformation, the entire image is traversed, and then each

pixel is processed according to the mapping relationship. In fact, a horizontal mirroring

transformation is to swap the image coordinate columns to the right and the right columns to the

left. The transformation can be performed on a column-by-column basis. The same is true for a

vertical mirroring transformation, which can be performed on a row-by-row basis. Here, we take a

vertical transformation as an example to see how it is written in Python:


Code path:


![](9.-Image-Mirroring.pdf-0-0.jpeg)

![](9.-Image-Mirroring.pdf-0-1.jpeg)

![](9.-Image-Mirroring.pdf-0-2.jpeg)

![](9.-Image-Mirroring.pdf-0-3.jpeg)


```
import cv2

import numpy as np

img = cv2.imread('yahboom.jpg',1)

#cv2.imshow('src',img)

imgInfo = img.shape

height = imgInfo[0]

width = imgInfo[1]

deep = imgInfo[2]

```

```
newImgInfo = (height*2,width,deep)

dst = np.zeros(newImgInfo,np.uint8)#uint8

for i in range(0,height):

for j in range(0,width):

dst[i,j] = img[i,j]

#xy = 2*h - y -1

dst[height*2-i-1,j] = img[i,j]

for i in range(0,width):

dst[height,i] = (0,0,255) #BGR

```


![](9.-Image-Mirroring.pdf-1-0.jpeg)


![](9.-Image-Mirroring.pdf-1-1.jpeg)


![](9.-Image-Mirroring.pdf-1-2.jpeg)

You can see the mirror image from the picture.
