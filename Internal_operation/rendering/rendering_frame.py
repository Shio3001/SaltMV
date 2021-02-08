import copy


class Rendering:
    def __init__(self):
        self.now_f = 0
        self.operation = {}
        self.editor = {}

    def main(self, draw_base, operation, this_scene, now_frame):  # 必要なもの
        self.now_f = now_frame
        self.operation = operation
        # print(draw_base.shape, self.now_f)
        draw_base = self.scene(this_scene, draw_base)
        # print(draw_base.shape)

        return draw_base

    def scene(self, this_scene, draw_base):
        self.editor = this_scene.editor
        for this_layer in this_scene.layer_group:
            draw_base = self.layer(this_layer, draw_base)
        return draw_base

    def layer(self, this_layer, draw_base):

        for this_objct in this_layer.object_group:
            draw_base = self.obj(this_objct, draw_base)

        return draw_base

    def obj(self, this_objct, draw_base):

        ed_size = [int(self.editor["x"]), int(self.editor["y"])]

        if this_objct.installation[0] <= self.now_f < this_objct.installation[1]:  # オブジェクト範囲外であれば返却
            return draw_base

        additions_point = [0, 0]
        source = copy.deepcopy(draw_base)
        additions = copy.deepcopy(draw_base)

        for this_effect in this_objct.effect_group:
            additions, ef_additions_point = self.effect(this_effect, additions)
            additions_point = [d + r for d, r in zip(additions_point, ef_additions_point)]

        # ここより上は座標中心区域
        confirm_point = self.center_to_upper_left(additions_point, ed_size)

        additions_size = [additions.shape[1], additions.shape[0]]

        source_margin = [[], []]  # エディター全体に対する希望範囲
        additions_margin = [[], []]  # 追加描画範囲に対する希望範囲

        source_margin[0] = confirm_point
        source_margin[1] = [int(c + a) for c, a in zip(confirm_point, additions_size)]

        additions_margin[0] = [0, 0]
        additions_margin[1] = additions_size

        for i in range(2):
            if source_margin[0][i] < 0:
                additions_margin[0][i] = abs(source_margin[0][i])
                source_margin[0][i] = 0

                # print("加算")

            if source_margin[1][i] > ed_size[i]:
                additions_margin[1][i] = ed_size[i] - source_margin[0][i]
                source_margin[1][i] = ed_size[i]

                # print("減算")

            #source_margin[:][i] = additions_margin[:][i]

        #print(source_margin, additions_margin)

        input_draw = source[source_margin[0][1]:source_margin[1][1], source_margin[0][0]:source_margin[1][0]]
        additions_draw = additions[additions_margin[0][1]:additions_margin[1][1], additions_margin[0][0]:additions_margin[1][0]]

        # print(input_draw.shape)
        output_draw = self.operation["plugin"]["synthetic"][this_objct.synthetic].main(input_draw, additions_draw)
        source[source_margin[0][1]:source_margin[1][1], source_margin[0][0]:source_margin[1][0]] = output_draw

        return source

    def effect(self, this_effect, draw_base):
        # 二分探索すればいいよ <timeによる配列と配列の間位をさがす>

        before_point, next_point = copy.deepcopy(self.time_search(this_effect))
        now_point = self.operation["rendering"]["point"].main(before_point, next_point, self.now_f)

        effect_send = EffectPluginElements(draw_base, now_point, before_point, next_point, self.now_f, self.editor, self.operation)
        draw_base, draw_point = this_effect.procedure(effect_send)

        return draw_base, draw_point

    def time_search(self, this_effect):  # 二分探索
        left = 0
        right = len(this_effect.effect_point) - 1

        if len(this_effect.effect_point) == 1:
            return this_effect.effect_point[0], this_effect.effect_point[0]  # 前地点と次地点あわせ

        while left <= right:  # 2つ以上のあたい
            mid = (left + right) // 2
            if this_effect.effect_point[mid] <= self.now_f < this_effect.effect_point[mid + 1]:
                return this_effect.effect_point[mid], this_effect.effect_point[mid + 1]

            elif this_effect.effect_point[mid] > self.now_f:  # 現在フレームより前地点がでかい場合
                left -= 1

            elif this_effect.effect_point[mid + 1] <= self.now_f:  # 現在フレームより次地点がちいさい場合
                right += 1

        return this_effect.effect_point[0], this_effect.effect_point[0]

    def center_to_upper_left(self, point, ed_size):

        point = [int(p + (e / 2)) for p, e in zip(point, ed_size)]
        return point


class EffectPluginElements:
    def __init__(self, draw, effect_value, before_value, next_value, now_frame, editor, operation):
        self.draw = draw

        self.effect_value = effect_value
        self.before_value = before_value
        self.next_value = next_value

        self.now_frame = now_frame
        self.editor = editor
        self.operation = operation

        # self.editor_size =
        self.draw_size = {"x": self.draw.shape[1], "y": self.draw.shape[0]}

        # self.location = location
