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

        base_float64 = base.astype('float64')
        add_float64 = add.astype('float64')

        base_section = base_float64[base_up:base_down, base_left:base_right] / 255
        add_section = add_float64[add_up:add_down, add_left:add_right] / 255

        process = self.operation["plugin"]["synthetic"][synthetic_name].main(base_section, add_section)  # source, additions
        process[:, :, 0:3] *= 255
        process_uint8 = process.astype('uint8')

        base[base_up:base_down, base_left:base_right] = process_uint8

        return base
