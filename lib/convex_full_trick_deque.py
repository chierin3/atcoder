from collections import deque

# 傾きが単調減少する直線群に対して、xの値が単調増加するクエリを行う場合に高速化できるConvex Hull Trickの実装
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

def alien_trick(X, l1, l2, solve):
    h1, k1 = solve(l1)
    h2, k2 = solve(l2)
    while l1 + 1 < l2:
        l = (l1 + l2) // 2
        h, k = solve(l)
        if k > X:
            l1 = l
            h1, k1 = h, k
        else:
            l2 = l
            h2, k2 = h, k
    return max(h1 - l1 * X, h2 - l2 * X)

N, K = map(int,input().split())
A = list(map(int,input().split()))
A.sort()

def solve(pena):
    dp = [(10**20, 0)] * (N + 1)
    CHT = ConvexHullTrick()
    dp[0] = (0, 0)
    CHT.add_line(0, 0, 0)
    for i in range(N):
        line = CHT.query(A[i])
        val = line[0] * A[i] + line[1]
        dp[i + 1] = (val + A[i] * (i + 1) + pena, dp[line[2]][1] + 1)
        CHT.add_line(-(i + 1), dp[i + 1][0], i + 1)
    return dp[N]

l1 = -10**10
l2 = 10**10
ans = alien_trick(K, l1, l2, solve)
print(ans)