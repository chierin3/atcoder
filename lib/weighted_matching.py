import heapq
N = int(input())
A = []
for i in range(N):
    a = int(input())
    A.append(a)

#辺重みを頂点重みに変換する
B = [0]
for i in range(N):
    B.append(A[i] - B[i])

#辺の重みを負にして優先度付きキューに入れる
Q = []
for i in range(N):
    heapq.heappush(Q, (-B[i] - B[i + 1], i, i + 1))
#隣接リストを作る
L = [i - 1 for i in range(N + 1)]
R = [i + 1 for i in range(N + 1)]

ans = 0
visited = [False] * (N + 1)
count = 0
while Q:
    a, l, r = heapq.heappop(Q)
    if (visited[l] or visited[r]):
        continue
    visited[l] = True
    visited[r] = True
    ans -= a
    print(ans)
    count += 1
    if count == (N + 1) // 2:
        break
    if 0 < l and r < N:
        nl = L[l]
        nr = R[r]
        heapq.heappush(Q, (-B[nl] - B[nr], nl, nr))
        L[nr] = nl
        R[nl] = nr