#https://github.com/chierin3/atcoder
class BIT:
    # 長さN+1の配列を初期化
    def __init__(self, N):
        self.size = N
        self.bit = [0]*(N+1)

    # i番目までの和を求める
    def sum(self, i):
        res = 0
        while i > 0:
            res += self.bit[i] # フェニック木のi番目の値を加算
            i -= -i & i # 最も右にある1の桁を0にする
        return res

    # i番目の値にxを足して更新する
    def add(self, i, x):
        while i <= self.size:
            self.bit[i] += x # フェニック木のi番目にxを足して更新
            i += -i & i # 最も右にある1の桁に1を足す

    # [l, r)の範囲の和を求める
    # l, rは0-indexed
    def query(self, l, r):
        return self.sum(r) - self.sum(l)
    
N, L, R = map(int,input().split())
A = list(map(int,input().split()))
B = [0] * (N + 1)
for i in range(N):
    B[i + 1] = B[i] + A[i]
Z = set(B)
for i in range(N + 1):
    Z.add(B[i] - L)
    Z.add(B[i] - R - 1)
Z = sorted(list(Z))
Z = {Z[i] : i + 1 for i in range(len(Z))}
bit = BIT(len(Z))
ans = 0
for i in range(N + 1):
    left = bit.sum(Z[B[i] - R - 1])
    right = bit.sum(Z[B[i] - L])
    ans += right - left
    bit.add(Z[B[i]], 1)
print(ans)