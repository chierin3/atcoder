N, M = map(int,input().split())
A = []
B = []
C = []
D = []
for i in range(N):
    a, b = map(int,input().split())
    A.append(a)
    B.append(b)
for i in range(M):
    c, d = map(int,input().split())
    C.append(c)
    D.append(d)

def check(mid):
    ans1 = []
    ans2 = []
    for i in range(N):
        ans1.append(B[i] - mid * A[i])
    ans1.sort(reverse=True)
    for i in range(M):
        ans2.append(D[i] - mid * C[i])
    ans2.sort(reverse=True)
    return sum(ans1[:5]) >= 0 or sum(ans1[:4]) + ans2[0] >= 0

# 答えの二部探索の実数対応
# 小数点以下15桁までの精度が必要
left, right = 0, 10**10
for _ in range(90):
    mid = (left + right) / 2
    if check(mid):
        left = mid  # midが条件を満たすなら、さらに大きい値を探す
    else:
        right = mid # midが条件を満たさないなら、小さい値を探す
print(left)  # 最大のmidを出力