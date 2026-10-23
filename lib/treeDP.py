
class TreeDP:
    def __init__(self, n, v, func):
        self.n = n
        self.v = v
        self.func = func
        self.edges = [[] for _ in range(n + 1)]
        self.dp = [v] * (n + 1)

    def add_edge(self, u, v):
        self.edges[u].append(v)

    def build(self, root=1):
        stack = [root]
        visited = [False] * (self.n + 1)
        completed = [False] * (self.n + 1)
        while stack:
            v = stack.pop()
            if visited[v]:
                if not completed[v]:
                    completed[v] = True
                    dp2 = []
                    for u in self.edges[v]:
                        dp2.append(self.dp[u])
                    self.dp[v] = self.func(dp2) + 1
            else:
                visited[v] = True
                stack.append(v)
                for u in self.edges[v]:
                    if not visited[u]:
                        stack.append(u)

def merge(dp):
    return sum(dp)

N = int(input())
tree = TreeDP(N, 0, merge)
for _ in range(N - 1):
    a, b = map(int, input().split())
    tree.add_edge(a, b)
    tree.add_edge(b, a)
tree.build()
max_size = 0
for v in tree.edges[1]:
    max_size = max(max_size, tree.dp[v])
print(N - max_size)