class Edge: 
    # to: Edgeの行き先、cap: Edgeの容量、rev: 逆辺のEdgeオブジェクト
    def __init__(self, to:int, cap:int, rev:any):
        self.to = to
        self.cap = cap
        self.rev = rev

# Ford-Fulkerson法による最大流問題の解法
# 計算量は O(F * E) で、Fは最大流量、Eは辺の数
class MaximumFlow():
    size:int
    G:list[list[Edge]]
    used:list[bool]
    
    def __init__(self, N:int, INF:int):
        # N + 2にすることで、0番目を始点s、H * W + 1番目を終点tとして扱えるようにする
        self.size = N + 2
        self.INF = INF
        self.G = [[] for i in range(self.size)]

    # uからvへの容量capの辺を追加する
    # vからuへの逆辺の容量は0で追加する
    def add(self, u:int, v:int, cap:int):
        E = Edge(v, cap, None)
        rev = Edge(u, 0, E)
        E.rev = rev
        self.G[u].append(E)
        self.G[v].append(rev)
    
    def dfs(self, s:int, g:int, F:int) -> int:
        if s == g : return F
        self.used[s] = True
        for E in self.G[s]:
            if E.cap == 0 : continue
            if self.used[E.to] : continue
            flow = self.dfs(E.to,g,min(F,E.cap))
            if flow >= 1:
                E.cap -= flow
                E.rev.cap += flow
                return flow
        return 0
    
    def max_flow(self, s, g) -> int:
        ans = 0
        while True:
            self.used = [False] * self.size
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