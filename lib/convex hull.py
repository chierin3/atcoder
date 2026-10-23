#外積
def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

def get_convex_hull(P:list[tuple[int,int]]):
    sorted_P = sorted(P)
    lower = []
    for p in sorted_P:
        #外積が正の時に追加、負の時に削除
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(sorted_P):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]

N,Q = map(int,input().split())
P = []
for i in range(N):
    x,y = map(int,input().split())
    P.append((x,y))
convex_hull = get_convex_hull(P)
for i in range(Q):
    q = int(input())
    ans = 0
    for j in range(len(convex_hull)):
        ans = max(ans,abs(convex_hull[j][0]-P[q-1][0])+abs(convex_hull[j][1]-P[q-1][1]))
    print(ans)