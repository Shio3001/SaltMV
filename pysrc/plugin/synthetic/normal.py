# 通常
import numpy as np


class Synthetic:
    def __init__(self):
        self.name = "通常"

    def main(self, source, additions):

        x_size = round(source.shape[1])
        y_size = round(source.shape[0])

        one_np = np.ones((y_size, x_size))
        all_calculation = np.ones((y_size, x_size, 4))

        all_calculation[:, :, 3] = source[:, :, 3] * (one_np - additions[:, :, 3]) + additions[:, :, 3]

        for i in range(3):  # RGB

            all_calculation[:, :, i] = (source[:, :, 3] * (one_np - additions[:, :, 3]) * source[:, :, i] + additions[:, :, 3] * additions[:, :, i])
            all_calculation[:, :, i] /= all_calculation[:, :, 3]

            #RGB_draw[:, :, i] = (additions[:, :, i] - source[:, :, i]) * (additions[:, :, 3] / 255)
            #RGB_draw[:, :, i] = (additions[:, :, i] - source[:, :, i]) * (additions[:, :, 3] / 255)
            # print(len(RGB_draw))

            #source[:, :, 0:3] += RGB_draw[:, :, 0:3]

            # print(source)

        return all_calculation
