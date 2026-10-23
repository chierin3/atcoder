from typing import Callable

class Monoid():
    count1 = 0
    count2 = 0
    max_val1 = 0
    max_val2 = 0

def merge(a:Monoid, b:Monoid) -> Monoid:
    c = Monoid()
    if a.max_val1 == b.max_val1:
        c.max_val1 = a.max_val1
        c.count1 = a.count1 + b.count1
        c.max_val2 = max(a.max_val2, b.max_val2)
        if c.max_val2 == a.max_val2:
            c.count2 = a.count2
        if c.max_val2 == b.max_val2:
            c.count2 += b.count2
    elif a.max_val1 > b.max_val1:
        c.max_val1 = a.max_val1
        c.count1 = a.count1
        c.max_val2 = max(a.max_val2, b.max_val1)
        if c.max_val2 == a.max_val2:
            c.count2 = a.count2
        if c.max_val2 == b.max_val1:
            c.count2 += b.count1
    else:
        c.max_val1 = b.max_val1
        c.count1 = b.count1
        c.max_val2 = max(a.max_val1, b.max_val2)
        if c.max_val2 == a.max_val1:
            c.count2 = a.count1
        if c.max_val2 == b.max_val2:
            c.count2 += b.count2
    return c

# 0-indexed
# [l,r)の区間に対してfuncを作用させる
class segmentTree():
    # N: 要素数, e: 単位元を返す関数, op: 二項演算
    def __init__(self, N:int, e:Callable, op:Callable) -> None:
        size = 1
        while size < N : size *= 2
        self.N = N
        self.size = size
        self.INF = e()
        self.op = op
        self.data = [e() for _ in range(size * 2)]

    def build(self, A:list):
        for i in range(len(A)):
            self.data[i + self.size] = A[i]
        for i in range(self.size - 1, 0, -1):
            self.data[i] = self.op(self.data[i * 2], self.data[i * 2 + 1])

    def get(self, pos:int) -> Monoid:
        return self.data[pos + self.size]
    
    def update(self, pos:int, x:Monoid):
        pos = pos + self.size
        self.data[pos] = x
        while pos >= 2:
            pos >>= 1
            self.data[pos] = self.op(self.data[pos * 2],self.data[pos * 2 + 1])

    # pos番目にfuncを作用させる
    def add_f(self, pos:int, x:Monoid):
        z = self.get(pos)
        self.update(pos, self.op(z, x))
    
    def query(self, l:int, r:int) -> Monoid:
        l += self.size
        r += self.size
        value_L = self.INF
        value_R = self.INF
        while l < r:
            if l & 1:
                value_L = self.op(value_L, self.data[l])
                l += 1
            if r & 1:
                r -= 1
                value_R = self.op(self.data[r], value_R)
            l >>= 1
            r >>= 1
        return self.op(value_L, value_R)
    
    # funcを満たす最小のrを返す
    def bisect(self, x:int, func:Callable) -> int:
        l = 0
        r = self.N
        while r - l > 1:
            m = (l + r) // 2
            if func(self.query(0, m), x):
                r = m
            else:
                l = m
        return r
    
N, Q = map(int,input().split())
A = list(map(int,input().split()))
ST = segmentTree(N, Monoid, merge)
B = [Monoid() for _ in range(N)]
for i in range(N):
    B[i].max_val1 = A[i]
    B[i].count1 = 1
ST.build(B)
for _ in range(Q):
    query = list(map(int,input().split()))
    if query[0] == 1:
        p, x = query[1], query[2]
        p -= 1
        m = Monoid()
        m.max_val1 = x
        m.count1 = 1
        ST.update(p, m)
    else:
        l, r = query[1], query[2]
        res = ST.query(l - 1, r)
        print(res.count2)