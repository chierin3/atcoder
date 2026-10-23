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
    return min(m1,m2)

# 遅延評価のマージ
def combine(l1,l2):
    return l1 + l2

# 遅延評価の適用
def apply(m,l):
    return m + l

class HeavyLightDecomposition():
    N:int
    G:list[list[int]]
    heavy:list[int]
    depth:list[int]
    parent:list[int]
    size:list[int]
    vertex:list[int]
    id:list[int]
    head:list[int]
    SEG:LazySegmentTree

    def __init__(self,N:int) -> None:
        self.N = N
        self.G = [[] for _ in range(N)]
        self.heavy = [-1] * N
        self.depth = [0] * N
        self.parent = [-1] * N
        self.size = [0] * N
        self.vertex = [-1] * N
        self.id = [-1] * N
        self.head = [0] * N
        self.weight = [0] * N
        self.edge_id = [-1] * N

    def connect(self, u:int, v:int, w:int, i:int):
        self.G[u].append((v, w, i))
        self.G[v].append((u, w, i))

    def built(self):
        stack = [0]
        visited = [False] * self.N
        while stack:
            u = stack.pop()
            if visited[u]:
                self.size[u] = 1
                mx = 0
                for v, w, i in self.G[u]:
                    self.size[u] += self.size[v]
                    if self.size[v] > mx:
                        mx = self.size[v]
                        self.heavy[u] = v
            else:
                visited[u] = True
                stack.append(u)
                for v, w, i in self.G[u]:
                    if not visited[v]:
                        self.parent[v] = u
                        self.depth[v] = self.depth[u] + 1
                        self.weight[v] = w
                        self.edge_id[i] = v
                        stack.append(v)
        stack = [0]
        k = 0
        while stack:
            u = stack.pop()
            self.vertex[k] = u
            self.id[u] = k
            k += 1
            for v, w, i in self.G[u]:
                if v == self.parent[u] : continue
                if v == self.heavy[u]:
                    self.head[v] = self.head[u]
                else:
                    self.head[v] = v
                    stack.append(v)
            if self.heavy[u] != -1:
                stack.append(self.heavy[u])

    def level_ancestor(self, u:int, d:int):
        if (self.depth[u] < d) : return -1
        while(self.depth[self.head[u]] > d):
            u = self.parent[self.head[u]]
        return self.vertex[self.id[u] - (self.depth[u] - d)]
    
    def lca(self, u:int, v:int):
        while self.head[u] != self.head[v]:
            if self.id[u] < self.id[v]:
                u, v = v, u
            u = self.parent[self.head[u]]
        if self.depth[u] > self.depth[v]:
            u, v = v, u
        return u

    def distance(self, u:int, v:int):
        w = self.lca(u, v)
        return self.depth[u] + self.depth[v] - 2 * self.depth[w]
    
    def jump(self, u:int, v:int, i:int):
        w = self.lca(u, v)
        dist = self.distance(u, v)
        if dist < i : return -1
        if i < self.depth[u] - self.depth[w]:
            return self.level_ancestor(u, self.depth[u] - i)
        else:
            return self.level_ancestor(v, self.depth[v] - (dist - i))
        
    def query(self, u:int, v:int):
        w = self.lca(u, v)
        ans = 10**18
        while self.head[u] != self.head[w]:
            ans = min(ans, self.SEG.query(self.id[self.head[u]], self.id[u] + 1))
            u = self.parent[self.head[u]]
        ans = min(ans, self.SEG.query(self.id[w] + 1, self.id[u] + 1))
        while self.head[v] != self.head[w]:
            ans = min(ans, self.SEG.query(self.id[self.head[v]], self.id[v] + 1))
            v = self.parent[self.head[v]]
        ans = min(ans, self.SEG.query(self.id[w] + 1, self.id[v] + 1))
        return ans
    
    def update(self, u:int, v:int, x:int):
        w = self.lca(u, v)
        while self.head[u] != self.head[w]:
            self.SEG.update(self.id[self.head[u]], self.id[u] + 1, x)
            u = self.parent[self.head[u]]
        self.SEG.update(self.id[w] + 1, self.id[u] + 1, x)
        while self.head[v] != self.head[w]:
            self.SEG.update(self.id[self.head[v]], self.id[v] + 1, x)
            v = self.parent[self.head[v]]
        self.SEG.update(self.id[w] + 1, self.id[v] + 1, x)

N = int(input())
HLD = HeavyLightDecomposition(N)
HLD.SEG = LazySegmentTree(N, 10**18, 0, merge, combine, apply)
for i in range(N - 1):
    u, w = map(int,input().split())
    u -= 1
    HLD.connect(u, i + 1, w, i)
HLD.built()
HLD.weight[0] = 10**18
W = [0] * N
for i in range(N):
    W[HLD.id[i]] = HLD.weight[i]
HLD.SEG.build(W)
Q = int(input())
for _ in range(Q):
    u, v = map(int,input().split())
    u -= 1
    v -= 1
    HLD.update(u, v, 1)
R = int(input())
for _ in range(R):
    u, v = map(int,input().split())
    if u == v:
        print(0)
        continue
    u -= 1
    v -= 1
    ans = HLD.query(u, v)
    print(ans)