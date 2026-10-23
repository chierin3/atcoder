#最大値nのnCkを計算する(modは素数)
class Combination:
    def __init__(self, n, mod):
        self.n = n
        self.mod = mod
        self.fact = [1] * (n + 1)
        self.inv_fact = [1] * (n + 1)
        for i in range(2, n + 1):
            self.fact[i] = self.fact[i - 1] * i % mod
            self.inv_fact[i] = pow(self.fact[i], -1, mod)

    def comb(self, n, k):
        if n < k:
            return 0
        return self.fact[n] * self.inv_fact[k] * self.inv_fact[n - k] % self.mod

#最大値nのnCkを計算する(modは素数ではない場合)
#nは5000以下とする(時間計算量O(n^2))
class Combination_low:
    def __init__(self, n, mod):
        self.n = n
        self.mod = mod
        self.comb = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n + 1):
            self.comb[i][0] = 1
            for j in range(1, i + 1):
                self.comb[i][j] = (self.comb[i - 1][j - 1] + self.comb[i - 1][j]) % mod

A,B,C,D = map(int,input().split())
m = 998244353
CONB = Combination(A + B + C + D, m)
ans = 0
for i in range(C+1):
    a = A + B + i
    left = CONB.comb(a, B)
    d = D - 1 + C - i
    right = CONB.comb(d, D - 1)
    ans =  (ans + left * right) % m
print(ans)