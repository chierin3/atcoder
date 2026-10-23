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

N, Q = map(int, input().split())
A = list(map(int, input().split()))
P = list(map(int, input().split()))
G = [[] for _ in range(N)]
for i in range(N - 1):
    p = P[i]
    G[p].append(i + 1)
IN = [-1] * N
OUT = [-1] * N
TOUR = []
stack = [0]
visited = [False] * N
while stack:
    v = stack.pop()
    if visited[v]:
        OUT[v] = len(TOUR)
    else:
        visited[v] = True
        IN[v] = len(TOUR)
        TOUR.append(v)
        stack.append(v)
        for w in G[v]:
            if not visited[w]:
                stack.append(w)
bit = BIT(N)
for i in range(N):
    bit.add(IN[i] + 1, A[i])
for i in range(Q):
    query = list(map(int, input().split()))
    if query[0] == 0:
        _, u, x = query
        bit.add(IN[u] + 1, x)
    else:
        _, u = query
        ans = bit.sum(OUT[u]) - bit.sum(IN[u])
        print(ans)