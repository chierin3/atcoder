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

class HeavyLightDecomposition():
    N:int
    G:list[list[int]]
    heavy:list[int]
    depth:list[int]
    parent:list[int]
    size:list[int]
    vertex:list[int]
    id:list[int]
    head:list[int]
    SEG:segmentTree

    def __init__(self,N:int) -> None:
        self.N = N
        self.G = [[] for _ in range(N)]
        self.heavy = [-1] * N
        self.depth = [0] * N
        self.parent = [-1] * N
        self.size = [0] * N
        self.vertex = [-1] * N
        self.id = [-1] * N
        self.head = [0] * N

    def connect(self, u:int, v:int):
        self.G[u].append(v)
        self.G[v].append(u)

    def built(self):
        stack = [0]
        visited = [False] * self.N
        while stack:
            u = stack.pop()
            if visited[u]:
                self.size[u] = 1
                mx = 0
                for v in self.G[u]:
                    self.size[u] += self.size[v]
                    if self.size[v] > mx:
                        mx = self.size[v]
                        self.heavy[u] = v
            else:
                visited[u] = True
                stack.append(u)
                for v in self.G[u]:
                    if not visited[v]:
                        self.parent[v] = u
                        self.depth[v] = self.depth[u] + 1
                        stack.append(v)
        stack = [0]
        k = 0
        while stack:
            u = stack.pop()
            self.vertex[k] = u
            self.id[u] = k
            k += 1
            for v in self.G[u]:
                if v == self.parent[u] : continue
                if v == self.heavy[u]:
                    self.head[v] = self.head[u]
                else:
                    self.head[v] = v
                    stack.append(v)
            if self.heavy[u] != -1:
                stack.append(self.heavy[u])

    def level_ancestor(self, u:int, d:int):
        if (self.depth[u] < d) : return -1
        while(self.depth[self.head[u]] > d):
            u = self.parent[self.head[u]]
        return self.vertex[self.id[u] - (self.depth[u] - d)]
    
    def lca(self, u:int, v:int):
        while self.head[u] != self.head[v]:
            if self.id[u] < self.id[v]:
                u, v = v, u
            u = self.parent[self.head[u]]
        if self.depth[u] > self.depth[v]:
            u, v = v, u
        return u

    def distance(self, u:int, v:int):
        w = self.lca(u, v)
        return self.depth[u] + self.depth[v] - 2 * self.depth[w]
    
    def jump(self, u:int, v:int, i:int):
        w = self.lca(u, v)
        dist = self.distance(u, v)
        if dist < i : return -1
        if i < self.depth[u] - self.depth[w]:
            return self.level_ancestor(u, self.depth[u] - i)
        else:
            return self.level_ancestor(v, self.depth[v] - (dist - i))
        
    def query(self, u:int, v:int):
        w = self.lca(u, v)
        ans = 0
        while self.head[u] != self.head[w]:
            ans += self.SEG.query(self.id[self.head[u]], self.id[u] + 1)
            u = self.parent[self.head[u]]
        ans += self.SEG.query(self.id[w], self.id[u] + 1)
        while self.head[v] != self.head[w]:
            ans += self.SEG.query(self.id[self.head[v]], self.id[v] + 1)
            v = self.parent[self.head[v]]
        ans += self.SEG.query(self.id[w], self.id[v] + 1)
        ans -= self.SEG.get(self.id[w])
        return ans

N, Q = map(int,input().split())
A = list(map(int,input().split()))
HLD = HeavyLightDecomposition(N)
HLD.SEG = segmentTree(N, 0, lambda x, y : x + y)
for i in range(N - 1):
    x, y = map(int,input().split())
    HLD.connect(x, y)
HLD.built()
for i in range(N):
    HLD.SEG.update(HLD.id[i], A[i])
for _ in range(Q):
    query = list(map(int,input().split()))
    if query[0] == 0:
        p, x = query[1], query[2]
        HLD.SEG.add(HLD.id[p], x)
    else:
        u, v = query[1], query[2]
        print(HLD.query(u, v))