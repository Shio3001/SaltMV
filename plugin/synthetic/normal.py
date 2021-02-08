# 通常
class Synthetic:
    def __init__(self):
        self.name = "通常"

    def main(self, draw_base, draw, draw_range):

        synthesis_target = draw_base[draw_range[0][0]:draw_range[0][1], draw_range[1][0]:draw_range[1][1]]

        print(len(synthesis_target))

        for i in range(3):  # RGB
            RGB_draw = (draw[:, :, i] - synthesis_target[0:0:i]) * (draw[:, :, 3] / 255)
            print(len(RGB_draw))

        synthesis_target += RGB_draw

        draw_base[draw_range[0][0]:draw_range[0][1], draw_range[1][0]:draw_range[1][1]] = synthesis_target
        return draw_base
