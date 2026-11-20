import sys
class LCA:
    def __init__(self, n):
        self.n = n
        self.root = 0
        self.G = [[] for _ in range(n+1)]
        self.depth = [0] * (n + 1)
        v = 0
        while (1 << v) < n:
            v += 1
        self.v = v
        self.parent = [[-1] * (n + 1) for _ in range(v + 1)]

    def add_edge(self, a, b):
        self.G[a].append(b)
        self.G[b].append(a)

    def init(self):
        Q = [(self.root, 0)]
        visited = [False] * (self.n + 1)
        while Q:
            v, d = Q.pop()
            if not visited[v]:
                visited[v] = True
                self.depth[v] = d
                for u in self.G[v]:
                    if not visited[u]:
                        self.parent[0][u] = v
                        Q.append((u, d + 1))
        for i in range(1, self.v + 1):
            for j in range(1, self.n + 1):
                if self.parent[i-1][j] != -1:
                    self.parent[i][j] = self.parent[i-1][self.parent[i-1][j]]

    def find_lca(self, u, v):
        if self.depth[u] > self.depth[v]:
            u, v = v, u
        for i in range(self.v, -1, -1):
            if ((self.depth[v] - self.depth[u]) >> i) & 1:
                v = self.parent[i][v]
        if u == v:
            return u
        for i in range(self.v, -1, -1):
            if self.parent[i][u] != -1 and self.parent[i][u] != self.parent[i][v]:
                u = self.parent[i][u]
                v = self.parent[i][v]
        return self.parent[0][u]
    
    def distance(self, u, v):
        lca = self.find_lca(u, v)
        return self.depth[u] + self.depth[v] - 2 * self.depth[lca]

input = sys.stdin.buffer.readline
N, Q = map(int,input().split())
X = list(map(int,input().split()))
lca = LCA(N)
for i in range(N - 1):
    a, b = map(int,input().split())
    a -= 1
    b -= 1
    lca.add_edge(a, b)
lca.init()

IN = [-1] * N
OUT = [-1] * N
TOUR = []
stack = [0]
visited = [False] * N
while stack:
    v = stack.pop()
    if visited[v]:
        OUT[v] = len(TOUR)
        TOUR.append(v)
    else:
        visited[v] = True
        stack.append(v)
        IN[v] = len(TOUR)
        TOUR.append(v)
        for w in lca.G[v]:
            if not visited[w]:
                stack.append(w)

W = len(TOUR)
width = max(1, int(W / (Q ** 0.5)))
qs = [[] for _ in range(W // width + 1)]
A = [0] * Q
B = [0] * Q
P = [0] * Q
for i in range(Q):
    u, v, a, b = map(int,input().split())
    u -= 1
    v -= 1
    A[i] = a
    B[i] = b
    if IN[u] > IN[v]:
        u, v = v, u
    p = lca.find_lca(u, v)
    P[i] = p
    if p == u:
        l = IN[u] + 1
    else:
        l = OUT[u]
    r = IN[v]
    qs[l // width].append((r, l, i))
ans = [0] * Q
visited = [False] * N
count = [0] * (N + 9)
total = [0] * (N + 9)

def add(x):
    if visited[x]:
        total[count[X[x]]] -= 1
        count[X[x]] -= 1
    else:
        count[X[x]] += 1
        total[count[X[x]]] += 1
    visited[x] = not visited[x]

def remove(x):
    if visited[x]:
        total[count[X[x]]] -= 1
        count[X[x]] -= 1
    else:
        count[X[x]] += 1
        total[count[X[x]]] += 1
    visited[x] = not visited[x]

x = 0
y = -1
for i, qb in enumerate(qs):
    qb.sort(key = lambda x : x[0], reverse=bool(i & 1))
    for r, l, j in qb:
        while x > l:
            x -= 1
            add(TOUR[x])
        while y < r:
            y += 1
            add(TOUR[y])
        while x < l:
            remove(TOUR[x])
            x += 1
        while y > r:
            remove(TOUR[y])
            y -= 1
        add(P[j])
        ans[j] = total[A[j]] - total[B[j] + 1]
        remove(P[j])
        
sys.stdout.write("\n".join(map(str,ans)))