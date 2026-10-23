# 強連結成分分解 (SCC) の実装
# componentに強連結成分のリストがトポロジカルソート順に格納される
# 各頂点の強連結成分IDはcomp_idに格納される
class SCC:
    def __init__(self, N):
        self.N = N
        self.G = [[] for _ in range(N + 1)]
        self.GR = [[] for _ in range(N + 1)]
        self.order = [] # 帰りがけ順の並び
        self.component = [] # 強連結成分のリスト
        self.comp_id = [-1] * (N + 1)  # 各頂点の強連結成分ID

    def add_edge(self, a, b):
        self.G[a].append(b)
        self.GR[b].append(a)

    def find_scc(self):
        visited = [False] * (self.N + 1) # 訪問済みフラグ
        processed = [False] * (self.N + 1) # 処理済みフラグ
        for i in range(1, self.N + 1):
            if not visited[i]:
                Q = [i]
                while Q:
                    v = Q.pop()
                    if not visited[v]:
                        visited[v] = True
                        Q.append(v)
                        for u in self.G[v]:
                            if not visited[u]:
                                Q.append(u)
                    else:
                        if not processed[v]:
                            processed[v] = True
                            self.order.append(v)

        visited = [False] * (self.N + 1)
        id = 1
        for i in reversed(self.order):
            if not visited[i]:
                self.component.append([])
                Q = [i]
                while Q:
                    v = Q.pop()
                    if not visited[v]:
                        visited[v] = True
                        self.component[-1].append(v)
                        self.comp_id[v] = id
                        for u in self.GR[v]:
                            if not visited[u]:
                                Q.append(u)
                id += 1

    def same(self, a, b):
        return self.comp_id[a] == self.comp_id[b]

N, M = map(int, input().split())
scc = SCC(N)
for _ in range(M):
    a, b = map(int, input().split())
    scc.add_edge(a, b)
scc.find_scc()
dp = [0] * len(scc.component)
ans = 0
for i in range(len(scc.component)-1, -1, -1):
    if len(scc.component[i]) == 1:
        for v in scc.G[scc.component[i][0]]:
            dp[i] += dp[scc.comp_id[v]]
    else:
        dp[i] = 1
    if dp[i] : ans += len(scc.component[i])
print(ans)