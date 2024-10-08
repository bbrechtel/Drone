#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Some of these imports might not be completely necessary but just to be safe we chose to keep all of them
import numpy as np
import cv2
import cvlib
import matplotlib as plt
import random
import os


# In[2]:


####################### STEP 1: BACKGOUND REMOVAL #######################
# Infrared Picture Function
def load_infrared_cleaned_image(image_number):
    # Prepping function
    image_number = str(image_number)
    window_name = "image"
    
    # Inserting unique path (obviously we will each have a unique path here)
    # Make sure that you have the second backslash at the end 
    path = r"C:\Users\bbrec\Downloads\data22\\" + image_number + ".bmp"
    image = cv2.imread(path)
    
    # Resizing the image. Got from ChatGPT
    new_size = (700, 600)  # Specify the new dimensions
    resized_image = cv2.resize(image, new_size)
    
    # Converting the image to infrared. Got from ChatGPT
    grayscale_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
    infrared_image = cv2.applyColorMap(grayscale_image, cv2.COLORMAP_HOT)  # You can try other colormaps as well
    
    
    # Creating the median image  
    median_image = cv2.medianBlur(infrared_image,11)
    
    # Subtracting the median image from the infrared image in order to make the drone stand out more. 
    final_image = cv2.subtract(infrared_image,median_image)
    
    # Options for showing other pics in the cleaning process 
    #cv2.imshow(window_name,resized_image)
    
    #cv2.imshow(window_name, infrared_image)
    
    #cv2.imshow(window_name, final_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return resized_image


# grayscale image function
def load_grayscale_cleaned_image(image_number):
    
    
    # Prepping function
    image_number = str(image_number)
    window_name = "image"
    
    # Inserting unique path (obviously we will each have a unique path here)
    # Make sure that you have the second backslash VV 
    path = r"C:\Users\bbrec\Downloads\data22\\" + image_number + ".bmp"
    image = cv2.imread(path)
    
    # Resizing the image. Got from ChatGPT
    new_size = (600, 600)  # Specify the new dimensions
    resized_image = cv2.resize(image, new_size)
    
    # Converting the image to infrared. Got from ChatGPT
    grayscale_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
    #infrared_image = cv2.applyColorMap(grayscale_image, cv2.COLORMAP_HOT)  # You can try other colormaps as well
    
    
    # Creating the median image  
    median_image = cv2.medianBlur(grayscale_image,7)
    
    # Subtracting the median image from the infrared image in order to make the drone stand out more. 
    final_image = cv2.subtract(grayscale_image,median_image)
    
    
    
    # Options for showing other pics in the cleaning process 
    #cv2.imshow(window_name,resized_image)
    
    #cv2.imshow(window_name, infrared_image)
    
    #cv2.imshow(window_name, final_image)
    new_grey = final_image
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return new_grey


# In[ ]:





# In[3]:


####################### STEP 2: OBJECT DETECTION #######################
# This is the Naive function for finding the drone. Naive means this is simply looking for the brightest pixel in the image
# as opposed to the brightest group of pixels. When orginally tested had an 80% accuracy rate of finding t
def findDroneNaive(pic):
    
    # Loading the images using the other functions
    gray = load_grayscale_cleaned_image(pic)
    firstImage = load_infrared_cleaned_image(pic)
    
    # Locating the brightest pixel in the image
    (minVal,maxVal,minLoc,maxLoc) = cv2.minMaxLoc(gray)
    
    # Drawing the circle around the brightest pixel
    cv2.circle(firstImage, maxLoc, 25, (0,255,0),1)
    
    # Showing the image
    cv2.imshow("Naive",firstImage)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    #return firstImage


# In[4]:


# Test 1
i=0
while i < 7:    
    findDroneNaive(i)
    i+=1


# In[6]:


