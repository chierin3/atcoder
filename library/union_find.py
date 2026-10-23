class UnionFind:
    def __init__(self, n):
        self.parent_or_size = [-1] * n

    def find(self, x):
        if self.parent_or_size[x] < 0:
            return x
        self.parent_or_size[x] = self.find(self.parent_or_size[x])
        return self.parent_or_size[x]

    def union(self, x, y):
        x = self.find(x)
        y = self.find(y)
        if x == y:
            return False
        if self.parent_or_size[x] > self.parent_or_size[y]:
            x, y = y, x
        self.parent_or_size[x] += self.parent_or_size[y]
        self.parent_or_size[y] = x
        return True

    def same(self, x, y):
        return self.find(x) == self.find(y)

    def size(self, x):
        return -self.parent_or_size[self.find(x)]
