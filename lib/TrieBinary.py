class Node:
    def __init__(self):
        self.zero = None
        self.one = None
        self.count = 0

# Binary Trieの実装
class Trie:

    def __init__(self):
        self.root = Node()

    def add(self, s):
        node = self.root
        for c in s:
            if c == 0:
                if node.zero is None:
                    node.zero = Node()
                node = node.zero
            else:
                if node.one is None:
                    node.one = Node()
                node = node.one
            node.count += 1

    def remove(self, s):
        node = self.root
        for c in s:
            if c == 0:
                if node.zero.count == 1:
                    node.zero = None
                    return
                node = node.zero
            else:
                if node.one.count == 1:
                    node.one = None
                    return
                node = node.one
            node.count -= 1

    def exec(self, s):
        ans = 0
        node = self.root
        for c in s:
            if c == 1 and node.zero is not None:
                ans += node.zero.count
            if c == 0:
                node = node.zero
            else:
                node = node.one
        return ans + node.count

N, M, K = map(int,input().split())
T = input()
S = [[-1] * K for _ in range(N)]
for i in range(N):
    s = input()
    for j in range(K):
        S[i][j] = 0 if s[j] == T[j] else 1
TRIE = Trie()
for i in range(N):
    TRIE.add(S[i])
Q = int(input())
for _ in range(Q):
    i, j = map(int,input().split())
    TRIE.remove(S[i-1])
    S[i-1][j-1] = 1 - S[i-1][j-1]
    TRIE.add(S[i-1])
    if N == M:
        if sum(S[i-1]) == K:
            print("No")
        else:
            print("Yes")
    else:
        count = TRIE.exec(S[i-1])
        if count <= M:
            print("Yes")
        else:
            print("No")