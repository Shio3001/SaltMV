# 通常
import numpy as np
import cv2


class Synthetic:
    def __init__(self):
        self.name = "通常"

    def main(self, source, additions):

        #cv2.imwrite('source.png', source.astype('uint8'))

        x_size = round(source.shape[1])
        y_size = round(source.shape[0])

        np255 = np.full((y_size, x_size), 1)
        all_calculation = np.full((y_size, x_size, 4), 1)
        all_calculation = all_calculation.astype(np.float64)

        all_calculation[:, :, 3] = source[:, :, 3] * (np255 - additions[:, :, 3]) + additions[:, :, 3]

        for i in range(3):  # RGB

            all_calculation[:, :, i] = source[:, :, 3] * (np255 - additions[:, :, 3]) * source[:, :, i] + additions[:, :, 3] * additions[:, :, i]
            zero_distribution = np.where(all_calculation[:, :, 3] == 0, 1, 0)

            for_division = all_calculation[:, :, 3] + zero_distribution
            #for_division = for_division.astype(np.uint8)

            #print("for_division", for_division)
            #print("all_calculation", all_calculation[:, :, i])

            all_calculation[:, :, i] /= for_division

            # all_calculation[:, :, i] =

            #RGB_draw[:, :, i] = (additions[:, :, i] - source[:, :, i]) * (additions[:, :, 3] / 255)
            #RGB_draw[:, :, i] = (additions[:, :, i] - source[:, :, i]) * (additions[:, :, 3] / 255)
            # print(len(RGB_draw))

            #source[:, :, 0:3] += RGB_draw[:, :, 0:3]

            # print(source)

        # print(all_calculation)

        #cv2.imwrite('all_calculation.png', all_calculation.astype('uint8'))
        #cv2.imwrite('additions.png', additions.astype('uint8'))

        return all_calculation

# C=αfCr+(1−αf)Cb
# https://odashi.hatenablog.com/entry/20110921/1316610121