# This is the Robust function. ideally this function finds the brightest region in the picture. Still needs some fine 
# tuning but overall works better than the Naive function with a 90% accuracy rate on the same photos
def findDroneRobust(picNumber):
    
    # Loading the images
    gray = load_grayscale_cleaned_image(picNumber)
    #orig = load_infrared_cleaned_image(picNumber)
    
    # Implementing the Gaussian Blur which causes the computer to look at the birghtest regions of the image rather than 
    # the single brightest pixel. 
    gray2 = cv2.GaussianBlur(gray, (3, 3), 0)
    
    # Finding the brightest region
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray2)
    image = orig.copy()
    
    # Drawing the circle
    cv2.circle(image,maxLoc, 25, (100,255,100), 2)
    
    # Showing the circle
    cv2.imshow("Robust", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    #this = image
    #return(this)


# In[8]:


# Test Two
i = 0 
while i < 7:
    cv2.imshow("this", findDroneRobust(i))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    i+=1


# In[12]:


# Test 2 
i=0
while i < 7:    
    findDroneNaive(i)
    i+=1


# In[22]:


# Here we create two lists that we will run our smoothing algoritm on. "B" does not stand for anything in particular. 
Brow = []
Bcol = []
for i in range(0,500):
    # Here we have to me sure that the findDroneRobust() function returns the maxLoc variable. It cannot return the image
    Brow.append(findDroneRobust(i)[0])
    Bcol.append(findDroneRobust(i)[1])
    


# In[23]:


# Once we have these two lists we can run the smoothing algorithm.
# The algorithm essentially states that if the maxLoc value moves more than 10 pixels in one frame it should disregard
# that value and replace it with the average of the last three values. 
for i in range(0,500):
    if i > 3 and abs(Brow[i] - Brow[i-1]) > 10:
        Brow[i] = (Brow[i-1] + Brow[i-2]+Brow[i-3])/3
    Brow[i] = int(Brow[i])
    if i > 3 and abs(Bcol[i] - Bcol[i-1]) > 10:
        Bcol[i] = (Bcol[i-1] + Bcol[i-2]+Bcol[i-3])/3
    Bcol[i] = int(Bcol[i])


# In[24]:


# Creating the folder to hold all of the edited pictures (with the drone detected) 
# Keep in mind when you run this you will create a folder on your computer of 500 images
for i in range(0,500):
    edited_image = cv2.circle(load_infrared_cleaned_image(i),(Brow[i],Bcol[i]), 25, (100,255,100), 2)
    
    # This particular line will have to be changed for each computer that the code is run on
    output_folder = r"C:\Users\bbrec\Downloads\test2\\"
    output_filename = str(i) +'.bmp'

    output_path = output_folder+output_filename
    cv2.imwrite(output_path,edited_image)


# In[99]:


# Since the previous cell does not upload the images in chronological order we need to sort them with this cell.
i=0
pre_img_sort = []
while i < 500:
    pre_img_sort.append(str(i)+'.bmp')
    i+=1


# In[100]:


# Creating the  video 

# These two line will also be dependant upon the user's unique computer. 
path = r"C:\Users\bbrec\Downloads\test2\\"
video_ouput = r"C:\Users\bbrec\Downloads\\" + 'FinalVideo.mp4'

# not sure if this is necessary
pre_img = os.listdir(path)

# This is the second part of sorting the list. It could possibly function on its own however 
# just to be safe we left the previous sorting cell of code. 
img = []
for i in pre_img_sort:
    i = path+i
    img.append(i)
    
# This is creating the ouput video
cv2_fourcc = cv2.VideoWriter_fourcc(*'mp4v')  
video = cv2.VideoWriter(video_ouput,cv2_fourcc,24,[700,600])

# This is adding all of the pictures to the video
for i in range(len(img)):
    video.write(cv2.imread(img[i]))
video.release()


# In[81]:


# This is the Robust function. ideally this function finds the brightest region in the picture. Still needs some fine 
# tuning but overall works better than the Naive function with a 90% accuracy rate on the same photos
def findDroneRobust2(picNumber):
    
    # Loading the images
    gray = load_grayscale_cleaned_image(picNumber)
    orig = load_infrared_cleaned_image(picNumber)
    
    # Implementing the Gaussian Blur which causes the computer to look at the birghtest regions of the image rather than 
    # the single brightest pixel. 
    gray2 = cv2.GaussianBlur(gray, (3, 3), 0)
    
    # Finding the brightest region
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray2)
    image = orig.copy()
    # Drawing the circle
    cv2.circle(image,(row[i],column[i]), 25, (100,255,100), 2)
    # Showing the circle
    #cv2.imshow("Robust", image)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()       
    
    return(image)


# In[2]:


# A few months later and I have decided to implemnt a Kalman filter into this script 
# The following code will showcase the necessary notes and explainations of the Kalman Filter in this program.


# In[ ]:


# 

