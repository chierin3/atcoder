import heapq

def aStarPath(G:list[tuple],sp:int)->list:
    visited = [False] * len(G)
    cost = [10**9] * len(G)
    cost[sp] = 0
    Q = []
    heapq.heappush(Q,(0,sp))
    while Q:
        q,p = heapq.heappop(Q)
        if visited[p] : continue
        visited[p] = True
        for g in G[p]:
            pos = g[0]
            cos = g[1]     
            if cost[pos] > q + cos:
                cost[pos] = q + cos
                heapq.heappush(Q,(q + cos,pos))
    return cost


def shortestPath(G:list[tuple],sp:int)->list:
    visited = [False] * len(G)
    cost = [10**9] * len(G)
    cost[sp] = 0
    Q = []
    heapq.heappush(Q,(0,sp))
    while Q:
        q,p = heapq.heappop(Q)
        if visited[p] : continue
        visited[p] = True
        for g in G[p]:
            pos = g[0]
            cos = g[1]     
            if cost[pos] > q + cos:
                cost[pos] = q + cos
                heapq.heappush(Q,(q + cos,pos))
    return cost

N,M = map(int,input().split())
G = [ [] for i in range(N+1) ]
for m in range(M):
    a,b,c = map(int,input().split())
    G[a].append((b,c))
    G[b].append((a,c))
cost = shortestPath(G,1)
for i in range(1,N+1):
    if cost[i] == 10**9 : print(-1)
    else : print(cost[i])