import numpy as np
import cv2

img = cv2.imread ("D:/sem -7/Digital Image Processing/DIP LAB/lenna.png",0)


#run length encoding
img_string = ''

for line_no in range(len(img)):
    new_line = 0
    count = 0
    previous_pixel = 0
    for idx in range(len(img[0])):
        if new_line == 0:
            new_line =1
            previous_pixel = img[line_no][idx]
            count = 1
        
        elif previous_pixel != img[line_no][idx]:
            img_string += '('+ str(previous_pixel) + ',' + str(count) +')'
            count = 1
            previous_pixel = img[line_no][idx]

        else:
            count += 1

    img_string += '('+ str(previous_pixel) + ',' + str(count) +')'

print("length of image string", len(img_string))


#decode
image_array = np.zeros( len(img)* len(img[0]), dtype = np.uint8)
i = 0
datum = ''
for ch in img_string:

    if ch == ')':
        pixel = int(datum.split(',')[0])
        count = int(datum.split(',')[1])
        datum = ''

        for x in range(count):
            image_array[i] = pixel
            i+=1

    elif ch != '(':
        datum += ch

image_array = image_array.reshape(len(img), len(img[0]))
cv2.imshow("Original Image",img)
cv2.imshow("Rebuilt Image",image_array)
cv2.waitKey(0)
print(image_array)