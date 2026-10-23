class LCA:
    def __init__(self, n):
        self.n = n
        self.root = 1
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

N = int(input())
lca = LCA(N)
for _ in range(N - 1):
    a, b = map(int, input().split())
    lca.add_edge(a, b)
lca.init()
Q = int(input())
for _ in range(Q):
    u, v = map(int, input().split())
    print(lca.find_lca(u, v))