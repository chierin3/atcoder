mod = 998244353

class LazySegmentTree:
    """
    遅延評価セグメントツリーのクラス。
    Attributes:
        _n (int): 要素数。
        _size (int): セグメントツリーのサイズ。
        _height (int): セグメントツリーの高さ。
        _INF: モノイドの初期値。
        _INFL: 遅延評価の初期値。
        _func (function): 区間の演算を行う関数。
        _funcL (function): 遅延評価の演算を行う関数。
        _funcR (function): 遅延評価の反映を行う関数。
        _data (list): セグメントツリーのデータを格納するリスト。
        _lazy (list): 遅延評価のデータを格納するリスト。
    Methods:
        __init__(n, INF, INFL, func, funcL, funcR):
            クラスの初期化を行う。
        _propagate_from_top(k):
            遅延評価を上から伝播させる。
        _update_from_bottom(k):
            遅延評価を下から更新する。
        build(array):
            配列からセグメントツリーを構築する。
        update(l, r, x):
            区間 [l, r) の値を更新する。
        query(l, r):
            区間 [l, r) のクエリを処理する。
    """
    def __init__(self,n,INF,INFL,func,funcL,funcR):
        self._n = n
        self._size = 1
        self._height = 0
        while self._size <= n:
            self._size <<= 1
            self._height += 1
        self._INF = INF
        self._INFL = INFL
        self._func = func
        self._funcL = funcL
        self._funcR = funcR
        self._data = [self._INF] * (2 * self._size)
        self._lazy = [self._INFL] * (2 * self._size)

    def _propagate_from_top(self,k):
        k += self._size
        funcL = self._funcL
        funcR = self._funcR
        for h in range(self._height,0,-1):
            i = k >> h
            if self._lazy[i] != self._INFL:
                self._lazy[2*i] = funcL(self._lazy[2*i],self._lazy[i])
                self._lazy[2*i+1] = funcL(self._lazy[2*i+1],self._lazy[i])
                self._data[i] = funcR(self._data[i],self._lazy[i])
                self._lazy[i] = self._INFL

    def _update_from_bottom(self,k):
        k = (k + self._size) >> 1
        func = self._func
        funcR = self._funcR
        while k > 0:
            self._data[k] = func(funcR(self._data[2*k],self._lazy[2*k]),
                                 funcR(self._data[2*k+1],self._lazy[2*k+1]))
            k >>= 1
    
    def build(self,array):
        func = self._func
        for i,x in enumerate(array,self._size):
            self._data[i] = x
        for i in range(self._size-1,0,-1):
            self._data[i] = func(self._data[2*i],self._data[2*i+1])
    
    def update(self,l,r,x):
        funcL = self._funcL
        self._propagate_from_top(l)
        self._propagate_from_top(r-1)
        L = l + self._size
        R = r + self._size
        while L < R:
            if L & 1:
                self._lazy[L] = funcL(self._lazy[L],x)
                L += 1
            if R & 1:
                R -= 1
                self._lazy[R] = funcL(self._lazy[R],x)
            L >>= 1
            R >>= 1
        self._update_from_bottom(l)
        self._update_from_bottom(r-1)
    
    def query(self,l,r):
        func = self._func
        funcR = self._funcR
        self._propagate_from_top(l)
        self._propagate_from_top(r-1)
        L = l + self._size
        R = r + self._size
        res_L = res_R = self._INF
        while L < R:
            if L & 1:
                res_L = func(res_L,funcR(self._data[L],self._lazy[L]))
                L += 1
            if R & 1:
                R -= 1
                res_R = func(funcR(self._data[R],self._lazy[R]),res_R)
            L >>= 1
            R >>= 1
        return func(res_L,res_R)

MASK = (1 << 18) - 1

# モノイドのマージ
def merge(m1,m2):
    return (m1[0] + m2[0], (m1[1] + m2[1]) % mod, (m1[2] + m2[2]) % mod, (m1[3] + m2[3]) % mod, (m1[4] + m2[4]) % mod)

# 遅延評価のマージ
def combine(l1,l2):
    return (l1 + l2) % mod

# 遅延評価の適用
def apply(m,l):
    n = m[0]
    s1 = m[1]
    s2 = m[2]
    s3 = m[3]
    s4 = m[4]
    l2 = (l * l) % mod
    l3 = (l2 * l) % mod
    l4 = (l3 * l) % mod
    s1 = (s1 + (n * l) % mod) % mod
    s2 = (s2 + (2 * m[1] * l) % mod) % mod
    s2 = (s2 + (l2 * n) % mod) % mod
    s3 = (s3 + (3 * m[2] * l) % mod) % mod
    s3 = (s3 + (3 * m[1] * l2) % mod) % mod
    s3 = (s3 + (l3 * n) % mod) % mod
    s4 = (s4 + (4 * m[3] * l) % mod) % mod
    s4 = (s4 + (6 * m[2] * l2) % mod) % mod
    s4 = (s4 + (4 * m[1] * l3) % mod) % mod
    s4 = (s4 + (l4 * n) % mod) % mod
    return (n, s1, s2, s3, s4)

N, Q = map(int,input().split())
A = list(map(int,input().split()))
segtree = LazySegmentTree(N,(0, 0, 0, 0, 0),0,merge,combine,apply)
B = []
for i in range(N):
    B.append((1, A[i], pow(A[i], 2, mod), pow(A[i], 3, mod), pow(A[i], 4, mod)))
segtree.build(B)

for _ in range(Q):
    q = list(map(int,input().split()))
    if q[0] == 1:
        l,r,x = q[1:]
        segtree.update(l-1,r,x)
    elif q[0] == 2:
        l,r,k = q[1:]
        res = segtree.query(l-1,r)
        print(res[k])