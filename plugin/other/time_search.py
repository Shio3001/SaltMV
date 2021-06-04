import copy


class TimeSearch:
    def time_search(now_f, this_effect, effect_point_internal_id_time, number=None):  # 二分探索
        print("time_search", effect_point_internal_id_time)

        effect_point_internal_id_time_sort = dict(sorted(effect_point_internal_id_time.items(), key=lambda x: x[1]))

        print("time_search_sort", effect_point_internal_id_time_sort)

        ef_key = list(effect_point_internal_id_time_sort.keys())
        ef_val = list(effect_point_internal_id_time_sort.values())

        left = 0
        right = len(ef_val) - 1

        if len(ef_val) == 1:
            return ef_val[0],  ef_val[0]  # 前地点と次地点あわせ

        while left <= right:  # 2つ以上のあたい
            mid = (left + right) // 2
            print(mid)
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
