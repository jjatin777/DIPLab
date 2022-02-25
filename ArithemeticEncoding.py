import numpy as np
import cv2

# img = [[0,0,1],[1,2,2],[3,4,5]]
img = [[169, 169, 168, 175, 162,138], [169, 169, 168, 175, 162,138], [169, 169, 168, 175, 162,138]]
# img = cv2.imread ("D:/sem -7/Digital Image Processing/DIP LAB/lenna.png",0)

no_of_pixel = len(img[0]) *len(img)
prob = {}

#count occurrence of element in image array
for row in img:
    for element in row:
        if element in prob:
            prob[element] += 1
        else:
            prob[element] = 1

prev = 0
for key,val in prob.items():
    prob[key] = [prev, prev+(val/no_of_pixel)]
    prev += (val/no_of_pixel)



# encode
# prob = {}
# prob['a'] = [0.0, 0.4]
# prob['b'] = [0.4, 0.6]
# prob['c'] = [0.6,0.7]
# prob['d'] = [0.7,1.0]

low = 0.0
high = 1.0
# img = [['d'],['a'],['d']]

for row in img:
    for element in row:
        range = high - low

        high = low + range* prob[element][1]
        low = low + range* prob[element][0]

tag_val = (high+low)/2


# decode

length = len(img)*len(img[0])
image_array = np.zeros( len(img)* len(img[0]), dtype = np.uint8)
i = 0

while(length) :
    length -= 1
    for key, val in prob.items():

        if tag_val > val[0] and tag_val < val[1]:
            tag_val = (tag_val - val[0]) / (val[1] - val[0])
            image_array[i] = key
            i+=1
            break


image_array = image_array.reshape(len(img), len(img[0]))
print("original array")
print(img)
# cv2.imshow("Rebuilt Image",image_array)
# cv2.waitKey(0)
print("Rebuild Array")
print(image_array)
    


