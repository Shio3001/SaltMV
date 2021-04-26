import copy


class CallBack:
    def __init__(self, data):
        data.scroll_event = None
        data.scroll_sta_event = None
        data.scroll_end_event = None

        def ratio_f_pos_edit():
            ratio_data = RatioData(data.pxf.ratio_f, data.pxf.sta_end_f)

            return ratio_data

        def set_scroll_event(func):  # コールバック設定
            data.scroll_event = func
            ratio = ratio_f_pos_edit()
            data.scroll_event(ratio)

        def set_scroll_sta_event(func):  # コールバック設定
            data.scroll_sta_event = func
            ratio = ratio_f_pos_edit()
            data.scroll_sta_event(ratio)

        def set_scroll_end_event(func):  # コールバック設定
            data.scroll_end_event = func
            ratio = ratio_f_pos_edit()
            data.scroll_end_event(ratio)

        data.set_scroll_event = set_scroll_event  # コールバック初期設定
        data.set_scroll_event(data.event_not_func)  # とりあえずdata.event_not_func : テスト関数をぶちこむ

        data.set_scroll_sta_event = set_scroll_sta_event  # コールバック初期設定
        data.set_scroll_sta_event(data.event_not_func)

        data.set_scroll_end_event = set_scroll_end_event  # コールバック初期設定
        data.set_scroll_end_event(data.event_not_func)

        def run_scroll_event():
            if not str(type(data.scroll_event)) == "<class 'function'>":
                return
            ratio = ratio_f_pos_edit()
            data.scroll_event(ratio)

        def run_scroll_sta_event():
            if not str(type(data.scroll_event)) == "<class 'function'>":
                return
            ratio = ratio_f_pos_edit()
            data.scroll_sta_event(ratio)

        def run_scroll_end_event():
            if not str(type(data.scroll_event)) == "<class 'function'>":
                return
            ratio = ratio_f_pos_edit()
            data.scroll_end_event(ratio)

        data.run_scroll_event = run_scroll_event
        data.run_scroll_sta_event = run_scroll_sta_event
        data.run_scroll_end_event = run_scroll_end_event


class RatioData:
    def __init__(self, ratio_f, sta_end_f):
        self.ratio_f = copy.deepcopy(ratio_f)
        self.sta_end_f = copy.deepcopy(sta_end_f)
