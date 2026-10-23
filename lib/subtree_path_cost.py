from typing import Callable
# 0-indexed
# [l,r)の区間に対してfuncを作用させる
class segmentTree():
    def __init__(self,N:int,INF:int,func:Callable) -> None:
        size = 1
        while size < N : size *= 2
        self.N = N
        self.size = size
        self.INF = INF
        self.func = func
        self.data = [self.INF] * (size*2)

    def get(self,pos:int)->int:
        return self.data[pos + self.size]
    
    def update(self,pos:int,x:int):
        pos = pos + self.size
        self.data[pos] = x
        while pos >= 2:
            pos >>= 1
            self.data[pos] = self.func(self.data[pos*2],self.data[pos*2+1])

    # pos番目にxを足す
    def add(self,pos:int,x:int):
        z = self.get(pos)
        self.update(pos, z + x)

    # pos番目にfuncを作用させる
    def add_f(self,pos:int,x:int):
        z = self.get(pos)
        self.update(pos, self.func(z, x))
    
    def query(self,l:int,r:int)->int:
        l += self.size
        r += self.size
        value_L = self.INF
        value_R = self.INF
        while l < r:
            if l & 1:
                value_L = self.func(value_L, self.data[l])
                l += 1
            if r & 1:
                r -= 1
                value_R = self.func(self.data[r], value_R)
            l >>= 1
            r >>= 1
        return self.func(value_L, value_R)
    
    # funcを満たす最小のrを返す
    def bisect(self,x:int,func:Callable)->int:
        l = 0
        r = self.N
        while r - l > 1:
            m = (l + r) // 2
            if func(self.query(0, m), x):
                r = m
            else:
                l = m
        return r
    
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
    
N = int(input())
G = [[] for _ in range(N)]
for i in range(N - 1):
    u, v, w = map(int, input().split())
    u -= 1
    v -= 1
    G[u].append((v, w, i))
    G[v].append((u, w, i))
IN = [-1] * N
OUT = [-1] * N
TOUR = []
DEPTH = []
stack = [(0, 0)]
visited = [False] * N
W = [0] * N
edge_id = [-1] * N
while stack:
    v, d = stack.pop()
    if visited[v]:
        OUT[v] = len(TOUR)
        TOUR.append(v)
        DEPTH.append(d)
    else:
        visited[v] = True
        IN[v] = len(TOUR)
        TOUR.append(v)
        DEPTH.append(d)
        is_child = True
        for u, w, id in G[v]:
            if not visited[u]:
                is_child = False
                W[u] = w
                edge_id[id] = u
                stack.append((v, d))
                stack.append((u, d + 1))
        if is_child:
            stack.append((v, d))
SEG = segmentTree(len(TOUR), (1000000,-1), lambda x, y: x if x[0] < y[0] else y)
bit = BIT(len(TOUR))
for i in range(len(TOUR)):
    SEG.update(i, (DEPTH[i], TOUR[i]))
for i in range(N):
    bit.add(IN[i] + 1, W[i])
    bit.add(OUT[i] + 1, -W[i])
Q = int(input())
for i in range(Q):
    query = list(map(int, input().split()))
    if query[0] == 1:
        i, w = query[1], query[2]
        i -= 1
        u = edge_id[i]
        bit.add(IN[u] + 1, w - W[u])
        bit.add(OUT[u] + 1, W[u] - w)
        W[u] = w
    else:
        u, v = query[1], query[2]
        u -= 1
        v -= 1
        l = IN[u]
        r = IN[v]
        if l > r:
            l, r = r, l
        w = SEG.query(l, r + 1)[1]
        ans = bit.sum(IN[u] + 1) + bit.sum(IN[v] + 1) - 2 * bit.sum(IN[w] + 1)
        print(ans)