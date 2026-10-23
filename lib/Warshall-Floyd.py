# Warshall-Floyd Algorithm
INF = 10**10
N = map(int,input().split())
G = [list(map(int, input().split())) for _ in range(N)]
dp = [[INF] * N for _ in range(N)]
for i in range(N):
    for j in range(N):
        dp[i][j] = G[i][j] if G[i][j] >= 0 else INF
for k in range(N):
    for i in range(N):
        for j in range(N):
            dp[i][j] = min(dp[i][j], dp[i][k] + dp[k][j])