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
        for this_effect in this_objct.effect_group:
            draw_base = self.obj(this_effect, draw_base)
        return draw_base

    def effect(self, this_effect, draw_base):
        return draw_base
