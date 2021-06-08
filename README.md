# BAGGAGEAI-Assignment
Given two sets of images:- background and threat objects. Your task is to cut the threat objects, scale it down, rotate with 45 degree and paste it  into the background images using image processing techniques in python

`Resources` Folder has images which I will use to make readme

`Result_images` Folder has resukted final images

`background images` Folder has images of X ray scanned baggage used as input

`threat images` Folder has images of X ray scanned threat object used as input

`BaggageAI_CV_Hiring_assignment.pdf` having problem statement

`Practice.ipynb` is notebook file where I have used various algorithm for practice. I will not reccomend it to understand, next 2 files are final solution.
## Solution Files
`image_processing.py` - make all functions like loading, processing, plotting of image

`main.py`- where final program will run and shows result.
### Background and Threat Images
Here I see that Threat images are much bigger in size and has high ratio of background in it.

**image_processing.py**

First task is to load background image and threat image

For threat image we need to rotate it- using function `load_threat_image` in `process` class used fuctions cv.getRotationMatrix2D; cv.warpAffine and for each image used different centres
so that image does not lie outside its boundary and **resized** it to (100,200) dimension. ![](https://github.com/pandey-parth/BAGGAGEAI-Assignment/blob/main/Resources/rotated.png)

After this processing threat image to remove background- `process_threat` fuction in `process` class. Firstly, grayscale it,  inverse_threshold the image with values greater than 240
 will be assign 255- `_, threshd = cv.threshold(gray, 240, 255, cv.THRESH_BINARY_INV)`![](https://github.com/pandey-parth/BAGGAGEAI-Assignment/blob/main/Resources/mask.png)

From here to remove background and paste it to baggage- I have tested 2 methods, Best method based on runtime is used in file, but another method can be seen in notebook file


**Method1**

After masking make roi same size of threat image and run a loop on roi such that when mask pixle is (255) it will change roi value of threat image.
Then paste roi to bag_image
Runtime for this method- `104 ms ± 7.27 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)`

**Method2**

After inverse thresholding used kernel of elliptical shape and morphed it to mask image to increase smoothness. `morphed = cv.morphologyEx(threshd, cv.MORPH_CLOSE, kernel)`.
 Now find contour, draw it. After this used bitwise_and operation `masked_data = cv.bitwise_and(img, img, mask=mask)` to get color on mask.
 
I had darken the color so that it will look translucent. ![](https://github.com/pandey-parth/BAGGAGEAI-Assignment/blob/main/Resources/process_image.png)

Runtime- `9.98 ms ± 470 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)`
**10 times faster!!**

Now `add_image` function is used to paste processed image to background image and provide coordinates so that we will see later that threat present in bggage or not.

**Check threat in Boundary**

Here I masked processed final baggage image and initial baggage image using inverse threshold, kernel, morphing and draawing contours.
After this used `absdiff` on 2 arrays and see how many non zeros are present! Change only occured in pasting part and pasting part has more than 2000 pixles.

There are few pixles that remain non zero due to incomplete tight bound so I have used `if num_of_non_zeros < 200` return True

**Final Result**

![](https://github.com/pandey-parth/BAGGAGEAI-Assignment/blob/main/Result_images/08.jpg)
