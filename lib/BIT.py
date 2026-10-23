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
        return self.sum(r + 1) - self.sum(l)

N=10 # int(input())
B=[2,6,3,16,7,10,6,3,9,11] # list(map(int, input().split()))
Q=1000 # int(input())

bit=BIT(N)
for i, b in enumerate(B):
    bit.add(i+1,b)

for _ in range(Q):
    L, R=map(int, input().split())
    ans=bit.sum(R)-bit.sum(L-1)
    print(ans)