import cv2 as cv
from matplotlib import pyplot as plt
from PIL import Image
import numpy as np




class process():
    def __init__(self,bcg_path,threat_path,img_no): # input required are path of image and threat image number
        self.bcg_path=bcg_path
        self.threat_path=threat_path
        self.no=img_no
    
    def load_background_image(self): # function will read image and convert it to RGB channel
        img=cv.imread(self.bcg_path)
        img=cv.cvtColor(img,cv.COLOR_BGR2RGB)
        return img
    
    def load_threat_image(self): # function will read image and convert it to RGB channel; resize and rotated
        img= cv.imread(self.threat_path)
        img=cv.cvtColor(img,cv.COLOR_BGR2RGB)
        
        center_list=[(50,200),(50,450),(150,600),(150,220),(10,570)] # for every image we will take different centres
        h,w,ch=img.shape
            
        M=cv.getRotationMatrix2D(center_list[self.no -1],45,1.0) # rotate 45 deg CCW
        rot=cv.warpAffine(img,M,(w,h),borderValue=(255,255,255))
        img=cv.resize(rot,(150,400))
        return img

    def process_threat(self,img): # Processing threat image (making boundary tight bound)
        gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY) # grayscale

        _, threshd = cv.threshold(gray, 240, 255, cv.THRESH_BINARY_INV) # inverse thresholding

        kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (11, 11)) # initiating elliptical kernel

        morphed = cv.morphologyEx(threshd, cv.MORPH_CLOSE, kernel) # smoothing out threshold image using morphology and kernel

        cnts = cv.findContours(morphed, 
                                cv.RETR_EXTERNAL,
                                cv.CHAIN_APPROX_SIMPLE)[0]   # Finding contour points(boundary points of threat image)
        
        cnt = sorted(cnts, key=cv.contourArea)[-1]
        
        mask = cv.drawContours(threshd, cnt, 0, (0, 0, 0), 5) # drawing contour
        masked_data = cv.bitwise_and(img, img, mask=mask)
        
        x, y, w, h = cv.boundingRect(cnt) # It will bound threat image
        dst = masked_data[y: y + h, x: x + w]
        
        dst_gray = cv.cvtColor(dst, cv.COLOR_RGB2GRAY)
        _, alpha = cv.threshold(dst_gray, 0, 255, cv.THRESH_BINARY)
        b, g, r = cv.split(dst)
        
        rgba = [b, g, r, alpha]
        dst = cv.merge(rgba, 4)
        dst=np.multiply(dst,0.8) # Look translucent
        
        return dst.astype('uint8')
    
    def add_threat(self,thr_img,bcg_img,coord): # pasting threat on baggage 

        background = Image.fromarray(bcg_img)
        image = Image.fromarray(thr_img)
        
        background.paste(image,coord,image) # ccordinates input
        return background
    
    def check_threat_in_boundary(self,prc_img,bcg_img): # For checking we will use similar method we used in process_image
        prc_img=np.array(prc_img)                       # that pasted image and baggage image were masked (grayscale, thresholding, contour)
        bg_gr=cv.cvtColor(bcg_img,cv.COLOR_RGB2GRAY)    # after that use cv.absdiff that will give how many non-zeroes are there
        _, threshed = cv.threshold(bg_gr, 240, 255, cv.THRESH_BINARY_INV) # I have used 200 as max non-zeroes (~4000 pixles preesent in threat)

        kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (11, 11))

        morphed = cv.morphologyEx(threshed, cv.MORPH_CLOSE, kernel)

        cnts = cv.findContours(morphed, 
                                cv.RETR_EXTERNAL,
                                cv.CHAIN_APPROX_SIMPLE)[0]
        
        cnt = sorted(cnts, key=cv.contourArea)[-1]
        
        mask_bg= cv.drawContours(threshed, cnt, 0, (0, 0, 0), 0)

        pc_gr=cv.cvtColor(prc_img,cv.COLOR_RGB2GRAY)
        _, threshd = cv.threshold(pc_gr, 240, 255, cv.THRESH_BINARY_INV)

        kernl = cv.getStructuringElement(cv.MORPH_ELLIPSE, (11, 11))

        morphd = cv.morphologyEx(threshd, cv.MORPH_CLOSE, kernl)

        cnts = cv.findContours(morphd, 
                                cv.RETR_EXTERNAL,
                                cv.CHAIN_APPROX_SIMPLE)[0]
        
        cnt = sorted(cnts, key=cv.contourArea)[-1]
        
        mask_pc= cv.drawContours(threshd, cnt, 0, (0, 0, 0), 0)
        
        arr=cv.absdiff(mask_bg,mask_pc)
        num_of_non_zeros = np.count_nonzero(arr)
        if num_of_non_zeros < 200:
            return True
        else:
            return False
    
    def plot(self,img):
        img = np.array(img)
        img=cv.cvtColor(img,cv.COLOR_BGR2RGB)
        cv.imshow('image',img)
        cv.waitKey(0)
    
