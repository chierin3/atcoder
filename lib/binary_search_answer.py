N, K = map(int,input().split())
W = []
P = []
S = []
for i in range(N):
    w, p = map(int,input().split())
    W.append(w)
    P.append(p)
    S.append(w * p / 100)

def check(mid):
    ans = []
    for i in range(N):
        ans.append(S[i] - mid * W[i] / 100)
    ans.sort(reverse=True)
    return sum(ans[:K]) >= 0

left, right = 0, 100
for _ in range(60):
    mid = (left + right) / 2
    if check(mid):
        left = mid  # midが条件を満たすなら、さらに大きい値を探す
    else:
        right = mid # midが条件を満たさないなら、小さい値を探す
print(left)  # 最大のmidを出力