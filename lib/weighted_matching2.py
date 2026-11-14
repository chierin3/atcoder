N = int(input())
A = []
for i in range(N):
    a = int(input())
    A.append(a)

#辺重みを頂点重みに変換する
#一番左の頂点は番兵として負の無限大を置く
B = [-10**20, 0]
for i in range(N):
    B.append(A[i] - B[i + 1])

candidate = []
stack = []
for i in range(N + 2):
    #stackの上２つの頂点を結ぶ辺の重みが局所最大の場合、その辺を候補に追加する
    while len(stack) >= 3:
        a1 = stack[-3] + stack[-2]
        a2 = stack[-2] + stack[-1]
        a3 = stack[-1] + B[i]
        #a2==a3の場合は、タイブレークでa2を大とする
        if a1 < a2 and a2 >= a3:
            candidate.append(a2)
            stack.pop()
            stack.pop()
        else:
            break
    stack.append(B[i])
#stackに番兵以外の頂点が残っている場合、残りの辺を候補に追加する
while len(stack) >= 3:
    candidate.append(stack[-2] + stack[-1])
    stack.pop()
    stack.pop()
candidate.sort(reverse=True)
ans = 0
for c in candidate:
    ans += c
    print(ans)