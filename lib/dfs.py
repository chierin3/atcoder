# DFSを再帰関数を使わずに実装
# 再帰関数はメモリ使用量が大きくなるため、スタックを使って実装する
N = int(input())
G = [[] for _ in range(N)]
M = []
for _ in range(N-1):
    u, v = map(int, input().split())
    G[u-1].append(v-1)
    G[v-1].append(u-1)
    M.append((u-1, v-1))
L = [-1] * N
R = [-1] * N  
stack = [0]
parent = [-1] * N
l = 1
while stack:
    v = stack.pop()
    if L[v] == -1:  # 初めて訪れるノード
        L[v] = l
        R[v] = l
        l += 1
        stack.append(v)  # 処理を後で再開するためにスタックに戻す
        for u in G[v]:
            if L[u] == -1:
                parent[u] = v
                stack.append(u)
    else:  # 子ノードの処理が終わった後に戻ってきたノード
        for u in G[v]:
            if parent[v] != u:  # 親ノードではない子ノード
                R[v] = max(R[v], R[u])