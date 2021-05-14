import copy


class TimeSearch:
    def time_search(now_f, this_effect, number=None):  # 二分探索
        left = 0
        right = len(this_effect.effect_point) - 1

        if len(this_effect.effect_point) == 1:
            return this_effect.effect_point[0], None  # 前地点と次地点あわせ

        while left <= right:  # 2つ以上のあたい
            mid = (left + right) // 2
            if this_effect.effect_point[mid]["time"] <= now_f < this_effect.effect_point[mid + 1]["time"]:
                return this_effect.effect_point[mid], this_effect.effect_point[mid + 1]

            elif this_effect.effect_point[mid]["time"] > now_f:  # 現在フレームより前地点がでかい場合
                left -= 1

            elif this_effect.effect_point[mid + 1]["time"] <= now_f:  # 現在フレームより次地点がちいさい場合
                right += 1

        print(left, right)

        if number:
            return left, right

        return copy.deepcopy(this_effect.effect_point[left], this_effect.effect_point[right])
