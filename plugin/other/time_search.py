import copy
from io import BufferedRandom


class TimeSearch:
    def time_search(now_f, this_effect, effect_point_internal_id_time, key_get=None):  # 二分探索
        #print("time_search", effect_point_internal_id_time)

        effect_point_internal_id_time_sort = dict(sorted(effect_point_internal_id_time.items(), key=lambda x: x[1]))

        #print("time_search_sort", effect_point_internal_id_time_sort)

        ef_key = list(effect_point_internal_id_time_sort.keys())
        ef_val = list(effect_point_internal_id_time_sort.values())

        left = 0
        right = len(ef_val) - 1

        """ #将来のためのコード未実装
        if #ここにイージングが停止なら・・・の処理を書く
            #print("返送")
            return ef_val[0],  0  # 前地点と次地点あわせ
        """

        if len(ef_val) == 1 and key_get:
            # print("返送")
            return ef_val[0],  ef_val[0], ef_key[0], ef_key[0]  # 前地点と次地点あわせ

        if len(ef_val) == 1:
            # print("返送")
            return ef_val[0],  ef_val[0]  # 前地点と次地点あわせ

        #print(ef_key, ef_val, now_f)

        while left <= right:  # 2つ以上のあたい
            mid = (left + right) // 2
            # print(mid)
            if ef_val[mid] <= now_f < ef_val[mid + 1]:
                break

            elif ef_val[mid] > now_f:  # 現在フレームより前地点がでかい場合
                left -= 1

            elif ef_val[mid + 1] <= now_f:  # 現在フレームより次地点がちいさい場合
                right += 1

        left_key = ef_key[left]
        right_key = ef_key[right]

        point_left = copy.deepcopy(this_effect.effect_point_internal_id_point[left_key])
        point_right = copy.deepcopy(this_effect.effect_point_internal_id_point[right_key])

        if key_get:
            return point_left, point_right, left_key, right_key

        #print("二分探索結果", point_left, point_right)

        return point_left, point_right
