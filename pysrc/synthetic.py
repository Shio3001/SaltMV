class SyntheticControl:
    def __init__(self):
        pass

    def set_operation(self, operation):
        self.operation = operation

    def call(self, synthetic_name, base, add, base_draw_range_lu, base_draw_range_rd, add_draw_range_lu, add_draw_range_rd):

        base_left = base_draw_range_lu[0]
        base_up = base_draw_range_lu[1]

        base_right = base_draw_range_rd[0]
        base_down = base_draw_range_rd[1]

        add_left = add_draw_range_lu[0]
        add_up = add_draw_range_lu[1]

        add_right = add_draw_range_rd[0]
        add_down = add_draw_range_rd[1]

        size_x = add_down - add_up
        size_y = add_right - add_left

        if size_x < 0:
            return base

        if size_y < 0:
            return base

        base_section = base[base_up:base_down, base_left:base_right]
        add_section = add[add_up:add_down, add_left:add_right]

        base[base_up:base_down, base_left:base_right] = self.operation["plugin"]["synthetic"][synthetic_name].main(base_section, add_section)  # source, additions
        return base
