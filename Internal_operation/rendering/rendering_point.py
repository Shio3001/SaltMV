class PointAnalysis:
    def __init__(self):
        pass

    def main(self, before_point, next_point, now_f):
        if before_point["time"] == next_point["time"]:
            next_point["time"] += 1

        now_point = self.analysis(before_point, next_point, now_f)

        return now_point

    def analysis(self, before_point, next_point, now_f):

        t = next_point["time"] - before_point["time"]
        nt = now_f - before_point["time"]

        del before_point["time"]
        del next_point["time"]

        now_point = {bk: ((nv - bv) / t) * nt for bk, nk, bv, nv in zip(before_point.keys(), next_point.keys(), before_point.vales(), next_point.vales())}
        now_point["time"] = now_f

        # print(now_point)

        return now_point
