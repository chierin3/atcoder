from functools import cmp_to_key

# 偏角ソート
# p1,p2は(x,y)のタプル
def cmp(p1, p2):
    # 第一象限・第二象限か第三象限・第四象限かで場合分け
    ph1 = p1[1] < 0 or (p1[1] == 0 and p1[0] < 0)
    ph2 = p2[1] < 0 or (p2[1] == 0 and p2[0] < 0)
    if ph1 != ph2:
        return -1 if ph2 else 1 # p1が第一・第二象限なら前に
    # 外積で偏角の大小を判定
    cross = p1[0] * p2[1] - p1[1] * p2[0]
    if cross == 0:
        return 0
    elif cross > 0:
        return -1
    else:
        return 1

N, Q = map(int, input().split())
P = []
for i in range(N):
    x, y = map(int, input().split())
    P.append((x, y, i))
P.sort(key=cmp_to_key(cmp), reverse=True)
PtoIdx = [0] * N
for i in range(N):
    PtoIdx[P[i][2]] = i
L = [0] * N
R = [N] * N
for i in range(1, N):
    L[i] = L[i - 1] if cmp(P[i - 1], P[i]) == 0 else i
for i in range(N - 2, -1, -1):
    R[i] = R[i + 1] if cmp(P[i], P[i + 1]) == 0 else i + 1
for _ in range(Q):
    l, r = map(int, input().split())
    l -= 1
    r -= 1
    a = L[PtoIdx[l]]
    b = R[PtoIdx[r]]
    if a >= b:
        print(N - (a - b))
    else:
        print(b - a)
