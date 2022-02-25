import cv2
import numpy as np
import copy
import scipy.fftpack

# reading gray image
img = cv2.imread ("D:\sem -7\Digital Image Processing\DIP LAB\lenna.png", 0)

image_array = np.zeros( [len(img), len(img[0])], dtype = int)

def zigzag(quantized):

    vector = np.zeros( [len(quantized)* len(quantized[0])], dtype = int )
    i = 0
    j = 0
    vector[0] = quantized[i][j]
    k=1
    j+=1
    while(k < len(quantized)* len(quantized[0])):

        while i < len(quantized) and j >= 0:
            vector[k] = quantized[i][j]
            k+=1
            j-=1
            i+=1
        
        j+=1
        i-=1

        if i == len(quantized) -1:
            j+=1
        else:
            i+=1

        while j < len(quantized[0]) and i >= 0:
            vector[k] = quantized[i][j]
            k+=1
            i-=1
            j+=1
        i+=1
        j-=1

        if j == len(quantized[0]) -1:
            i+=1
        else:
            j+=1
    
    return vector

def reversezigzag(vector):

    quantized= np.zeros( [8,8], dtype = int )
    i = 0
    j = 0
    quantized[i][j] = vector[0]
    k=1
    j+=1
    while(k < len(vector)):

        while i < len(quantized) and j >= 0:
            quantized[i][j] = vector[k]
            k+=1
            j-=1
            i+=1
        
        j+=1
        i-=1

        if i == len(quantized) -1:
            j+=1
        else:
            i+=1

        while j < len(quantized[0]) and i >= 0:
            quantized[i][j] = vector[k]
            k+=1
            i-=1
            j+=1
        i+=1
        j-=1

        if j == len(quantized[0]) -1:
            i+=1
        else:
            j+=1
    
    return quantized       

#centralizing image pixels //img is of type uint8 so converted it to int first
image_array = img.astype(int) - 128

# quantization_Array = np.ones([8,8], dtype = int)
quantization_Array = np.array([[16, 11, 10, 16, 24, 40, 51, 61], 
                            [12, 12, 14, 19, 26, 58, 60, 55], 
                            [14, 13, 16, 24, 40, 57, 69, 56], 
                            [14, 17, 22, 29, 51, 87, 80, 62], 
                            [18, 22, 37, 56, 68, 109, 103, 77], 
                            [24, 35, 55, 64, 81, 104, 113, 92], 
                            [49, 64, 78, 87, 103, 121, 120, 101], 
                            [72, 92, 95, 98, 112, 100, 103, 99]])

img_string = ''

# taking 8x8 blocks of img
for i in range(8,len(img)+1, 8):
    for j in range(8,len(img[0])+1, 8):

        # dct transfomation (method for matrix)
        dct_transform = scipy.fftpack.dct( scipy.fftpack.dct( image_array[i-8:i, j-8:j].T, norm='ortho' ).T, norm='ortho' )

        # quantization
        quantized = np.divide(dct_transform, quantization_Array)

        # rounding float numpy matrix (rounding gives better result than converting to int)
        quantized = np.round_(quantized) 

        # zig zag traversal
        vector = zigzag(quantized)

        #run length encoding
        count = 1
        previous_pixel = vector[0]
        for idx in range(1,len(vector)):

            if previous_pixel != vector[idx]:
                img_string += '('+ str(previous_pixel) + ',' + str(count) +')'
                count = 1
                previous_pixel = vector[idx]
            else:
                count += 1
        img_string += '('+ str(previous_pixel) + ',' + str(count) +')'

# decode

# to store final image
decoded_img = np.zeros( [len(img), len(img[0])], dtype = int)
idx = 0 # to keep track of img_string

# decoding
for i in range(8,len(img)+1, 8):
    for j in range(8,len(img[0])+1, 8):

        # to open rle into 1 d vector
        vector = np.zeros( [64], dtype =int)
        cnt = 0
        datum = ''
        for ch in img_string[idx:]:
            idx += 1
            if ch == ')':
                pixel = int(datum.split(',')[0])
                count = int(datum.split(',')[1])
                datum = ''

                for x in range(count):
                    vector[cnt] = pixel
                    cnt +=1

            elif ch != '(':
                datum += ch

            # to break from for loop after taking 64 pixels
            if cnt == 64 :
                break

        # reading zigzag vector to 2d vector
        quantized = reversezigzag(vector)
    
        # multiplying with quantization array
        multiplied = np.multiply(quantized, quantization_Array)
        
        # applying inverse dct
        idct_transform = scipy.fftpack.idct( scipy.fftpack.idct(multiplied.T, norm='ortho' ).T, norm='ortho' )

        # storing idct resut into original image as integer
        decoded_img[i-8:i, j-8:j] = idct_transform.astype(int)

# decentralizing array
decoded_img += 128

# converting to uint8 for display
decoded_img = decoded_img.astype(np.uint8)

cv2.imshow("Original Image",img)
cv2.imshow("Rebuilt Image",decoded_img)
cv2.waitKey(0)