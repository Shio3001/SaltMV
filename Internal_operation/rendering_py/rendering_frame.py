import copy


class Rendering:
    def __init__(self):
        self.now_f = 0
        self.operation = {}
        self.editor = {}
        self.effect_point_default_keys = None

    def main(self, draw_base, operation, this_scene, now_frame, effect_point_default_keys):  # 必要なもの
        self.effect_point_default_keys = effect_point_default_keys
        self.now_f = now_frame
        self.operation = operation
        self.time_search = self.operation["plugin"]["other"]["time_search"].time_search
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

        for this_object in this_layer.object_group:
            draw_base = self.obj(this_object, draw_base)

        return draw_base

    def obj(self, this_object, draw_base):

        ed_size = [int(self.editor["x"]), int(self.editor["y"])]

        if this_object.installation[0] <= self.now_f < this_object.installation[1]:  # オブジェクト範囲外であれば返却
            return draw_base

        additions_point = [0, 0]
        source = copy.deepcopy(draw_base)
        additions = copy.deepcopy(draw_base)

        for this_effect in this_object.effect_group:
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

            if source_margin[1][i] > ed_size[i]:
                additions_margin[1][i] = ed_size[i] - source_margin[0][i]
                source_margin[1][i] = ed_size[i]

        input_draw = source[source_margin[0][1]:source_margin[1][1], source_margin[0][0]:source_margin[1][0]]
        additions_draw = additions[additions_margin[0][1]:additions_margin[1][1], additions_margin[0][0]:additions_margin[1][0]]

        # print(input_draw.shape)
        output_draw = self.operation["plugin"]["synthetic"][this_object.synthetic].main(input_draw, additions_draw)
        source[source_margin[0][1]:source_margin[1][1], source_margin[0][0]:source_margin[1][0]] = output_draw

        return source

    def effect(self, this_effect, draw_base):
        # 二分探索すればいいよ <timeによる配列と配列の間位をさがす>

        before_point, next_point = self.time_search(self.now_f, this_effect)
        now_point = self.operation["rendering_py"]["point"].main(before_point, next_point, self.now_f, self.effect_point_default_keys)

        effect_send = EffectPluginElements(draw_base, now_point, before_point, next_point, self.now_f, self.editor, self.operation)
        draw_base, draw_point = this_effect.procedure(effect_send)

        return draw_base, draw_point

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
