
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