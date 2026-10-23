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
    
N, Q = map(int, input().split())
P = list(map(int, input().split()))
G = [[] for _ in range(N)]
for i in range(N - 1):
    p = P[i]
    G[p].append(i + 1)
IN = [-1] * N
OUT = [-1] * N
TOUR = []
DEPTH = []
stack = [(0, 0)]
visited = [False] * N
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
        for w in G[v]:
            if not visited[w]:
                stack.append((v, d))
                stack.append((w, d + 1))
SEG = segmentTree(len(TOUR), (1000000,-1), lambda x, y: x if x[0] < y[0] else y)
for i in range(len(TOUR)):
    SEG.update(i, (DEPTH[i], TOUR[i]))
for i in range(Q):
    u, v = map(int, input().split())
    l = IN[u]
    r = IN[v]
    if l > r:
        l, r = r, l
    ans = SEG.query(l, r + 1)[1]
    print(ans)