# coding:utf-8
import sys
import os
import copy


class InitialValue:
    def __init__(self):
        pass

    def main(self, elements):
        setting_effect = elements.effectElements()
        setting_effect.effectname = str(os.path.basename(__file__)).replace('.py', '')
        setting_effect.effectPoint = [{"time": 0, "speed": 1}]
        setting_effect.various_fixed = {}
        setting_effect.procedure = CentralRole()

        return setting_effect


class CentralRole:
    def __init__(self):

        self.direction = [1, 1]
        self.starting_point = [0, 0]

    def main(self, data):

        # editor_size = {"x": editor[0], "y": editor[1]}
        # draw_size = {"x": draw.shape[1], "y": draw.shape[0]}
        speed = data.position["speed"] - 1

        # self.direction = [d + speed if d < 0 else (speed * - 1) * d for d in self.direction]

        direction_range = [list(data.editor_size.values())[i] / 2 - list(data.draw_size.values())[i] / 2 for i in range(2)]

        speed_direction = [x + speed if x >= 0 else x + (speed * -1) for x in self.direction]

        for j in range(2):
            if -1 * direction_range[j] < speed_direction[j] + self.starting_point[j] < direction_range[j]:
                pass
            else:
                self.direction[j] *= -1
                speed_direction[j] *= -1

        # self.starting_point = [x + y for x, y in zip(self.starting_point, speed_direction)]
        self.starting_point = [self.starting_point[k] + speed_direction[k] for k in range(2)]
        return data.draw, self.starting_point
