class LazySegmentTree:
    """
    遅延評価セグメントツリーのクラス。
    Attributes:
        _n (int): 要素数。
        _size (int): セグメントツリーのサイズ。
        _height (int): セグメントツリーの高さ。
        _INF: 無限大を表す値。
        _INFL: 遅延評価の初期値。
        _func (function): 区間の演算を行う関数。
        _funcL (function): 遅延評価の演算を行う関数。
        _funcR (function): 遅延評価の反映を行う関数。
        _data (list): セグメントツリーのデータを格納するリスト。
        _lazy (list): 遅延評価のデータを格納するリスト。
    Methods:
        __init__(n, INF, INFL, func, funcL, funcR):
            クラスの初期化を行う。
        _reflect(k):
            遅延評価の反映を行う。
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
    
    def _reflect(self,k):
        return self._funcR(self._data[k],self._lazy[k])

    def _propagate_from_top(self,k):
        k += self._size
        for h in range(self._height,0,-1):
            i = k >> h
            if self._lazy[i] != self._INFL:
                self._lazy[2*i] = self._funcL(self._lazy[2*i],self._lazy[i])
                self._lazy[2*i+1] = self._funcL(self._lazy[2*i+1],self._lazy[i])
                self._data[i] = self._reflect(i)
                self._lazy[i] = self._INFL

    def _update_from_bottom(self,k):
        k = (k + self._size) >> 1
        while k > 0:
            self._data[k] = self._func(self._reflect(2*k),self._reflect(2*k+1))
            k >>= 1
    
    def build(self,array):
        for i,x in enumerate(array,self._size):
            self._data[i] = x
        for i in range(self._size-1,0,-1):
            self._data[i] = self._func(self._data[2*i],self._data[2*i+1])
    
    def update(self,l,r,x):
        self._propagate_from_top(l)
        self._propagate_from_top(r-1)
        L = l + self._size
        R = r + self._size
        while L < R:
            if L & 1:
                self._lazy[L] = self._funcL(self._lazy[L],x)
                L += 1
            if R & 1:
                R -= 1
                self._lazy[R] = self._funcL(self._lazy[R],x)
            L >>= 1
            R >>= 1
        self._update_from_bottom(l)
        self._update_from_bottom(r-1)
    
    def query(self,l,r):
        self._propagate_from_top(l)
        self._propagate_from_top(r-1)
        L = l + self._size
        R = r + self._size
        res_L = res_R = self._INF
        while L < R:
            if L & 1:
                res_L = self._func(res_L,self._reflect(L))
                L += 1
            if R & 1:
                R -= 1
                res_R = self._func(self._reflect(R),res_R)
            L >>= 1
            R >>= 1
        return self._func(res_L,res_R)
    
from operator import add
INF = 1 << 60
N = int(input())
A = list(map(int,input().split()))
segtree = LazySegmentTree(N,INF,0,min,add,add)
segtree.build(A)

Q = int(input())
for _ in range(Q):
    q = list(map(int,input().split()))
    if q[0] == 1:
        l,r,x = q[1:]
        segtree.update(l,r,x)
    elif q[0] == 2:
        l,r = q[1:]
        print(segtree.query(l,r))