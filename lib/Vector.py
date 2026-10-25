import math

# 2次元ベクトルのクラス
class Vector():
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    
    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self
    
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
    
    def __imul__(self, scale):
        self.x *= scale
        self.y *= scale
        return self
    
    def __mul__(self, scale):
        return Vector(self.x * scale, self.y * scale)
    
    def __itruediv__(self, scale):
        self.x /= scale
        self.y /= scale
        return self
    
    def __truediv__(self, scale):
        return Vector(self.x / scale, self.y / scale)
    
    def __ifloordiv__(self, scale):
        self.x //= scale
        self.y //= scale
        return self

    def __floordiv__(self, scale):
        return Vector(self.x // scale, self.y // scale)
    
    def dot(self, other):
        return self.x * other.x + self.y * other.y
    
    def cross(self, other):
        return self.x * other.y - self.y * other.x
    
    def norm2(self):
        return self.x ** 2 + self.y ** 2
    
    def norm(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5
    
    def normarize(self):
        return self / self.norm()
    
    def rotate90(self):
        return Vector(self.y, -self.x)
    
    # 偏角の大小を比較する関数
    # 順番は第一象限→第二象限→第三象限→第四象限の順で、同じ象限内では外積の符号で比較する
    def cmp(self, other):
        # 第一象限・第二象限か第三象限・第四象限かで場合分け
        ph1 = self.y < 0 or (self.y == 0 and self.x < 0)
        ph2 = other.y < 0 or (other.y == 0 and other.x < 0)
        if ph1 != ph2:
            return not ph1
        # 外積で偏角の大小を判定
        cross = self.cross(other)
        return cross > 0
    
    def __lt__(self, other):
        return self.cmp(other)
    
    def __str__(self):
        return f"{self.x}, {self.y}"
    
def get_arg(p1, p2):
    a1 = math.atan2(p1.y, p1.x) * 180 / math.pi
    a2 = math.atan2(p2.y, p2.x) * 180 / math.pi
    return min(abs(a1 - a2), 360 - abs(a1 - a2))

T = int(input())
for _ in range(T):
    px, py, qx, qy, rx, ry, sx, sy = map(int,input().split())
    P = Vector(px, py)
    Q = Vector(qx, qy)
    R = Vector(rx, ry)
    S = Vector(sx, sy)
    A = P + Q
    B = R + S
    if (P - Q).cross(R - S) != 0:
        print("Yes")
    elif (P - Q).rotate90().cross(B - A) == 0:
        print("Yes")
    else:
        print("No")
