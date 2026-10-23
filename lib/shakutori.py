# 尺取り法をdequeを使って実装
from collections import deque
N,K = map(int,input().split())
S = [int(input()) for i in range(N)]
prod = 1
ans = 0
Q = deque()
for i in range(N):
    Q.append(S[i])
    prod *= S[i]
    while Q and prod > K:
        q = Q.popleft()
        prod //= q
    ans = max(ans, len(Q))
print(ans)