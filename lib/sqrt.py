import math

# n以下の最大の整数平方根を返す
def isqrt_bs(n):
    if n < 0:
        return -1
    left, right = 0, n
    ans = 0
    while left <= right:
        mid = (left + right) // 2
        if mid * mid <= n:
            ans = mid
            left = mid + 1
        else:
            right = mid - 1
    return ans

# l以上r以下の完全平方数の個数を返す（二分探索版）遅い
def get_sqrt_num_bs(l, r):
    return isqrt_bs(r) - isqrt_bs(l - 1)

# l以上r以下の完全平方数の個数を返す（まあまあ速い）
def get_sqrt_num(l, r):
    return math.floor(math.isqrt(r)) - math.floor(math.isqrt(l - 1))

T = int(input())
for _ in range(T):
    C, D = map(int,input().split())
    K = math.floor(math.log10(C + D)) + 1
    ans = 0
    for i in range(1, K + 1):
        L = max(1, 10 ** (i - 1) - C)
        R = min(D, 10 ** i - C - 1)
        if L <= R:
            c = C * (10 ** i) + C
            ans += get_sqrt_num_bs(c + L, c + R)
    print(ans)