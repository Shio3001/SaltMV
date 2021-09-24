import copy
import inspect


class parts:
    def UI_set(self, UI_auxiliary):

        UI_auxiliary.pxf = UI_auxiliary.plus_px_frame_data(direction=0, debug_name="bpm")
        UI_auxiliary.callback_operation = UI_auxiliary.operation["plugin"]["other"]["callback"].CallBack()

        # def draw(info):
        #     px_pos, _ = info
        #     # print("実際の描画発火")
        #     UI_auxiliary.edit_diagram_position("now", x=px_pos)
        #     UI_auxiliary.territory_draw()

        # UI_auxiliary.pxf.callback_operation.set_event("draw_func", draw)

        UI_auxiliary.pxf.init_set_sta_end_f(sta=0, end=100)
        UI_auxiliary.pxf.set_sta_end_f(sta=0, end=100)
        UI_auxiliary.pxf.set_sta_end_px(sta=0, end=100)
        UI_auxiliary.pxf.set_px_ratio(size=2)

        UI_auxiliary.bpm_shape_key = []

        def shortage_add(num):
            len_bpm_shape_key = len(UI_auxiliary.bpm_shape_key)
            now_add = num - len_bpm_shape_key

            for i in range(now_add):
                name = UI_auxiliary.make_id("bpm{0}".format(i))
                UI_auxiliary.new_diagram(name)
                UI_auxiliary.bpm_shape_key.append(name)

            UI_auxiliary.territory_draw()

        def over_del(num):
            len_bpm_shape_key = len(UI_auxiliary.bpm_shape_key)

            for i in range(num, len_bpm_shape_key):
                UI_auxiliary.del_diagram(UI_auxiliary.bpm_shape_key[i])

            UI_auxiliary.territory_draw()
            del UI_auxiliary.bpm_shape_key[num: len_bpm_shape_key]

        def judgement(num):
            len_bpm_shape_key = len(UI_auxiliary.bpm_shape_key)
            judgement_num = num - len_bpm_shape_key

            if judgement_num > 0:
                shortage_add(num)
            elif judgement_num < 0:
                over_del(num)

        UI_auxiliary.bpm_y_view_size = 50  # temp

        UI_auxiliary.set_bpm_fps = 0
        UI_auxiliary.set_bpm_bpm = 0

        def set_bpm(fps=None, bpm=None, bpm_y_view_size=None):

            if not fps is None:
                UI_auxiliary.set_bpm_fps = int(fps)
            if not bpm is None:
                UI_auxiliary.set_bpm_bpm = int(bpm)

            if UI_auxiliary.set_bpm_bpm == 0:
                judgement(0)
                return

            section = 60 * UI_auxiliary.set_bpm_fps / UI_auxiliary.set_bpm_bpm

            view_fps = UI_auxiliary.pxf.sta_end_f[1] - UI_auxiliary.pxf.sta_end_f[0]

            quantity = round(view_fps / section) + 1

            judgement(quantity)

            origin_point = int(UI_auxiliary.pxf.sta_end_f[0] - UI_auxiliary.pxf.sta_end_f_init[0])

            origin_point_quotient = origin_point // section
            #origin_point_mod = origin_point & section

            print("quantity", quantity)
            print("section", section)
            print("view_fps", view_fps)
            print("origin_point", origin_point)
            print("origin_point_quotient", origin_point_quotient)

            for i in range(quantity):
                name = UI_auxiliary.bpm_shape_key[i]
                set_px = UI_auxiliary.pxf.f_to_px(section * (i+1+origin_point_quotient))
                UI_auxiliary.edit_diagram_size(name, x=1)

                if not bpm_y_view_size is None:
                    UI_auxiliary.bpm_y_view_size = bpm_y_view_size

                UI_auxiliary.edit_diagram_size(name, y=UI_auxiliary.bpm_y_view_size)

                UI_auxiliary.edit_diagram_position(name, x=set_px, y=0)
                UI_auxiliary.edit_diagram_color(name, "#cccccc")

            # for i in range(quantity):
            #     set_px = UI_auxiliary.pxf.f_to_px(section * i + UI_auxiliary.pxf.sta_end_f[0])

            #     name = UI_auxiliary.make_id("bpm")

            #     UI_auxiliary.new_diagram(name)
            #     UI_auxiliary.edit_diagram_size(name, x=0, y=100)
            #     UI_auxiliary.edit_diagram_position(name, x=set_px, y=100)
            #     UI_auxiliary.edit_diagram_color(name, "#cccccc")

            UI_auxiliary.territory_draw()
            UI_auxiliary.territory_stack(False)

        UI_auxiliary.set_bpm = set_bpm

        return UI_auxiliary
