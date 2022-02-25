import cv2
import copy
import matplotlib.pyplot as plt


#Read Image
img = cv2.imread ("D:\sem -7\Digital Image Processing\DIP LAB\Einstein.jpg",1)
# print(img.shape)
# print(len(img))
cv2.imshow("Normal Image", img)
cv2.waitKey(20000)
cv2.destroyAllWindows()

# channel = copy.deepcopy(img)
# for x in range(len(img)):
#     for y in range(len(img[x])):
#         for z in range(len(img[x][y])):
#             if(z == 0 or z == 1):
#                 channel[x][y][z] = 0


# cv2.imshow("channel Image", channel)
# cv2.waitKey(2000)
# cv2.destroyAllWindows()


#Negative Image

negative = copy.deepcopy(img)
for x in range(len(img)):
    for y in range(len(img[x])):
        for z in range(len(img[x][y])):
            negative[x][y][z] = 255 - negative[x][y][z]


cv2.imshow("Normal Image", img)
cv2.imshow("Negative Image", negative)
cv2.waitKey(20000)
cv2.destroyAllWindows()


#histogram
x_plt = [y for y in range(256)]
y_plt = [0  for y in range(256)]

for x in range(len(img)):
    for y in range(len(img[x])):
            y_plt[negative[x][y][0]] += 1 # REd


plt.bar(x_plt,y_plt,align='center')
plt.xlabel('Bins')
plt.ylabel('Frequency')
plt.show()

