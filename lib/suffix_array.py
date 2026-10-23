from collections import defaultdict, deque

def ManberMyers(S, conv=ord):
    N = len(S)
    d = defaultdict(list)
    for i,s in enumerate(S):
        d[conv(s)].append(i)
    rank = [0]*(N+1)
    i = 1 # offset for empty
    tbd = deque([])
    for k in sorted(d.keys()):
        for t in d[k]:
            rank[t] = i
        i += len(d[k])
        if len(d[k]) > 1:
            tbd.append((d[k],1))
    while tbd:
        target, l = tbd.popleft()
        d = defaultdict(list)
        for t in target:
            nt = rank[t+l] if t+l < N else -1
            d[nt].append(t)
        i = 0
        for k in sorted(d.keys()):
            for t in d[k]:
                rank[t] += i
            i += len(d[k])
            if len(d[k]) > 1:
                tbd.append((d[k],l*2))
    result = [0]*(N+1)
    for i,r in enumerate(rank):
        result[r] = i
    return result

S =input()
SA = ManberMyers(S)

def binary_search(T):
    ng, ok = -1, len(S) + 1
    while ok - ng > 1:
        mid = (ng + ok) // 2
        l = SA[mid]
        if T <= S[l : l + len(T)]:
            ok = mid
        else:
            ng = mid
    return ok

Q = int(input())
for _ in range(Q):
    T =input()
    l = binary_search(T)
    r = binary_search(T + "~")
    print(r - l)