class UnionFind():
    par:list[int]
    size:list[int]
    def __init__(self,N:int) -> None:
        self.par = [-1] * (N+1)
        self.size = [1] * (N+1)
    def root(self,x:int)->int:
        route = [] 
        while True:
            if self.par[x] == -1 : break
            else : 
                route.append(x) #経路圧縮用に通ったルートを保存
                x = self.par[x]
        for r in route:
            self.par[r] = x
        return x
    def unite(self,u:int,v:int):
        ru = self.root(u)
        rv = self.root(v)
        if ru == rv : return
        if self.size[ru] < self.size[rv]:
            self.par[ru] = rv
            self.size[rv] += self.size[ru]
        else :
            self.par[rv] = ru
            self.size[ru] += self.size[rv]
    def same(self,u:int,v:int)->bool:
        return self.root(u) == self.root(v)
    def get_size(self,x:int)->int:
        return self.size[self.root(x)]
    def get_group(self,x:int)->list[int]:
        p = self.root(x)
        return [i for i in range(len(self.par)) if self.root(i) == p]

N,Q = map(int,input().split())
UF = UnionFind(N)
for i in range(Q):
    q,u,v = map(int,input().split())
    if q == 1 : UF.unite(u,v)
    else :
        if UF.same(u,v) : print("Yes")
        else : print("No")