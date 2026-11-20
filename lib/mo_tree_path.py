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

N = int(input())
A = list(map(int,input().split()))
B = list(map(int,input().split()))
Z = {z:i for i,z in enumerate(sorted(set(B)))}
for i in range(N):
    B[i] = Z[B[i]]
del Z
G = [[] for _ in range(N)]
for i in range(N - 1):
    a, b = map(int,input().split())
    a -= 1
    b -= 1
    G[a].append(b)
    G[b].append(a)
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

IN2 = [-1] * N
OUT2 = [-1] * N
TOUR2 = []
stack = [0]
visited = [False] * N
while stack:
    v = stack.pop()
    if visited[v]:
        OUT2[v] = len(TOUR2)
        TOUR2.append(v)
    else:
        visited[v] = True
        stack.append(v)
        IN2[v] = len(TOUR2)
        TOUR2.append(v)
        for w in G[v]:
            if not visited[w]:
                stack.append(w)

Q = int(input())
W = len(TOUR2)
width = max(1, int(W / (Q ** 0.5)))
qs = [[] for _ in range(W // width + 1)]
K = []
for i in range(Q):
    u, v = map(int,input().split())
    u -= 1
    v -= 1
    if IN[u] > IN[v]:
        u, v = v, u
    lca = SEG.query(IN[u], IN[v] + 1)[1]
    is_lca = lca == u or lca == v
    if lca == u:
        l = IN2[u]
        r = IN2[v]
    else:
        l = OUT2[u]
        r = IN2[v]
    qs[l // width].append((r, l, i, lca, is_lca))
ans = [0] * Q
visited = [False] * N
count = 0
total = [[0] * len(Z) for _ in range(2)]

def add(x):
    global count
    if visited[x]:
        total[A[x]][B[x]] -= 1
        count -= total[(A[x] + 1) % 2][B[x]]
    else:
        total[A[x]][B[x]] += 1
        count += total[(A[x] + 1) % 2][B[x]]
    visited[x] = not visited[x]

def remove(x):
    global count
    if visited[x]:
        total[A[x]][B[x]] -= 1
        count -= total[(A[x] + 1) % 2][B[x]]
    else:
        total[A[x]][B[x]] += 1
        count += total[(A[x] + 1) % 2][B[x]]
    visited[x] = not visited[x]

x = 0
y = -1
for i, qb in enumerate(qs):
    qb.sort(key=lambda x : x[0], reverse=bool(i & 1))
    for r, l, j, p, b in qb:
        while x > l:
            x -= 1
            add(TOUR2[x])
        while y < r:
            y += 1
            add(TOUR2[y])
        while x < l:
            remove(TOUR2[x])
            x += 1
        while y > r:
            remove(TOUR2[y])
            y -= 1
        if not b:
            ans[j] = count + total[(A[p] + 1) % 2][B[p]]
        else:
            ans[j] = count
for a in ans:
    print(a)