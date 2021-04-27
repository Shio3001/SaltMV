import cv2
import numpy as np


in_data = cv2.imread("IMG_5796.jpg")

a = 128


in_data2 = cv2.cvtColor(in_data, cv2.COLOR_BGR2GRAY)
print(in_data2.shape)

in_data_bool = (in_data2 > a) * 255

print(in_data)

print(type(in_data_bool))
print(in_data_bool)
# np.array(map(int, input().rsplit()))
out = cv2.cvtColor(in_data_bool.astype('uint8'), cv2.COLOR_RGBA2BGR)
cv2.imwrite("nya_n.png", out)
# cv2.imshow("frame", out)
