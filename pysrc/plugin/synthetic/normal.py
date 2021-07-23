# 通常
class Synthetic:
    def __init__(self):
        self.name = "通常"

    def main(self, source, additions):

        RGB_draw = source

        for i in range(3):  # RGB
            #RGB_draw[:, :, i] = (additions[:, :, i] - source[:, :, i]) * (additions[:, :, 3] / 255)
            RGB_draw[i] = (additions[i] - source[i]) * (additions[3] / 255)
            # print(len(RGB_draw))

        source[0:3] += RGB_draw[0:3]

        # print(source)

        return source
