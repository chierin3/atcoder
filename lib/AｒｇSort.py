import bisect
import math

# 偏角ソート用の二次元点クラス
class Point():
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

    # 偏角の大小を比較する関数
    def cmp(self, other):
        # 第一象限・第二象限か第三象限・第四象限かで場合分け
        ph1 = self.y < 0 or (self.y == 0 and self.x < 0)
        ph2 = other.y < 0 or (other.y == 0 and other.x < 0)
        if ph1 != ph2:
            return ph1
        # 外積で偏角の大小を判定
        cross = self.x * other.y - self.y * other.x
        return cross > 0
    
    def __lt__(self, other):
        return self.cmp(other)
    
def get_arg(p1, p2):
    a1 = math.atan2(p1.y, p1.x) * 180 / math.pi
    a2 = math.atan2(p2.y, p2.x) * 180 / math.pi
    return min(abs(a1 - a2), 360 - abs(a1 - a2))

N, Q = map(int, input().split())
P = []
X = []
Y = []
for i in range(N):
    x, y = map(int, input().split())
    P.append(Point(i, x, y))
    X.append(x)
    Y.append(y)
P.sort()
for _ in range(Q):
    l, r = map(int, input().split())
    l -= 1
    r -= 1
    a = bisect.bisect_right(P, Point(-1, X[l], Y[l]))
    b = bisect.bisect_left(P, Point(-1, X[r], Y[r]))
    if a <= b:
        print(N - (b - a))
    else:
        print(a - b)
