from sortedcontainers import SortedList
N = int(input())
LR = []
for i in range(N):
    l,r = map(int,input().split())
    LR.append((l,r))
LR.sort()
S = SortedList()
ans = 0
for l,r in LR[::-1]:
    ans += S.bisect_right(r)
    S.add(l)
print(ans)