import cv2
import copy
import numpy as np
import math



def Box_filter(img):

    box_array = np.zeros([img.shape[0]+2, img.shape[1]+2], dtype = int)

    for i in range(1,img.shape[0]+1):
        for j in range(1,img.shape[1]+1):
            box_array[i][j] = img[i-1][j-1]


    box_filter = copy.deepcopy(img)

    for i in range(1,box_array.shape[0]-1):
        for j in range(1,box_array.shape[1]-1):
            box_filter[i-1][j-1] = (box_array[i-1][j-1] + box_array[i-1][j] + box_array[i-1][j+1] + box_array[i][j-1] + box_array[i][j] + box_array[i][j+1] + box_array[i+1][j-1] + box_array[i+1][j] + box_array[i+1][j+1]) / 9

    cv2.imshow("Original image",img)
    cv2.imshow("BOX FILTER", box_filter)
    cv2.waitKey(0)

def Median_filter(img):

    array = np.zeros([img.shape[0]+2, img.shape[1]+2], dtype = int)

   
    for i in range(1,img.shape[0]+1):
        for j in range(1,img.shape[1]+1):
            array[i][j] = img[i-1][j-1]

    for j in range(1,img.shape[1]+1):
        array[0][j] = img[0][j-1]
    
    for j in range(1,img.shape[1]+1):
        array[img.shape[0]+1][j] = img[img.shape[0]-1][j-1]

    for i in range(1,img.shape[0]+1):
        array[i][0] = img[i-1][0]
    
    for i in range(1,img.shape[0]+1):
        array[i][img.shape[1]+1] = img[i-1][img.shape[1]-1]

    filter = copy.deepcopy(img)

    for i in range(1,array.shape[0]-1):
        for j in range(1,array.shape[1]-1):
            temp = [array[i-1][j-1], array[i-1][j], array[i-1][j+1], array[i][j-1], array[i][j], array[i][j+1], array[i+1][j-1], array[i+1][j], array[i+1][j+1]]
            temp = sorted(temp)
            filter[i-1][j-1] = temp[4]

    cv2.imshow("Original image",img)
    cv2.imshow("MEDIAN FILTER", filter)
    cv2.waitKey(0)

def Min_filter(img):

    array = np.zeros([img.shape[0]+2, img.shape[1]+2], dtype = int)

   
    for i in range(1,img.shape[0]+1):
        for j in range(1,img.shape[1]+1):
            array[i][j] = img[i-1][j-1]

    for j in range(1,img.shape[1]+1):
        array[0][j] = img[0][j-1]
    
    for j in range(1,img.shape[1]+1):
        array[img.shape[0]+1][j] = img[img.shape[0]-1][j-1]

    for i in range(1,img.shape[0]+1):
        array[i][0] = img[i-1][0]
    
    for i in range(1,img.shape[0]+1):
        array[i][img.shape[1]+1] = img[i-1][img.shape[1]-1]

    filter = copy.deepcopy(img)

    for i in range(1,array.shape[0]-1):
        for j in range(1,array.shape[1]-1):
            temp = [array[i-1][j-1], array[i-1][j], array[i-1][j+1], array[i][j-1], array[i][j], array[i][j+1], array[i+1][j-1], array[i+1][j], array[i+1][j+1]]
            filter[i-1][j-1] = min(temp)

    cv2.imshow("Original image",img)
    cv2.imshow("MIN FILTER", filter)
    cv2.waitKey(0)

def Max_filter(img):

    array = np.zeros([img.shape[0]+2, img.shape[1]+2], dtype = int)

   
    for i in range(1,img.shape[0]+1):
        for j in range(1,img.shape[1]+1):
            array[i][j] = img[i-1][j-1]

    for j in range(1,img.shape[1]+1):
        array[0][j] = img[0][j-1]
    
    for j in range(1,img.shape[1]+1):
        array[img.shape[0]+1][j] = img[img.shape[0]-1][j-1]

    for i in range(1,img.shape[0]+1):
        array[i][0] = img[i-1][0]
    
    for i in range(1,img.shape[0]+1):
        array[i][img.shape[1]+1] = img[i-1][img.shape[1]-1]

    filter = copy.deepcopy(img)

    for i in range(1,array.shape[0]-1):
        for j in range(1,array.shape[1]-1):
            temp = [array[i-1][j-1], array[i-1][j], array[i-1][j+1], array[i][j-1], array[i][j], array[i][j+1], array[i+1][j-1], array[i+1][j], array[i+1][j+1]]
            filter[i-1][j-1] = max(temp)

    cv2.imshow("Original image",img)
    cv2.imshow("MAX FILTER", filter)
    cv2.waitKey(0)

def Gaussian_filter(img):

    w = np.array([[4, 8, 4],
                [8, 16, 8],
                [4, 8, 4]], dtype = np.int16)
    div = 1  #sum of values in kernal
    

    array = np.pad(img, pad_width = ((1,1),(1,1)), mode = 'reflect')

    filter = np.full(img.shape,255, dtype = np.uint16)
    # print(img)
    for i in range(1,array.shape[0]-1):
        for j in range(1,array.shape[1]-1):
            filter[i-1][j-1] = np.sum(array[i-1:i+2, j-1:j+2] * w) / div
            # print(filter[i-1][j-1], np.sum(array[i-1:i+2, j-1:j+2] * w), (np.sum(array[i-1:i+2, j-1:j+2] * w)&255))

    # print(filter)
    cv2.imshow("Original image",img)
    cv2.imshow("GAUSSIAN FILTER", filter)
    cv2.waitKey(0)

def Laplacian_filter(img):

    w = np.array([[0, -1, 0],
                [-1, 4, -1],
                [0, -1, 0]], dtype = np.int16)
    div = 16
    
    array = np.pad(img, pad_width = ((1,1),(1,1)), mode = 'reflect')

    filter = np.full(img.shape,255, dtype = np.uint8)
   
    for i in range(1,array.shape[0]-1):
        for j in range(1,array.shape[1]-1):
            filter[i-1][j-1] = np.sum(array[i-1:i+2, j-1:j+2] * w) / div

    cv2.imshow("Original image",img)
    cv2.imshow("LAPLACE FILTER", filter)
    cv2.waitKey(0)


# img = cv2.imread ("D:/sem -7/Digital Image Processing/DIP LAB/Einstein.jpg",0)
# Laplacian_filter(img)

# img = cv2.imread ("D:/sem -7/Digital Image Processing/DIP LAB/RAW5.tif",0)
# # Gaussian_filter(img)

# img = cv2.imread ("D:/sem -7/Digital Image Processing/DIP LAB/RAW4.tif",0)
# Box_filter(img)

# img = cv2.imread ("D:/sem -7/Digital Image Processing/DIP LAB/RAW3.tif",0)
# Max_filter(img)

# img = cv2.imread ("D:/sem -7/Digital Image Processing/DIP LAB/RAW4.tif",0)
# Median_filter(img)

img = cv2.imread ("D:/sem -7/Digital Image Processing/DIP LAB/RAW3.tif",0)
Min_filter(img)

