from image_processing import process # image_processing.py file
import cv2 as cv
import numpy as np

background_img_path='./background_images/S0320365070_20180821160850_L-12_5.jpg' #path to image file
threat_img_path='./threat_images/BAGGAGE_20170524_075554_80428_B.jpg'

baggage= process(background_img_path,threat_img_path,5) # Initialising class 

bcg_img=baggage.load_background_image() #function loads background image

thr_img = baggage.load_threat_image() # function loads threat image and resize and rotate it

processed_threat_image=baggage.process_threat(thr_img) # explained in image_processing.py file

process_bag=baggage.add_threat(processed_threat_image,bcg_img,(300,200))
baggage.plot(process_bag)
print('Threat Object is present in Baggage: ', baggage.check_threat_in_boundary(process_bag,bcg_img))
process_bag=np.array(process_bag)
process_bag=cv.cvtColor(process_bag,cv.COLOR_BGR2RGB)
cv.imwrite('.\Result_images/08.jpg',process_bag)

