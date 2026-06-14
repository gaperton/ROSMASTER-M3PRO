# Image binarization
The core idea of binarization is to set a threshold, with values above the threshold being set to 0

(black) or 255 (white), making the image black and white. The threshold can be fixed or adaptive.

An adaptive threshold typically compares a pixel at a point with the average value of the pixels in

the region around that point, or with a weighted sum of Gaussian distributions. This difference

can be set or not.


Global Threshold:


Python-OpenCV provides a threshold function: cv2.threshold(src, threshold, maxValue, method)


src original image: the dashed line is the value to be thresholded; the dotted line is the threshold


cv2.THRESH_BINARY: The grayscale value of pixels greater than the threshold is set to maxValue

(for example, the maximum 8-bit grayscale value is 255), and the grayscale value of pixels less

than the threshold is set to 0.


cv2.THRESH_BINARY_INV : The grayscale value of pixels above the threshold is set to 0, while

those below the threshold are set to maxValue.


cv2.THRESH_TRUNC: Pixels with grayscale values less than the threshold value will not be

changed, and pixels with grayscale values greater than the threshold value will be set to the

threshold value.


cv2.THRESH_TOZERO: Pixels with grayscale values less than the threshold value will not be

changed, while those with grayscale values greater than the threshold value will all be changed to

0.


cv2.THRESH_TOZERO_INV: Pixels with grayscale values greater than the threshold will not be

changed; pixels with grayscale values less than the threshold will all be changed to 0.


Code path:


![](14.-Image-Binarization.pdf-1-0.jpeg)


![](14.-Image-Binarization.pdf-1-1.jpeg)
