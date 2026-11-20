N, Q = map(int, input().split())
A = list(map(int,input().split()))
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

width = max(1, int(N / (Q ** 0.5)))
qs = [[] for _ in range(N // width + 1)]
K = []
for i in range(Q):
    v, k = map(int,input().split())
    l = IN[v - 1]
    r = OUT[v - 1] - 1
    qs[l // width].append((r, l, i))
    K.append(k)
ans = [0] * Q
color = [0] * (max(A) + 1)
total = [0] * 100001

def add(x):
    color[A[x]] += 1
    total[color[A[x]]] += 1

def remove(x):
    total[color[A[x]]] -= 1
    color[A[x]] -= 1

x = 0
y = -1
for i, qb in enumerate(qs):
    qb.sort(key=lambda x : x[0], reverse=bool(i & 1))
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
        ans[j] = total[K[j]]
for a in ans:
    print(a)