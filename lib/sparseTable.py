from typing import Callable

class sparseTable():
    def __init__(self, N: int, func: Callable) -> None:
        self.N = N
        self.func = func
        self.size = N.bit_length()
        self.ST = [[0] * N for _ in range(self.size)]
        self.log_table = [0] * (N + 1)
        for i in range(2, N + 1):
            self.log_table[i] = self.log_table[i // 2] + 1

    def build(self, A: list) -> None:
        for i in range(self.N):
            self.ST[0][i] = A[i]
        for j in range(1, self.size):
            for i in range(self.N - (1 << j) + 1):
                self.ST[j][i] = self.func(self.ST[j - 1][i], self.ST[j - 1][i + (1 << (j - 1))])

    # [l,r]の区間に対してqueryを行う
    def query(self, l: int, r: int) -> int:
        j = self.log_table[r - l + 1]
        return self.func(self.ST[j][l], self.ST[j][r - (1 << j) + 1])

N, K = map(int, input().split())
H = list(map(int, input().split()))
ST1 = sparseTable(N, lambda x, y: min(x, y))
ST1.build(H)
ST2 = sparseTable(N, lambda x, y: max(x, y))
ST2.build(H)
ans = -10**20
for i in range(N - K + 1):
    min_h = ST1.query(i, i + K - 1)
    max_h = ST2.query(i, i + K - 1)
    ans = max(ans, max_h - min_h)
print(ans)