from collections import deque

class Edge: 
    # to: Edgeの行き先、cap: Edgeの容量、rev: 逆辺のEdgeオブジェクト
    def __init__(self, to:int, cap:int, rev:any):
        self.to = to
        self.cap = cap
        self.rev = rev

# Dinic法による最大流問題の解法
# 計算量は O(V^2 * E) で、Vは頂点の数、Eは辺の数
class MaximumFlow():
    s:int
    t:int
    size:int
    G:list[list[Edge]]
    used:list[bool]
    offset:int
    
    def __init__(self, N:int, INF:int):
        # N + 2にすることで、0番目を始点s、H * W + 1番目を終点tとして扱えるようにする
        self.size = N + 2
        self.s = N
        self.t = N + 1
        self.INF = INF
        self.G = [[] for i in range(self.size)]
        self.offset = 0

    # uからvへの容量capの辺を追加する
    # vからuへの逆辺の容量は0で追加する
    def add(self, u:int, v:int, cap:int):
        E = Edge(v, cap, None)
        rev = Edge(u, 0, E)
        E.rev = rev
        self.G[u].append(E)
        self.G[v].append(rev)

    # uとvの両方がTrueのときにコストcostを得る
    def add_constraint_both_true(self, u:int, v:int, cost:int):
        k = self.s - self.offset - 1
        self.add(u, k, self.INF)
        self.add(v, k, self.INF)
        self.add(k, self.t, cost)
        self.offset += 1

    # uとvの両方がFalseのときにコストcostを得る
    def add_constraint_both_false(self, u:int, v:int, cost:int):
        k = self.s - self.offset - 1
        self.add(k, u, self.INF)
        self.add(k, v, self.INF)
        self.add(self.s, k, cost)
        self.offset += 1

    def bfs(self, s:int):
        self.D = [-1] * self.size
        self.D[s] = 0
        Q = deque()
        Q.append(s)
        while Q:
            u = Q.popleft()
            for E in self.G[u]:
                if E.cap > 0 and self.D[E.to] < 0:
                    self.D[E.to] = self.D[u] + 1
                    Q.append(E.to)

    def dfs(self, s:int, g:int, f:int) -> int:
        if s == g : return f
        while self.used[s] < len(self.G[s]):
            E = self.G[s][self.used[s]]
            if E.cap > 0 and self.D[s] < self.D[E.to]:
                flow = self.dfs(E.to, g, min(f, E.cap))
                if flow > 0:
                    E.cap -= flow
                    E.rev.cap += flow
                    return flow
            self.used[s] += 1
        return 0

    def max_flow(self, s:int, g:int) -> int:
        ans = 0
        while True:
            self.bfs(s)
            if self.D[g] < 0 : break
            self.used = [0] * self.size
            while True:
                flow = self.dfs(s, g, self.INF)
                if flow == 0 : break
                ans += flow
        return ans
    
N, M = map(int,input().split())
MF = MaximumFlow(N, 10**9)
for i in range(M):
    a, b, c = map(int,input().split())
    MF.add(a, b, c)
print(MF.max_flow(1, N))