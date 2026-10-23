from typing import Callable
# 0-indexed
# [l,r)の区間に対してfuncを作用させる
class segmentTree():
    def __init__(self,N:int,INF:int,func:Callable) -> None:
        size = 1
        while size < N : size *= 2
        self.N = N
        self.size = size
        self.INF = INF
        self.func = func
        self.data = [self.INF] * (size*2)

    def get(self,pos:int)->int:
        return self.data[pos + self.size]
    
    def update(self,pos:int,x:int):
        pos = pos + self.size
        self.data[pos] = x
        while pos >= 2:
            pos >>= 1
            self.data[pos] = self.func(self.data[pos*2],self.data[pos*2+1])

    # pos番目にxを足す
    def add(self,pos:int,x:int):
        z = self.get(pos)
        self.update(pos, z + x)

    # pos番目にfuncを作用させる
    def add_f(self,pos:int,x:int):
        z = self.get(pos)
        self.update(pos, self.func(z, x))
    
    def query(self,l:int,r:int)->int:
        l += self.size
        r += self.size
        value_L = self.INF
        value_R = self.INF
        while l < r:
            if l & 1:
                value_L = self.func(value_L, self.data[l])
                l += 1
            if r & 1:
                r -= 1
                value_R = self.func(self.data[r], value_R)
            l >>= 1
            r >>= 1
        return self.func(value_L, value_R)
    
    # funcを満たす最小のrを返す
    def bisect(self, x:int, func:Callable, l:int, r:int) -> int:
        L = l
        while r - l > 1:
            m = (l + r) // 2
            if func(self.query(L, m), x):
                r = m
            else:
                l = m
        return r
    
    # funcを満たす最大のrを返す
    def bisect_left(self, x:int, func:Callable, l:int, r:int) -> int:
        R = r
        while r - l > 1:
            m = (l + r) // 2
            if func(self.query(m, R), x):
                l = m
            else:
                r = m
        return r
    
N, Q = map(int,input().split())
A = list(map(int,input().split()))
ST = segmentTree(N, 0, lambda a, b: a + b)
for i in range(N):
    ST.update(i, A[i])
for _ in range(Q):
    query = list(map(int,input().split()))
    if query[0] == 1:
        i, x = query[1], query[2]
        i -= 1
        ST.update(i, x)
    elif query[0] == 2:
        l, t = query[1], query[2]
        l -= 1
        print(ST.bisect(t, lambda a, b: a >= b, l, N + 1))
    else:
        r, t = query[1], query[2]
        print(ST.bisect_left(t, lambda a, b: a >= b, -1, r))