N, Q = map(int,input().split())
A = list(map(int,input().split()))
width = max(1, int(N / (Q ** 0.5)))
qs = [[] for _ in range(N // width + 1)]
for i in range(Q):
    l, r = map(int,input().split())
    l -= 1
    r -= 1
    qs[l // width].append((r, l, i))
ans = [0] * Q
count = 0
d = [0] * (max(A) + 1)
d[A[0]] += 1

def add(x):
    global count
    d[x] += 1
    count += C[d[x]]

def remove(x):
    global count
    count -= C[d[x]]
    d[x] -= 1

x = 0
y = 0
C = [0] * (N + 1)
for i in range(len(C)):
    if i >= 3:
        C[i] = (i - 2) * (i - 1) // 2
for i, qb in enumerate(qs):
    qb.sort(key=lambda x : x[0], reverse=bool(i & 1))
    for r, l, j in qb:
        while x > l:
            x -= 1
            add(A[x])
        while y < r:
            y += 1
            add(A[y])
        while x < l:
            remove(A[x])
            x += 1
        while y > r:
            remove(A[y])
            y -= 1
        ans[j] = count
for a in ans:
    print(a)