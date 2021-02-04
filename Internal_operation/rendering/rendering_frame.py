class Rendering:
    def __init__(self):
        self.now_f = 0
        self.operation = {}

    def main(self, draw_base, operation, this_scene, now_frame):  # 必要なもの
        self.now_f = now_frame
        self.operation = operation

        self.scene(this_scene, draw_base)

        return draw_base

    def scene(self, this_scene, draw_base):
        for this_layer in this_scene.layer_group:
            self.layer(this_layer, draw_base)
        return draw_base

    def layer(self, this_layer, draw_base):
        for this_objct in this_layer.objct_group:
            draw_base = self.obj(this_objct, draw_base)
        return draw_base

    def obj(self, this_objct, draw_base):
        if this_objct.installation[0] <= self.now_f < this_objct.installation[1]:
            return draw_base

        for this_effect in this_objct.effect_group:
            draw_base = self.effect(this_effect, draw_base)
        return draw_base

    def effect(self, this_effect, draw_base):
        # 二分探索すればいいよ <timeによる配列と配列の間位をさがす>
        return draw_base

    def time_search(self):
        return


class EffectPluginElements:
    def __init__(self, draw, effect_value, now_frame, editor, operation, location):
        self.draw = draw
        self.effect_value = effect_value
        self.now_frame = now_frame
        self.editor = editor
        self.operation = operation

        self.editor_size = {"x": self.editor[0], "y": self.editor[1]}
        self.draw_size = {"x": self.draw.shape[1], "y": self.draw.shape[0]}
        self.location = location
