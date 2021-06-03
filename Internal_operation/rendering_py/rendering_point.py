class PointAnalysis:
    def __init__(self):
        self.effect_point_default_keys = []

    def main(self, before_point, next_point, now_f, effect_point_default_keys):
        self.effect_point_default_keys = effect_point_default_keys
        if before_point["time"] == next_point["time"]:
            next_point["time"] += 1

        now_point = self.analysis(before_point, next_point, now_f)

        return now_point

    def analysis(self, before_point, next_point, now_f):

        t = next_point["time"] - before_point["time"]
        nt = now_f - before_point["time"]

        for k in self.effect_point_default_keys:
            del before_point[k]
            del next_point[k]

        now_point = {bk: ((nv - bv) / t) * nt for bk, nk, bv, nv in zip(before_point.keys(), next_point.keys(), before_point.vales(), next_point.vales())}

        # 時間演算法方法：((次の値 - 前の値) / 間の時間) * 今の時間

        now_point["time"] = now_f

        # print(now_point)

        return now_point
