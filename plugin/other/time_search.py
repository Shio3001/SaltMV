import copy


class TimeSearch:
    def time_search(now_f, this_effect, effect_point_internal_id_time, number=None):  # 二分探索
        ef_po = list(effect_point_internal_id_time.values())

        left = 0
        right = len(ef_po) - 1

        if len(ef_po) == 1:
            return ef_po[0],  ef_po[0]  # 前地点と次地点あわせ

        effect_point_internal_id_time = sorted(effect_point_internal_id_time.items(), key=lambda x: x[1])

        ef_key = list(effect_point_internal_id_time.keys())
        ef_val = list(effect_point_internal_id_time.values())

        while left <= right:  # 2つ以上のあたい
            mid = (left + right) // 2
            if ef_val[mid] <= now_f < ef_val[mid + 1]:
                return ef_val[mid], ef_val[mid + 1]

            elif ef_val[mid] > now_f:  # 現在フレームより前地点がでかい場合
                left -= 1

            elif ef_val[mid + 1] <= now_f:  # 現在フレームより次地点がちいさい場合
                right += 1

        if number:
            return ef_key[left], ef_key[right]

        point_left = this_effect.effect_point_internal_id_point[ef_key[left]]
        point_right = this_effect.effect_point_internal_id_point[ef_key[right]]

        return copy.deepcopy(point_left, point_right)
