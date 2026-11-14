N, L = map(int,input().split())
K = int(input())
A = list(map(int,input().split()))

def check(mid):
    count = 0
    cur = 0
    for i in range(N):
        if A[i] - cur >= mid and L - A[i] >= mid:
            count += 1
            cur = A[i]
    return count >= K

l = 0
r = L
while l < r:
    mid = (l + r + 1) // 2
    if check(mid):
        l = mid
    else:
        r = mid - 1
print(l)