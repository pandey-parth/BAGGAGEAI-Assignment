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
so that image does not lie outside its boundary and **resized** it to (150,400) dimension.

After this processing threat image to remove background- `process_threat` fuction in `process` class. Firstly, grayscale it,  
