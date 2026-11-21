def alien_trick(X, l1, l2, solve):
    res1 = solve(l1)
    res2 = solve(l2)
    while l1 + 1 < l2:
        l = (l1 + l2) // 2
        res = solve(l)
        if res[1] > X:
            l1 = l
            res1 = res
        else:
            l2 = l
            res2 = res
    return max(res1[0] - l1 * X, res2[0] - l2 * X)

N, R = map(int,input().split())
A = list(map(int,input().split()))

def solve(pena):
    dp = [[(10**20, 0)] * 2 for _ in range(N)]
    dp[0][0] = (0, 0)
    dp[0][1] = (pena, 1)
    for i in range(1, N):
        dp[i][0] = min(dp[i][0], dp[i - 1][0])
        val = dp[i - 1][1][0] - A[i - 1]
        if val < dp[i][0][0]:
            dp[i][0] = (val, dp[i - 1][1][1])
        val = dp[i - 1][0][0] - A[i - 1] + pena
        if val < dp[i][1][0]:
            dp[i][1] = (val, dp[i - 1][0][1] + 1)
        val = dp[i - 1][1][0] + pena
        if val < dp[i][1][0]:
            dp[i][1] = (val, dp[i - 1][1][1] + 1)
    return min(dp[N - 1][0], dp[N - 1][1])

l1 = -10**10
l2 = 10**10
ans = alien_trick(R, l1, l2, solve)
print(-ans)