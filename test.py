
import matplotlib.pyplot as plt

import numpy as np


def BezierFunction(t, xy1, xy2, xy3, xy4):

    tp = 1 - t
    bezier_result = tp * tp * tp * xy1 + 3 * tp * tp * t * xy2 + 3 * tp * t*t * xy3 + pow(t, 3) * xy4
    return bezier_result


x1 = 0
x2 = 1

y1 = 0
y2 = 1

rate = 1

arr0 = np.array([i/100 for i in range(0, 100)])
arr1 = np.array([BezierFunction(i/100, 0, x1, x2, 1) for i in range(0, 100)])
arr2 = np.array([BezierFunction(i/100, 0, y1, y2, 1) for i in range(0, 100)])
print(round(arr0 * 100))
print(round(arr1 * 100))
print(round(arr2 * 100))

plt.plot(arr0, arr1)
plt.plot(arr0, arr2)
plt.plot(arr1, arr2)

plt.show()
