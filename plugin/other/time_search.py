import copy


class TimeSearch:
    def time_search(now_f, this_effect, number=None,effect_point_internal_id_time):  # 二分探索
        ef_po = list(this_effect.effect_point_internal_id_point.values())

        left = 0
        right = len(ef_po) - 1

        if len(ef_po) == 1:
            return ef_po[0]["time"],  ef_po[0]["time"]  # 前地点と次地点あわせ

        while left <= right:  # 2つ以上のあたい
            mid = (left + right) // 2
            if ef_po[mid]["time"] <= now_f < ef_po[mid + 1]["time"]:
                return ef_po[mid], ef_po[mid + 1]

            elif ef_po[mid]["time"] > now_f:  # 現在フレームより前地点がでかい場合
                left -= 1

            elif ef_po[mid + 1]["time"] <= now_f:  # 現在フレームより次地点がちいさい場合
                right += 1

        print(left, right)

        if number:
            return left, right

        return copy.deepcopy(ef_po[left]["effect"], ef_po[right]["effect"])
