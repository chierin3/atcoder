from collections import deque

# 傾きが単調増加（減少）する直線群に対して、xの値が単調増加（減少）するクエリを行う場合に高速化できるConvex Hull Trickの実装
class ConvexHullTrick:
    def __init__(self):
        self.lines = deque()

    def add_line(self, a, b, i):
        while len(self.lines) >= 2 and self._is_bad(self.lines[-2], self.lines[-1], (a, b, i)):
            self.lines.pop()
        self.lines.append((a, b, i))

    def _is_bad(self, line1, line2, line3):
        return (line3[1] - line1[1]) * (line1[0] - line2[0]) <= (line2[1] - line1[1]) * (line1[0] - line3[0])
    
    def query(self, x):
        while len(self.lines) >= 2 and self._evaluate(self.lines[0], x) >= self._evaluate(self.lines[1], x):
            self.lines.popleft()
        return self.lines[0]
    
    def _evaluate(self, line, x):
        a, b, _ = line
        return a * x + b

# EDPC-Z Frog3    
N, C = map(int,input().split())
H = list(map(int,input().split()))
dp = [0] * N
CHT = ConvexHullTrick()
CHT.add_line(-2 * H[0], H[0] ** 2, 0)
for i in range(1, N):
    a, b, j = CHT.query(H[i])
    dp[i] = a * H[i] + b + C + H[i] ** 2
    CHT.add_line(-2 * H[i], dp[i] + H[i] ** 2, i + 1)
print(dp[N - 1])