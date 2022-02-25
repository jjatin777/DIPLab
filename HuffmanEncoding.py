import numpy as np
import cv2

class PriorityQueue:

    def __init__(self, value, elements):
        self.value = value
        self.elements = elements
        self.left = None
        self.right = None

    def put(self, value, elements):
        if self.value >= value:
            if self.left == None:
                self.left = PriorityQueue(value, elements)
            else:
                self.left.put(value, elements)
        else:
            if self.right == None:
                self.right = PriorityQueue(value, elements)
            else:
                self.right.put(value, elements)
    
    def get(self):
        if self.left == None and self.right == None:
            ret = [self.value, self.elements,1]
            return ret
            
        elif self.left == None:
            ret = [self.value, self.elements,2]
            return ret
        
        else:
            obj = self.left.get()
            if obj[2] == 1:
                self.left = None
            if obj[2] == 2:
                self.left = self.left.right
            obj[2] = 0
            return obj

        
# img = [[3,3,3,2],[2,3,3,3],[3,2,2,2],[2,1,1,0]]
# # img = [[169, 169, 168, 175, 162,138], [169, 169, 168, 175, 162,138], [169, 169, 168, 175, 162,138]]
img = cv2.imread ("D:/sem -7/Digital Image Processing/DIP LAB/lenna.png",0)

prob = {}
symbol_table = {}
reverse_symbol_table = {}

#count occurrence of element in image array
for row in img:
    for element in row:
        if element in prob:
            prob[element] += 1
        else:
            prob[element] = 1
            symbol_table[element] =''
# print("Probabilities")
# print(prob)

#enter values in priority_queue
q = None
for key,value in prob.items():
    if q == None:
       q = PriorityQueue(value, {key})
    else:
        q.put(value, {key})

#create huffman tree and assign values in reverse
while 1:
    item_a = q.get()
    if item_a[2] == 2:
        q = q.right

    #No more elements left
    if item_a[2] == 1:
        break

    item_b = q.get()
    if item_b[2] == 2:
        q = q.right

    for element in item_a[1]:
        symbol_table[element]+='1'

    for element in item_b[1]:
        symbol_table[element]+='0'
    
    #No more elements left
    if item_b[2] == 1:
        break

    q.put(item_a[0] + item_b[0], item_a[1].union(item_b[1]))

#reverse the assigned valued to get in correct format
for key,value in symbol_table.items():
    symbol_table[key] = value[::-1]


#calcuating number of bits required per pixel
sum = 0
mx = 0
print("\nSymbol table")
for key,value in symbol_table.items():
    reverse_symbol_table[value] = key
    sum += prob[key] * len(value)
    if mx < len(value):
        mx = len(value)

print("\nBits per pixel")
print(sum/(len(img)*len(img[0])))
print(mx)



#encode
image_string = ''
for row in img:
    for element in row:
        image_string += symbol_table[element]


#decode
image_array = np.zeros( len(img)* len(img[0]), dtype = np.uint8)
i = 0
symbol = ''

for ch in image_string:
    symbol += ch

    if symbol in reverse_symbol_table:
        image_array[i] = reverse_symbol_table[symbol]
        symbol = ''
        i += 1
    
    if len(symbol) > mx:
        break

image_array = image_array.reshape(len(img), len(img[0]))
cv2.imshow("Original Image",img)
cv2.imshow("Rebuilt Image",image_array)
cv2.waitKey(0)
print(image_array)