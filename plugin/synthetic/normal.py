# 通常
class Synthetic:
    def __init__(self):
        self.name = "通常"

    def main(self, synthesis_target, draw):

        RGB_draw = synthesis_target

        for i in range(3):  # RGB
            #print(RGB_draw[i].shape, synthesis_target[:, :, i].shape, draw[:, :, i].shape, draw[:, :, 3].shape)
            RGB_draw[:, :, i] = (draw[:, :, i] - synthesis_target[:, :, i]) * (draw[:, :, 3] / 255)
            # print(len(RGB_draw))

        synthesis_target[0:3] += RGB_draw[0:3]

        return synthesis_target
